"""Independent contract tests for the frozen Dark Factory finding contract.

The Step 1 gate: reject drift, extra fields, and restricted values. These tests
never touch a runtime; they read the frozen contract and the frozen legacy
oracles only.

The cross-check against the legacy oracle is what stops the expected fixture
from being a self-portrait. The fixture is produced by the detector, so on its
own it could only prove the detector agrees with itself; agreeing with an
independently frozen legacy artifact is what makes it truth.
"""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any, Mapping

import jsonschema
import yaml

import contracts as contract_loader
from canonical import encode
from errors import PrivacyViolationError
from findings import privacy

RUNTIME_VARIABLE = {
    "created_at": "2026-07-24T00:00:00Z",
    "finding_id": "sha256:" + "0" * 64,
}
DETECTOR_DIGEST = "sha256:" + "1" * 64


def _complete(fixture: Mapping[str, Any]) -> dict[str, Any]:
    """Fill the three members a fixture deliberately does not pin."""

    finding = copy.deepcopy(dict(fixture))
    finding.update(RUNTIME_VARIABLE)
    finding["references"]["detector_source_sha256"] = DETECTOR_DIGEST
    return finding


class FindingContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = contract_loader.load()
        self.fixtures: dict[str, dict[str, Any]] = {}
        for scenario in self.contract.scenarios:
            path = contract_loader.expected_finding_path(scenario)
            self.fixtures[scenario] = json.loads(path.read_text(encoding="utf-8"))

    def test_every_registered_scenario_has_a_frozen_expected_finding(self) -> None:
        """Registry-driven, so expansion cannot leave a scenario unpinned."""

        self.assertTrue(self.fixtures)
        self.assertEqual(
            sorted(self.fixtures), sorted(self.contract.scenarios)
        )
        for scenario, fixture in self.fixtures.items():
            self.assertEqual(fixture["scenario"], scenario)

    def test_all_five_source_defect_seeds_are_registered(self) -> None:
        """Expansion is complete: every DF-SOURCE seed has a binding."""

        self.assertEqual(
            sorted(self.contract.scenarios),
            [f"DF-SOURCE-00{index}" for index in range(1, 6)],
        )
        self.assertEqual(
            sorted(
                scenario.type_number
                for scenario in self.contract.scenarios.values()
            ),
            ["01", "02", "03", "04", "05"],
        )

    def test_each_scenario_binds_a_distinct_batch_and_relation_set(self) -> None:
        """A copied binding would make two types observe the same rows."""

        scenarios = list(self.contract.scenarios.values())
        for attribute in (
            "batch_id",
            "staging_relation",
            "operational_relation",
            "reporting_relation",
            "contract_code",
        ):
            values = [getattr(scenario, attribute) for scenario in scenarios]
            self.assertEqual(
                len(set(values)), len(values), f"duplicate {attribute} binding"
            )
        peers = [peer for scenario in scenarios for peer in scenario.required_peers]
        self.assertEqual(len(set(peers)), len(peers), "duplicate peer binding")

    def test_every_registered_scenario_binds_frozen_legacy_artifacts(self) -> None:
        for name, scenario in self.contract.scenarios.items():
            with self.subTest(scenario=name):
                self.assertTrue(
                    scenario.contract_oracle.is_file(),
                    "the frozen legacy oracle is missing",
                )
                self.assertTrue(
                    scenario.raw_fixture.is_file(),
                    "the frozen raw fixture is missing",
                )
                self.assertEqual(len(scenario.required_peers), 2)

    def test_expected_findings_satisfy_the_closed_schema(self) -> None:
        for scenario, fixture in self.fixtures.items():
            with self.subTest(scenario=scenario):
                jsonschema.validate(
                    instance=_complete(fixture),
                    schema=dict(self.contract.schema),
                )

    def test_schema_closes_every_object(self) -> None:
        """No object may accept an unknown member, at any depth."""

        def walk(node: Any, path: str) -> None:
            if not isinstance(node, dict):
                return
            if node.get("type") == "object":
                self.assertIs(
                    node.get("additionalProperties"),
                    False,
                    f"object at {path} does not reject unknown members",
                )
                self.assertIn("required", node, f"object at {path} has no required")
                self.assertEqual(
                    sorted(node["required"]),
                    sorted(node.get("properties", {})),
                    f"object at {path} does not require every declared member",
                )
            for key, child in node.items():
                if key in {"properties", "$defs"} and isinstance(child, dict):
                    for name, value in child.items():
                        walk(value, f"{path}/{key}/{name}")
                elif key == "items":
                    walk(child, f"{path}/items")

        walk(dict(self.contract.schema), "#")

    def test_schema_rejects_an_unknown_member(self) -> None:
        for scenario, fixture in self.fixtures.items():
            with self.subTest(scenario=scenario):
                drifted = _complete(fixture)
                drifted["unexpected_member"] = "anything"
                with self.assertRaises(jsonschema.ValidationError):
                    jsonschema.validate(
                        instance=drifted, schema=dict(self.contract.schema)
                    )

    def test_schema_rejects_a_nested_unknown_member(self) -> None:
        drifted = _complete(self.fixtures["DF-SOURCE-001"])
        drifted["controls"]["compared"][0]["raw_row"] = "anything"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=drifted, schema=dict(self.contract.schema))

    def test_schema_rejects_money_expressed_as_a_number(self) -> None:
        drifted = _complete(self.fixtures["DF-SOURCE-001"])
        for entry in drifted["controls"]["compared"]:
            if entry["value_class"] == "money":
                entry["declared"] = 173.44
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=drifted, schema=dict(self.contract.schema))

    def test_schema_pins_approval_and_remediation_to_not_requested(self) -> None:
        for member in ("approval", "remediation"):
            with self.subTest(member=member):
                drifted = _complete(self.fixtures["DF-SOURCE-001"])
                drifted[member]["state"] = "requested"
                with self.assertRaises(jsonschema.ValidationError):
                    jsonschema.validate(
                        instance=drifted, schema=dict(self.contract.schema)
                    )

    def test_allowlist_accepts_every_expected_finding(self) -> None:
        for scenario, fixture in self.fixtures.items():
            with self.subTest(scenario=scenario):
                privacy.enforce_allowlist(
                    _complete(fixture), self.contract.allowlist
                )

    def test_allowlist_rejects_an_unapproved_member(self) -> None:
        drifted = _complete(self.fixtures["DF-SOURCE-001"])
        drifted["holder_name"] = "anything"
        with self.assertRaises(PrivacyViolationError):
            privacy.enforce_allowlist(drifted, self.contract.allowlist)

    def test_allowlist_covers_exactly_the_expected_finding_surface(self) -> None:
        """Every allowlist path is reachable, and every leaf is allowlisted.

        An allowlist with dead entries drifts silently away from the schema, so
        the correspondence is asserted in both directions.
        """

        declared = set(self.contract.allowlist["paths"])
        observed: set[str] = set()
        for fixture in self.fixtures.values():
            observed |= {path for path, _ in privacy._paths(_complete(fixture))}
        self.assertEqual(observed - declared, set(), "unallowlisted finding members")
        self.assertEqual(declared - observed, set(), "unreachable allowlist entries")

    def test_error_codes_cover_every_raised_code(self) -> None:
        import errors

        declared = set(self.contract.error_codes["codes"])
        raised = {
            value.code
            for value in vars(errors).values()
            if isinstance(value, type)
            and issubclass(value, errors.DarkFactoryError)
            and value is not errors.DarkFactoryError
        }
        self.assertEqual(raised - declared, set(), "undeclared error codes")
        self.assertEqual(declared - raised, set(), "unraised error codes")


