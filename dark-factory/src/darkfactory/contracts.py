"""Loading of the Dark Factory executable contract.

The contract is the Dark Factory's own source of correctness. It is separate
from the legacy contracts under ``contracts/types/``, which this component reads
as an independent input and never regenerates.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

from .config import CONTRACT_ROOT, REPOSITORY_ROOT, read_bytes, read_yaml
from .errors import ObservationMissingError


@dataclass(frozen=True, slots=True)
class Scenario:
    """One canonical DF-SOURCE seed bound to immutable legacy identities."""

    scenario: str
    type_number: str
    contract_slug: str
    contract_code: str
    batch_id: str
    terminal_code: str
    terminal_stage: str
    contract_oracle: Path
    raw_fixture: Path
    raw_encoding: str
    staging_relation: str
    operational_relation: str
    reporting_relation: str
    # The control plane persists rejection controls under generic column names.
    # These bind those columns to this type's control names, so the agreement
    # check compares like with like instead of guessing by value shape.
    control_plane_count_control: str
    control_plane_net_control: str
    required_peers: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DarkFactoryContract:
    """The frozen Dark Factory contract as one immutable value."""

    detector_name: str
    detector_version: str
    detector_method: str
    schema_version: str
    finding_version: int
    finding_code: str
    scenarios: Mapping[str, Scenario]
    schema: Mapping[str, Any]
    allowlist: Mapping[str, Any]
    error_codes: Mapping[str, Any]

    def for_type(self, type_number: str) -> Scenario:
        for scenario in self.scenarios.values():
            if scenario.type_number == type_number:
                return scenario
        raise ObservationMissingError(
            f"no Dark Factory scenario is registered for type {type_number}"
        )


@lru_cache(maxsize=1)
def load() -> DarkFactoryContract:
    """Load and freeze the Dark Factory contract."""

    document = read_yaml(CONTRACT_ROOT / "scenarios.yaml")
    detector = document["detector"]
    finding = document["finding"]
    scenarios = {
        entry["scenario"]: Scenario(
            scenario=entry["scenario"],
            type_number=entry["type_number"],
            contract_slug=entry["contract_slug"],
            contract_code=entry["contract_code"],
            batch_id=entry["batch_id"],
            terminal_code=entry["terminal_code"],
            terminal_stage=entry["terminal_stage"],
            contract_oracle=REPOSITORY_ROOT / entry["contract_oracle"].strip(),
            raw_fixture=REPOSITORY_ROOT / entry["raw_fixture"].strip(),
            raw_encoding=entry["raw_encoding"],
            staging_relation=entry["staging_relation"],
            operational_relation=entry["operational_relation"],
            reporting_relation=entry["reporting_relation"],
            control_plane_count_control=(
                entry["control_plane_controls"]["count"]
            ),
            control_plane_net_control=(
                entry["control_plane_controls"]["net_amount"]
            ),
            required_peers=tuple(entry["required_peers"]),
        )
        for entry in document["scenarios"]
    }
    return DarkFactoryContract(
        detector_name=detector["name"],
        detector_version=detector["version"],
        detector_method=detector["method"],
        schema_version=finding["schema_version"],
        finding_version=int(finding["finding_version"]),
        finding_code=finding["code"],
        scenarios=MappingProxyType(scenarios),
        schema=json.loads(read_bytes(CONTRACT_ROOT / "finding.schema.json")),
        allowlist=read_yaml(CONTRACT_ROOT / "privacy-allowlist.yaml"),
        error_codes=read_yaml(CONTRACT_ROOT / "error-codes.yaml"),
    )


def expected_finding_path(scenario: str) -> Path:
    """Return the frozen Dark Factory expected-finding fixture for a scenario."""

    return (
        CONTRACT_ROOT
        / "expected"
        / f"{scenario.lower()}-finding.json"
    )
