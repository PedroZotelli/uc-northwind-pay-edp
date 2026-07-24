"""Adversarial probes against each privacy layer, independently.

Each restricted class is injected into a valid finding and each layer is asked
to refuse it on its own. Proving the layers are independently sufficient is what
makes "privacy-clean" a property rather than an assertion.
"""

from __future__ import annotations

import copy
import json
import re
import unittest
from pathlib import Path
from typing import Any

import jsonschema

from darkfactory import contracts as contract_loader
from darkfactory.errors import PrivacyViolationError, SchemaViolationError
from darkfactory.findings import privacy
from darkfactory.findings import writer as finding_writer

DIGIT_RUN = re.compile(r"\d+")


def _complete(fixture: dict[str, Any]) -> dict[str, Any]:
    finding = copy.deepcopy(fixture)
    finding["created_at"] = "2026-07-24T00:00:00Z"
    finding["finding_id"] = "sha256:" + "0" * 64
    finding["references"]["detector_source_sha256"] = "sha256:" + "1" * 64
    return finding


class PrivacyLayerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = contract_loader.load()
        self.scenario = self.contract.scenarios["DF-SOURCE-001"]
        self.finding = _complete(
            json.loads(
                contract_loader.expected_finding_path("DF-SOURCE-001").read_text(
                    encoding="utf-8"
                )
            )
        )

    def _scan(self, finding: dict[str, Any]) -> None:
        privacy.scan(
            finding,
            allowlist=self.contract.allowlist,
            raw_fixture=self.scenario.raw_fixture,
            raw_encoding=self.scenario.raw_encoding,
            scenario=self.scenario.scenario,
            batch_id=self.scenario.batch_id,
            contract_code=self.scenario.contract_code,
            terminal_code=self.scenario.terminal_code,
            type_number=self.scenario.type_number,
            peers=self.scenario.required_peers,
        )

    def test_the_approved_finding_passes_every_layer(self) -> None:
        finding_writer.validate_schema(self.finding, self.contract.schema)
        self._scan(self.finding)

    # Layer 1 — the closed schema.

    def test_layer_one_refuses_a_free_text_member(self) -> None:
        leaked = copy.deepcopy(self.finding)
        leaked["exception_text"] = "unbounded processor output"
        with self.assertRaises(SchemaViolationError):
            finding_writer.validate_schema(leaked, self.contract.schema)

    def test_layer_one_refuses_a_raw_row_member(self) -> None:
        leaked = copy.deepcopy(self.finding)
        leaked["controls"]["compared"][0]["raw_row"] = "H0001..."
        with self.assertRaises(SchemaViolationError):
            finding_writer.validate_schema(leaked, self.contract.schema)

    # Layer 2a — the positive field allowlist.

    def test_layer_two_refuses_an_unapproved_path(self) -> None:
        leaked = copy.deepcopy(self.finding)
        leaked["cardholder_name"] = "an unapproved value"
        with self.assertRaises(PrivacyViolationError):
            privacy.enforce_allowlist(leaked, self.contract.allowlist)

    def test_layer_two_refuses_an_approved_path_holding_a_foreign_shape(self) -> None:
        leaked = copy.deepcopy(self.finding)
        leaked["controls"]["compared"][0]["control"] = "PAN 4111111111111111"
        with self.assertRaises(PrivacyViolationError):
            privacy.enforce_allowlist(leaked, self.contract.allowlist)

    def test_layer_two_refuses_a_digest_that_is_not_a_digest(self) -> None:
        leaked = copy.deepcopy(self.finding)
        leaked["references"]["raw_sha256"] = "12345678901"
        with self.assertRaises(PrivacyViolationError):
            privacy.enforce_allowlist(leaked, self.contract.allowlist)

    # Layer 2b — identity binding to frozen contract truth.

    def test_layer_two_refuses_a_foreign_batch_identity(self) -> None:
        leaked = copy.deepcopy(self.finding)
        leaked["batch"]["batch_id"] = "B999999999999999"
        with self.assertRaises(PrivacyViolationError):
            self._scan(leaked)

    def test_layer_two_refuses_a_peer_outside_the_scenario_contract(self) -> None:
        leaked = copy.deepcopy(self.finding)
        leaked["continuation"]["peers"][0]["batch_id"] = "B111111111111111"
        with self.assertRaises(PrivacyViolationError):
            self._scan(leaked)

    def test_layer_two_refuses_a_mismatched_contract_code(self) -> None:
        leaked = copy.deepcopy(self.finding)
        leaked["batch"]["contract_code"] = "PIX_EVENTS01"
        with self.assertRaises(PrivacyViolationError):
            self._scan(leaked)

    # Layer 3 — the restricted corpus scan.

    def _restricted_identifier(self) -> str:
        tokens = privacy.extract_restricted_digits(
            self.scenario.raw_fixture,
            self.scenario.raw_encoding,
            self.contract.allowlist,
        )
        exempt = privacy.structural_digits(
            (self.scenario.batch_id, *self.scenario.required_peers)
        )
        candidates = sorted(
            token
            for token in tokens
            if len(token) == 16
            and not any(token in identity for identity in exempt)
        )
        self.assertTrue(candidates, "the fixture yields no restricted identifier")
        return candidates[0]

    def test_the_fixture_actually_contains_restricted_identifiers(self) -> None:
        """A corpus scan against an empty corpus would pass vacuously."""

        self.assertTrue(self._restricted_identifier())

    def test_layer_three_refuses_a_leaked_identifier(self) -> None:
        """The canary: a sixteen-digit identifier in a member shaped to hold it.

        ``batch.contract_code`` accepts ``[A-Z0-9_]{1,16}``, so a PAN satisfies
        layer 2a's pattern. Layer 3 must catch it on its own, which is what
        keeps the layer meaningful if a future contract change opens a hole.
        """

        leaked = copy.deepcopy(self.finding)
        leaked["batch"]["contract_code"] = self._restricted_identifier()
        with self.assertRaises(PrivacyViolationError):
            privacy.enforce_restricted_corpus(
                leaked,
                privacy.extract_restricted_digits(
                    self.scenario.raw_fixture,
                    self.scenario.raw_encoding,
                    self.contract.allowlist,
                ),
                privacy.structural_digits(
                    (self.scenario.batch_id, *self.scenario.required_peers)
                ),
                self.contract.allowlist,
            )

    def test_layer_two_pattern_alone_would_have_admitted_that_identifier(self) -> None:
        """Proves the canary is testing layer 3 rather than layer 2's pattern."""

        definition = self.contract.allowlist["value_classes"]["contract-code"]
        self.assertIsNotNone(
            re.match(definition["pattern"], self._restricted_identifier())
        )

    def test_layer_three_ignores_digest_members(self) -> None:
        """A digest's value is content-addressed, not chosen by the detector."""

        text = privacy.scannable_text(self.finding, self.contract.allowlist)
        self.assertNotIn(self.finding["references"]["raw_sha256"], text)
        self.assertIn(self.finding["batch"]["batch_id"], text)

    def test_layer_three_does_not_flag_the_batch_identity(self) -> None:
        """The batch identity is a long digit run inside the fixture too."""

        self._scan(self.finding)

    def test_layer_three_survives_every_scenario_fixture(self) -> None:
        for name, scenario in self.contract.scenarios.items():
            with self.subTest(scenario=name):
                finding = _complete(
                    json.loads(
                        contract_loader.expected_finding_path(name).read_text(
                            encoding="utf-8"
                        )
                    )
                )
                privacy.scan(
                    finding,
                    allowlist=self.contract.allowlist,
                    raw_fixture=scenario.raw_fixture,
                    raw_encoding=scenario.raw_encoding,
                    scenario=scenario.scenario,
                    batch_id=scenario.batch_id,
                    contract_code=scenario.contract_code,
                    terminal_code=scenario.terminal_code,
                    type_number=scenario.type_number,
                    peers=scenario.required_peers,
                )


class NoRestrictedValueReachesAnyFixtureTest(unittest.TestCase):
    """The frozen expected fixtures themselves must be privacy-clean.

    They are committed artifacts, so a leak in one would be a leak in the
    repository, not only in a run.
    """

    def test_no_fixture_contains_a_restricted_identifier(self) -> None:
        contract = contract_loader.load()
        for name, scenario in contract.scenarios.items():
            with self.subTest(scenario=name):
                tokens = privacy.extract_restricted_digits(
                    scenario.raw_fixture,
                    scenario.raw_encoding,
                    contract.allowlist,
                )
                exempt = privacy.structural_digits(
                    (scenario.batch_id, *scenario.required_peers)
                )
                fixture = json.loads(
                    contract_loader.expected_finding_path(name).read_text(
                        encoding="utf-8"
                    )
                )
                published = privacy.scannable_text(fixture, contract.allowlist)
                for token in tokens:
                    if any(token in identity for identity in exempt):
                        continue
                    self.assertNotIn(
                        token,
                        published,
                        f"{name} fixture carries a restricted identifier",
                    )


if __name__ == "__main__":
    unittest.main()
