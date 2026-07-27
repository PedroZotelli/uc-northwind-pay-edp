"""In-memory observation factories so unit tests never need a live runtime."""

from __future__ import annotations

from typing import Mapping, Sequence

import contracts as contract_loader
from observations.collect import ObservationSet
from observations.model import (
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
from observations.postgres import PeerObservation
from observations.transport import TransportObservation

DIGEST = "sha256:" + "a" * 64

DECLARED = {"detail_count": "2", "net_amount": "173.44"}
COMPUTED = {"detail_count": "2", "net_amount": "173.45"}


def transport(
    *,
    raw_zones: Sequence[str] = ("raw/quarantine",),
    csv_zones: Sequence[str] = (),
) -> TransportObservation:
    return TransportObservation(
        batch_id="B202607230000004",
        raw_zones=tuple(raw_zones),
        csv_zones=tuple(csv_zones),
        quarantine_reason={"code": "SOURCE_CONTROL_TOTAL_MISMATCH"},
        reference=DIGEST,
    )


def peers(status: str = "succeeded", report: str = "MATCHED") -> tuple[PeerObservation, ...]:
    return (
        PeerObservation("B202402290000001", status, report),
        PeerObservation("B202607230000002", status, report),
    )


def observation_set(
    *,
    declared: Mapping[str, Mapping[str, str]] | None = None,
    computed: Mapping[str, Mapping[str, str]] | None = None,
    diagnostic_independent: bool = True,
    withheld: frozenset[str] = frozenset(),
    staging_rows: int = 0,
    operational_rows: int = 0,
    business_mutation: bool = False,
    terminal_status: str = "quarantined",
    terminal_code: str = "SOURCE_CONTROL_TOTAL_MISMATCH",
    transport_observation: TransportObservation | None = None,
    peer_observations: tuple[PeerObservation, ...] | None = None,
) -> ObservationSet:
    """Build a complete, conclusive Type 01 observation set, then vary it."""

    declared_map = declared if declared is not None else {
        CHANNEL_SOURCE_MANIFEST: DECLARED,
        CHANNEL_JAVA: DECLARED,
        CHANNEL_POSTGRES_CONTROL_PLANE: DECLARED,
    }
    computed_map = computed if computed is not None else {
        CHANNEL_JAVA: COMPUTED,
        CHANNEL_POSTGRES_DIAGNOSTIC: COMPUTED,
        CHANNEL_POSTGRES_CONTROL_PLANE: COMPUTED,
    }
    channels = tuple(
        entry
        for entry in (
            ChannelObservation(
                CHANNEL_SOURCE_MANIFEST,
                ROLE_SYSTEM_OF_RECORD,
                INDEPENDENCE_SOURCE_DECLARATION,
                DIGEST,
            ),
            ChannelObservation(
                CHANNEL_JAVA, ROLE_OBSERVATION, INDEPENDENCE_INDEPENDENT, DIGEST
            ),
            ChannelObservation(
                CHANNEL_POSTGRES_DIAGNOSTIC,
                ROLE_OBSERVATION,
                INDEPENDENCE_INDEPENDENT
                if diagnostic_independent
                else INDEPENDENCE_DERIVED,
                DIGEST,
            ),
            ChannelObservation(
                CHANNEL_POSTGRES_CONTROL_PLANE,
                ROLE_OBSERVATION,
                INDEPENDENCE_PERSISTED,
                DIGEST,
            ),
            ChannelObservation(
                CHANNEL_TRANSPORT,
                ROLE_OBSERVATION,
                INDEPENDENCE_TRANSPORT,
                DIGEST,
            ),
            ChannelObservation(
                CHANNEL_CONTRACT_ORACLE,
                ROLE_CORRECTNESS,
                INDEPENDENCE_CONTRACT,
                DIGEST,
            ),
        )
        if entry.channel not in withheld
    )
    return ObservationSet(
        scenario=contract_loader.load().scenarios["DF-SOURCE-001"],
        lineage=Lineage(
            batch_id="B202607230000004",
            type_number="01",
            raw_sha256="b" * 64,
            manifest_sha256="c" * 64,
            contract_code="CRD_SETTLE01",
            contract_version=1,
            layout_version="001",
        ),
        declared=tuple(
            ControlSet.of(channel, values)
            for channel, values in declared_map.items()
            if channel not in withheld
        ),
        computed=tuple(
            ControlSet.of(channel, values)
            for channel, values in computed_map.items()
            if channel not in withheld
        ),
        channels=channels,
        diagnostic_is_independent=(
            diagnostic_independent
            and CHANNEL_POSTGRES_DIAGNOSTIC not in withheld
        ),
        terminal_status=terminal_status,
        terminal_code=terminal_code,
        postgres_business_mutation=business_mutation,
        staging_row_count=staging_rows,
        operational_row_count=operational_rows,
        transport=transport_observation or transport(),
        peers=peer_observations if peer_observations is not None else peers(),
        contract_oracle_sha256="d" * 64,
        withheld=withheld,
    )