class LegacyOracleAgreementTest(unittest.TestCase):
    """The expected finding must agree with the frozen legacy oracle.

    The legacy oracle under ``contracts/types/**`` is a separate, frozen source
    of correctness owned by the legacy baseline. Reading it here — rather than
    regenerating it — keeps the two roles distinct while proving they agree.
    """

    def setUp(self) -> None:
        self.contract = contract_loader.load()

    def _oracle(self, scenario_name: str) -> Mapping[str, Any]:
        scenario = self.contract.scenarios[scenario_name]
        return yaml.safe_load(
            Path(scenario.contract_oracle).read_text(encoding="utf-8")
        )

    def _fixture(self, scenario_name: str) -> Mapping[str, Any]:
        return json.loads(
            contract_loader.expected_finding_path(scenario_name).read_text(
                encoding="utf-8"
            )
        )

    def test_every_oracle_control_pair_appears_with_the_oracle_values(self) -> None:
        for scenario_name in self.contract.scenarios:
            with self.subTest(scenario=scenario_name):
                oracle = self._oracle(scenario_name)
                fixture = self._fixture(scenario_name)
                compared = {
                    entry["control"]: entry
                    for entry in fixture["controls"]["compared"]
                }
                pairs = [
                    key[len("declared_") :]
                    for key in oracle
                    if key.startswith("declared_")
                    and f"computed_{key[len('declared_'):]}" in oracle
                ]
                self.assertTrue(pairs, "oracle declares no control pairs")
                for name in pairs:
                    self.assertIn(name, compared, f"control {name} is not compared")
                    self.assertEqual(
                        compared[name]["declared"],
                        str(oracle[f"declared_{name}"]),
                    )
                    self.assertEqual(
                        compared[name]["computed"],
                        str(oracle[f"computed_{name}"]),
                    )

    def test_terminal_isolation_and_attribution_match_the_oracle(self) -> None:
        for scenario_name in self.contract.scenarios:
            with self.subTest(scenario=scenario_name):
                oracle = self._oracle(scenario_name)
                fixture = self._fixture(scenario_name)
                self.assertEqual(fixture["batch"]["batch_id"], oracle["batch_id"])
                self.assertEqual(fixture["scenario"], oracle["scenario"])
                self.assertEqual(
                    fixture["terminal"]["status"], oracle["expected_status"]
                )
                self.assertEqual(fixture["terminal"]["code"], oracle["expected_code"])
                self.assertEqual(
                    fixture["terminal"]["stage"], oracle["expected_stage"]
                )
                self.assertEqual(
                    fixture["isolation"]["sanitized_csv_present"],
                    oracle["csv_produced"],
                )
                self.assertEqual(
                    fixture["isolation"]["postgres_business_mutation"],
                    oracle["postgres_business_mutation"],
                )
                self.assertEqual(
                    fixture["isolation"]["quarantine_scope"],
                    oracle["quarantine_scope"],
                )
                self.assertEqual(
                    fixture["continuation"]["observed"],
                    oracle["unrelated_batches_continue"],
                )
                self.assertEqual(
                    fixture["attribution"]["owner"],
                    f"source_{oracle['source_system_role']}",
                )
                self.assertEqual(fixture["attribution"]["confidence"], "conclusive")

    def test_type01_matches_the_published_first_acceptance_target(self) -> None:
        """The exact first-acceptance-target table in DR-011, value by value."""

        fixture = self._fixture("DF-SOURCE-001")
        compared = {
            entry["control"]: entry for entry in fixture["controls"]["compared"]
        }
        self.assertEqual(fixture["batch"]["type_number"], "01")
        self.assertEqual(fixture["batch"]["batch_id"], "B202607230000004")
        self.assertEqual(compared["net_amount"]["declared"], "173.44")
        self.assertEqual(compared["net_amount"]["computed"], "173.45")
        self.assertEqual(compared["detail_count"]["declared"], "2")
        self.assertEqual(compared["detail_count"]["computed"], "2")
        self.assertEqual(fixture["terminal"]["status"], "quarantined")
        self.assertEqual(
            fixture["terminal"]["code"], "SOURCE_CONTROL_TOTAL_MISMATCH"
        )
        self.assertEqual(
            fixture["attribution"]["owner"], "source_system_of_record"
        )
        self.assertFalse(fixture["isolation"]["sanitized_csv_present"])
        self.assertFalse(fixture["isolation"]["postgres_business_mutation"])
        self.assertEqual(fixture["isolation"]["quarantine_scope"], "batch")
        self.assertEqual(
            [peer["batch_id"] for peer in fixture["continuation"]["peers"]],
            ["B202402290000001", "B202607230000002"],
        )
        for peer in fixture["continuation"]["peers"]:
            self.assertEqual(peer["status"], "succeeded")

    def test_fixture_files_are_stored_canonically_sorted(self) -> None:
        for scenario_name in self.contract.scenarios:
            with self.subTest(scenario=scenario_name):
                path = contract_loader.expected_finding_path(scenario_name)
                stored = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(
                    path.read_bytes(),
                    json.dumps(stored, indent=2, sort_keys=True).encode() + b"\n",
                )
                # Canonical encoding must round-trip the stored document.
                self.assertEqual(json.loads(encode(stored).decode()), stored)


if __name__ == "__main__":
    unittest.main()
