"""Validation and atomic publication of one Dark Factory evidence packet.

Dark Factory evidence lives under its own root and never touches the legacy
evidence tree. A packet is published all-or-nothing by renaming a private
temporary directory, so a reader never sees a partial packet.
"""

from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any, Mapping

import jsonschema  # type: ignore[import-untyped]  # no stubs in the frozen dependency set

from ..canonical import serialize
from ..contracts import DarkFactoryContract, Scenario
from ..errors import EvidenceConflictError, SchemaViolationError
from ..observations.collect import ObservationSet
from . import privacy

PACKET_FILES: tuple[str, ...] = (
    "finding.json",
    "detector-run.json",
    "observation-index.json",
    "privacy-scan.json",
)


def validate_schema(finding: Mapping[str, Any], schema: Mapping[str, Any]) -> None:
    """Layer 1. Refuse a candidate that does not satisfy the closed schema."""

    try:
        jsonschema.validate(instance=dict(finding), schema=dict(schema))
    except jsonschema.ValidationError as exc:
        raise SchemaViolationError(
            f"candidate finding violates the closed schema at "
            f"{'/'.join(str(part) for part in exc.absolute_path) or '<root>'}"
        ) from exc


def enforce(
    finding: Mapping[str, Any],
    *,
    contract: DarkFactoryContract,
    scenario: Scenario,
) -> None:
    """Run all three privacy layers over a candidate finding."""

    validate_schema(finding, contract.schema)
    privacy.scan(
        finding,
        allowlist=contract.allowlist,
        raw_fixture=scenario.raw_fixture,
        raw_encoding=scenario.raw_encoding,
        scenario=scenario.scenario,
        batch_id=scenario.batch_id,
        contract_code=scenario.contract_code,
        terminal_code=scenario.terminal_code,
        type_number=scenario.type_number,
        peers=scenario.required_peers,
    )


def _packet_payloads(
    finding: Mapping[str, Any],
    observations: ObservationSet,
    contract: DarkFactoryContract,
) -> dict[str, bytes]:
    detector_run = {
        "channels_consumed": [
            entry.channel for entry in observations.channels
        ],
        "channels_withheld": sorted(observations.withheld),
        "detector": contract.detector_name,
        "detector_version": contract.detector_version,
        "mode": "read_only",
        "scenario": observations.scenario.scenario,
        "status": "completed",
    }
    observation_index = {
        "observations": [
            entry.as_finding_entry() for entry in observations.channels
        ],
        "lineage": {
            "batch_id": observations.lineage.batch_id,
            "contract_code": observations.lineage.contract_code,
            "contract_version": observations.lineage.contract_version,
            "layout_version": observations.lineage.layout_version,
            "manifest_sha256": f"sha256:{observations.lineage.manifest_sha256}",
            "raw_sha256": f"sha256:{observations.lineage.raw_sha256}",
            "type_number": observations.lineage.type_number,
        },
    }
    privacy_scan = {
        "identity_binding": "enforced",
        "layers": ["closed-schema", "field-allowlist", "restricted-corpus"],
        "restricted_values_emitted": 0,
        "status": "clean",
    }
    return {
        "finding.json": serialize(finding),
        "detector-run.json": serialize(detector_run),
        "observation-index.json": serialize(observation_index),
        "privacy-scan.json": serialize(privacy_scan),
    }


def publish(
    finding: Mapping[str, Any],
    observations: ObservationSet,
    contract: DarkFactoryContract,
    *,
    evidence_root: Path,
) -> Path:
    """Write one immutable packet atomically, refusing to overwrite a different one."""

    root = evidence_root.resolve()
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    final = root / observations.lineage.batch_id
    payloads = _packet_payloads(finding, observations, contract)

    if final.exists():
        existing = final / "finding.json"
        if not existing.is_file():
            raise EvidenceConflictError(
                "an incomplete Dark Factory packet already exists for this batch"
            )
        previous = json.loads(existing.read_text(encoding="utf-8"))
        if previous.get("finding_id") != finding["finding_id"]:
            raise EvidenceConflictError(
                "a different Dark Factory finding already exists for this batch"
            )
        return final

    temporary = Path(
        tempfile.mkdtemp(prefix=f".{observations.lineage.batch_id}.", dir=root)
    )
    try:
        os.chmod(temporary, 0o700)
        for name, payload in payloads.items():
            path = temporary / name
            with path.open("xb") as stream:
                os.fchmod(stream.fileno(), 0o600)
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())
        temporary.rename(final)
    except OSError as exc:
        shutil.rmtree(temporary, ignore_errors=True)
        raise EvidenceConflictError(
            "the Dark Factory evidence packet could not be published atomically"
        ) from exc
    return final
