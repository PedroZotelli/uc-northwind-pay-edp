"""Assembly of one canonical finding from observations, detection, and attribution.

The finding is inert by construction: ``approval`` and ``remediation`` are
pinned to ``not_requested`` by the schema, so nothing downstream can read an
action out of it.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from attribution.source_system import Attribution
from canonical import finding_identity
from contracts import DarkFactoryContract
from detection.control_mismatch import Detection
from errors import ContinuationUnprovenError, IsolationUnprovenError
from observations.collect import ObservationSet


def _isolation(observations: ObservationSet) -> dict[str, Any]:
    return {
        "business_row_count": observations.operational_row_count,
        "observed": (
            not observations.transport.sanitized_csv_present
            and observations.transport.raw_quarantine_present
            and not observations.postgres_business_mutation
            and observations.staging_row_count == 0
            and observations.operational_row_count == 0
        ),
        "postgres_business_mutation": observations.postgres_business_mutation,
        "quarantine_scope": "batch",
        "raw_quarantine_present": observations.transport.raw_quarantine_present,
        "sanitized_csv_present": observations.transport.sanitized_csv_present,
        "staging_row_count": observations.staging_row_count,
    }


def _continuation(observations: ObservationSet) -> dict[str, Any]:
    peers = [
        {
            "batch_id": peer.batch_id,
            "reconciliation_status": peer.reconciliation_status,
            "status": peer.status,
        }
        for peer in observations.peers
    ]
    return {
        "observed": bool(peers)
        and all(
            peer["status"] == "succeeded"
            and peer["reconciliation_status"] == "MATCHED"
            for peer in peers
        ),
        "peers": peers,
    }


def build(
    contract: DarkFactoryContract,
    observations: ObservationSet,
    detection: Detection,
    attribution: Attribution,
    *,
    detector_source_sha256: str,
    created_at: datetime | None = None,
) -> dict[str, Any]:
    """Compose the canonical finding and stamp its identity.

    Isolation and continuation are gates, not decorations: a finding that
    cannot observe both is incomplete, and an incomplete finding is worse than
    none because it still looks like evidence.
    """

    isolation = _isolation(observations)
    if not isolation["observed"]:
        raise IsolationUnprovenError(
            "batch-scoped isolation could not be observed for this batch"
        )
    continuation = _continuation(observations)
    if not continuation["observed"]:
        raise ContinuationUnprovenError(
            "a required peer batch did not reach a reconciled success"
        )

    moment = (created_at or datetime.now(timezone.utc)).astimezone(timezone.utc)
    finding: dict[str, Any] = {
        "approval": {"state": "not_requested"},
        "attribution": attribution.as_finding_entry(),
        "batch": {
            "batch_id": observations.lineage.batch_id,
            "contract_code": observations.lineage.contract_code,
            "contract_version": observations.lineage.contract_version,
            "layout_version": observations.lineage.layout_version,
            "type_number": observations.lineage.type_number,
        },
        "continuation": continuation,
        "controls": {
            "compared": [
                entry.as_finding_entry() for entry in detection.compared
            ],
            "difference_count": detection.difference_count,
        },
        "created_at": moment.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "finding_code": contract.finding_code,
        "finding_id": "",
        "finding_version": contract.finding_version,
        "isolation": isolation,
        "method": {
            "comparison": contract.detector_method,
            "detector": contract.detector_name,
            "detector_version": contract.detector_version,
        },
        "observations": [
            entry.as_finding_entry() for entry in observations.channels
        ],
        "references": {
            "contract_oracle_sha256": f"sha256:{observations.contract_oracle_sha256}",
            "detector_source_sha256": detector_source_sha256,
            "raw_sha256": f"sha256:{observations.lineage.raw_sha256}",
            "source_manifest_sha256": (
                f"sha256:{observations.lineage.manifest_sha256}"
            ),
        },
        "remediation": {"state": "not_requested"},
        "scenario": observations.scenario.scenario,
        "schema_version": contract.schema_version,
        "terminal": {
            "code": observations.terminal_code,
            "stage": observations.scenario.terminal_stage,
            "status": observations.terminal_status,
        },
    }
    finding["finding_id"] = finding_identity(finding)
    return finding
