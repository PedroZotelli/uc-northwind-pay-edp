"""Assemble one complete, lineage-bound observation set for a batch.

This is where the Step 2 refusal rules live. Every channel is bound to the same
``(batch_id, type_number, raw_sha256, manifest_sha256)`` tuple before any
comparison runs, so the references a finding carries are load-bearing rather
than decorative.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from ..config import DetectorConfiguration, read_bytes
from ..contracts import Scenario
from ..errors import (
    ContradictoryObservationError,
    CrossBatchObservationError,
    LineageConflictError,
    ObservationMissingError,
)
from . import evidence as evidence_adapter
from . import postgres as postgres_adapter
from . import transport as transport_adapter
from .model import (
    CHANNEL_CONTRACT_ORACLE,
    CHANNEL_JAVA,
    CHANNEL_POSTGRES_CONTROL_PLANE,
    CHANNEL_POSTGRES_DIAGNOSTIC,
    CHANNEL_SOURCE_MANIFEST,
    CHANNEL_TRANSPORT,
    INDEPENDENCE_CONTRACT,
    INDEPENDENCE_DERIVED,
    INDEPENDENCE_INDEPENDENT,
    INDEPENDENCE_PERSISTED,
    INDEPENDENCE_SOURCE_DECLARATION,
    INDEPENDENCE_TRANSPORT,
    ROLE_CORRECTNESS,
    ROLE_OBSERVATION,
    ROLE_SYSTEM_OF_RECORD,
    ChannelObservation,
    ControlSet,
    Lineage,
)

# Channels the conclusiveness rule depends on. The end-to-end suite withholds
# each one in turn and asserts the attribution degrades to inconclusive.
WITHHOLDABLE_CHANNELS: tuple[str, ...] = (
    CHANNEL_SOURCE_MANIFEST,
    CHANNEL_JAVA,
    CHANNEL_POSTGRES_CONTROL_PLANE,
    CHANNEL_POSTGRES_DIAGNOSTIC,
)


@dataclass(frozen=True, slots=True)
class ObservationSet:
    """Every channel the detector consumed, already validated for lineage."""

    scenario: Scenario
    lineage: Lineage
    declared: tuple[ControlSet, ...]
    computed: tuple[ControlSet, ...]
    channels: tuple[ChannelObservation, ...]
    diagnostic_is_independent: bool
    terminal_status: str
    terminal_code: str
    postgres_business_mutation: bool
    staging_row_count: int
    operational_row_count: int
    transport: transport_adapter.TransportObservation
    peers: tuple[postgres_adapter.PeerObservation, ...]
    contract_oracle_sha256: str
    withheld: frozenset[str]

    def computed_for(self, channel: str) -> ControlSet | None:
        for control_set in self.computed:
            if control_set.channel == channel:
                return control_set
        return None

    def declared_for(self, channel: str) -> ControlSet | None:
        for control_set in self.declared:
            if control_set.channel == channel:
                return control_set
        return None


def _agree(left: Mapping[str, str], right: Mapping[str, str]) -> bool:
    """Whether two control sets agree on every control they share."""

    shared = set(left) & set(right)
    return bool(shared) and all(left[name] == right[name] for name in shared)


def collect(
    scenario: Scenario,
    *,
    configuration: DetectorConfiguration,
    evidence_root: Path,
    withhold: frozenset[str] = frozenset(),
) -> ObservationSet:
    """Read every channel read-only and refuse anything that does not cohere."""

    packet = evidence_adapter.load_packet(evidence_root, scenario.batch_id)

    file_type = packet.source_manifest.get("file_type")
    if not isinstance(file_type, dict):
        raise ObservationMissingError("source manifest has no file_type member")
    if file_type.get("number") != scenario.type_number:
        raise LineageConflictError(
            "source manifest declares a different type than the scenario"
        )
    if file_type.get("code") != scenario.contract_code:
        raise LineageConflictError(
            "source manifest declares a different contract code"
        )

    source_file = packet.source_manifest["source_file"]
    if source_file.get("sha256") != packet.raw_sha256:
        raise LineageConflictError(
            "source manifest and checksum sidecar disagree on the raw hash"
        )
    if packet.raw_intake.get("sha256") != packet.raw_sha256:
        raise LineageConflictError(
            "intake observation disagrees with the manifest on the raw hash"
        )
    if packet.raw_publication.get("sha256") != packet.raw_sha256:
        raise LineageConflictError(
            "publication observation disagrees on the raw hash"
        )
    manifest_sha256 = str(packet.raw_intake.get("manifest_sha256", ""))
    if not manifest_sha256:
        raise ObservationMissingError("intake observation has no manifest hash")

    with postgres_adapter.read_only_session(configuration) as connection:
        control_plane = postgres_adapter.observe_batch(
            connection,
            batch_id=scenario.batch_id,
            staging_relation=scenario.staging_relation,
            operational_relation=scenario.operational_relation,
            count_control=scenario.control_plane_count_control,
            net_control=scenario.control_plane_net_control,
        )
        peers = postgres_adapter.observe_peers(
            connection,
            peers=scenario.required_peers,
            reporting_relation=scenario.reporting_relation,
        )

    if control_plane.batch_id != scenario.batch_id:
        raise CrossBatchObservationError(
            "the control plane returned a different batch"
        )
    if control_plane.file_type != scenario.type_number:
        raise LineageConflictError(
            "the control plane records a different type for this batch"
        )
    if control_plane.source_sha256 != packet.raw_sha256:
        raise LineageConflictError(
            "the control plane disagrees with evidence on the raw hash"
        )
    if control_plane.source_manifest_sha256 != manifest_sha256:
        raise LineageConflictError(
            "the control plane disagrees with evidence on the manifest hash"
        )

    with transport_adapter.read_only_transport(configuration) as channel:
        transport = transport_adapter.observe_transport(
            channel,
            batch_id=scenario.batch_id,
        )

    terminal_status = str(packet.final_status.get("status", ""))
    terminal_code = str(packet.final_status.get("code", ""))
    if control_plane.status != terminal_status:
        raise ContradictoryObservationError(
            "evidence and the control plane disagree on terminal status"
        )
    if (control_plane.failure_code or "") != terminal_code:
        raise ContradictoryObservationError(
            "evidence and the control plane disagree on the terminal code"
        )
    reason_code = transport.quarantine_reason.get("code")
    if reason_code is not None and reason_code != terminal_code:
        raise ContradictoryObservationError(
            "the transport quarantine reason disagrees with the terminal code"
        )

    manifest_declared = evidence_adapter.manifest_declared(packet)
    java_declared = evidence_adapter.java_declared(packet)
    java_computed = evidence_adapter.java_computed(packet)
    diagnostic_computed = evidence_adapter.diagnostic_computed(packet)

    if not _agree(java_computed.values, diagnostic_computed.values):
        raise ContradictoryObservationError(
            "the Java and PostgreSQL diagnostic computed controls disagree"
        )
    if control_plane.computed.values and not _agree(
        java_computed.values, control_plane.computed.values
    ):
        raise ContradictoryObservationError(
            "the Java and control-plane computed controls disagree"
        )

    oracle_bytes = read_bytes(scenario.contract_oracle)
    contract_oracle_sha256 = hashlib.sha256(oracle_bytes).hexdigest()

    declared = tuple(
        control_set
        for control_set in (manifest_declared, java_declared, control_plane.declared)
        if control_set.channel not in withhold
    )
    computed = tuple(
        control_set
        for control_set in (java_computed, diagnostic_computed, control_plane.computed)
        if control_set.channel not in withhold and control_set.values
    )

    channels = tuple(
        entry
        for entry in (
            ChannelObservation(
                channel=CHANNEL_SOURCE_MANIFEST,
                role=ROLE_SYSTEM_OF_RECORD,
                independence=INDEPENDENCE_SOURCE_DECLARATION,
                reference=packet.source_manifest_reference,
            ),
            ChannelObservation(
                channel=CHANNEL_JAVA,
                role=ROLE_OBSERVATION,
                independence=INDEPENDENCE_INDEPENDENT,
                reference=packet.java_reference,
            ),
            ChannelObservation(
                channel=CHANNEL_POSTGRES_DIAGNOSTIC,
                role=ROLE_OBSERVATION,
                independence=(
                    INDEPENDENCE_INDEPENDENT
                    if packet.diagnostic_independence_is_recomputation
                    else INDEPENDENCE_DERIVED
                ),
                reference=packet.postgres_diagnostic_reference,
            ),
            ChannelObservation(
                channel=CHANNEL_POSTGRES_CONTROL_PLANE,
                role=ROLE_OBSERVATION,
                independence=INDEPENDENCE_PERSISTED,
                reference=control_plane.reference,
            ),
            ChannelObservation(
                channel=CHANNEL_TRANSPORT,
                role=ROLE_OBSERVATION,
                independence=INDEPENDENCE_TRANSPORT,
                reference=transport.reference,
            ),
            ChannelObservation(
                channel=CHANNEL_CONTRACT_ORACLE,
                role=ROLE_CORRECTNESS,
                independence=INDEPENDENCE_CONTRACT,
                reference=f"sha256:{contract_oracle_sha256}",
            ),
        )
        if entry.channel not in withhold
    )

    return ObservationSet(
        scenario=scenario,
        lineage=Lineage(
            batch_id=scenario.batch_id,
            type_number=scenario.type_number,
            raw_sha256=packet.raw_sha256,
            manifest_sha256=manifest_sha256,
            contract_code=str(file_type["code"]),
            contract_version=int(file_type["contract_version"]),
            layout_version=str(file_type["layout_version"]),
        ),
        declared=declared,
        computed=computed,
        channels=channels,
        diagnostic_is_independent=(
            packet.diagnostic_independence_is_recomputation
            and CHANNEL_POSTGRES_DIAGNOSTIC not in withhold
        ),
        terminal_status=terminal_status,
        terminal_code=terminal_code,
        postgres_business_mutation=bool(
            packet.postgres_load.get("business_state_committed", True)
        ),
        staging_row_count=control_plane.staging_row_count,
        operational_row_count=control_plane.operational_row_count,
        transport=transport,
        peers=peers,
        contract_oracle_sha256=contract_oracle_sha256,
        withheld=withhold,
    )
