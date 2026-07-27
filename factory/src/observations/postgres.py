"""Read-only adapter over the legacy PostgreSQL control plane.

Every session issues ``SET TRANSACTION READ ONLY`` before its first statement,
so a write is refused by the server rather than by this client. The adapter
connects as the existing non-superuser application role; it creates nothing and
requires no migration. See DR-005.
"""

from __future__ import annotations

import hashlib
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Iterator, Mapping, Sequence

import psycopg

from canonical import encode
from detector_config import DetectorConfiguration
from errors import (
    ObservationMissingError,
    RuntimeUnavailableError,
)
from .model import CHANNEL_POSTGRES_CONTROL_PLANE, ControlSet, normalize_control

# Relation names come from the frozen Dark Factory scenario contract, never
# from user input, and are validated against this shape before interpolation.
_RELATION_SHAPE = "abcdefghijklmnopqrstuvwxyz_."


def _safe_relation(relation: str) -> str:
    if not relation or any(character not in _RELATION_SHAPE for character in relation):
        raise ObservationMissingError("relation name is not a bare identifier")
    if relation.count(".") != 1:
        raise ObservationMissingError("relation name must be schema-qualified")
    return relation


@contextmanager
def read_only_session(
    configuration: DetectorConfiguration,
) -> Iterator[psycopg.Connection[Any]]:
    """Yield one connection whose transaction the server marks read only."""

    try:
        with psycopg.connect(configuration.postgres_dsn) as connection:
            connection.read_only = True
            with connection.cursor() as cursor:
                cursor.execute("SET TRANSACTION READ ONLY")
            yield connection
    except psycopg.Error as exc:
        raise RuntimeUnavailableError(
            "the legacy PostgreSQL runtime is not reachable read-only"
        ) from exc


def _fetch_one(
    connection: psycopg.Connection[Any],
    statement: str,
    parameters: Sequence[Any],
) -> tuple[Any, ...] | None:
    with connection.cursor() as cursor:
        cursor.execute(statement, parameters)
        return cursor.fetchone()


@dataclass(frozen=True, slots=True)
class ControlPlaneObservation:
    """What the loader component durably recorded about one batch."""

    batch_id: str
    file_type: str
    status: str
    failure_code: str | None
    source_sha256: str
    source_manifest_sha256: str
    declared: ControlSet
    computed: ControlSet
    staging_row_count: int
    operational_row_count: int
    reject_count: int
    reference: str


@dataclass(frozen=True, slots=True)
class PeerObservation:
    """One peer batch's terminal and reconciliation state."""

    batch_id: str
    status: str
    reconciliation_status: str


def observe_batch(
    connection: psycopg.Connection[Any],
    *,
    batch_id: str,
    staging_relation: str,
    operational_relation: str,
    count_control: str,
    net_control: str,
) -> ControlPlaneObservation:
    """Read the persisted control-plane record for one batch."""

    batch = _fetch_one(
        connection,
        """
        SELECT batch_id, file_type, status, failure_code,
               source_sha256, source_manifest_sha256, source_controls
          FROM control.batches
         WHERE batch_id = %s
        """,
        (batch_id,),
    )
    if batch is None:
        raise ObservationMissingError(
            f"the control plane holds no batch record for {batch_id}"
        )
    reject = _fetch_one(
        connection,
        """
        SELECT count(*), min(computed_count), min(computed_net_amount),
               min(declared_count), min(declared_net_amount)
          FROM control.rejects
         WHERE batch_id = %s
        """,
        (batch_id,),
    )
    reject_count = int(reject[0]) if reject is not None else 0

    staging = _fetch_one(
        connection,
        f"SELECT count(*) FROM {_safe_relation(staging_relation)} WHERE batch_id = %s",
        (batch_id,),
    )
    operational = _fetch_one(
        connection,
        f"SELECT count(*) FROM {_safe_relation(operational_relation)} WHERE batch_id = %s",
        (batch_id,),
    )

    declared_controls: dict[str, str] = {}
    source_controls = batch[6]
    if isinstance(source_controls, dict):
        for key, value in source_controls.items():
            if key == "currency":
                continue
            try:
                declared_controls[key] = normalize_control(value)
            except ValueError as exc:
                raise ObservationMissingError(
                    f"persisted source control {key} is not canonical"
                ) from exc

    computed_controls: dict[str, str] = {}
    if reject is not None and reject_count:
        if reject[1] is not None:
            computed_controls[count_control] = normalize_control(int(reject[1]))
        if reject[2] is not None:
            computed_controls[net_control] = format(reject[2], ".2f")

    projection = {
        "batch_id": batch[0],
        "computed": computed_controls,
        "declared": declared_controls,
        "failure_code": batch[3],
        "file_type": batch[1],
        "reject_count": reject_count,
        "status": batch[2],
    }
    return ControlPlaneObservation(
        batch_id=str(batch[0]),
        file_type=str(batch[1]),
        status=str(batch[2]),
        failure_code=None if batch[3] is None else str(batch[3]),
        source_sha256=str(batch[4]),
        source_manifest_sha256=str(batch[5]),
        declared=ControlSet.of(CHANNEL_POSTGRES_CONTROL_PLANE, declared_controls),
        computed=ControlSet.of(CHANNEL_POSTGRES_CONTROL_PLANE, computed_controls),
        staging_row_count=int(staging[0]) if staging is not None else 0,
        operational_row_count=int(operational[0]) if operational is not None else 0,
        reject_count=reject_count,
        reference=(
            "sha256:"
            + hashlib.sha256(encode(projection)).hexdigest()
        ),
    )


def observe_peers(
    connection: psycopg.Connection[Any],
    *,
    peers: Sequence[str],
    reporting_relation: str,
) -> tuple[PeerObservation, ...]:
    """Read each required peer batch's terminal and reconciliation state."""

    observed: list[PeerObservation] = []
    for batch_id in peers:
        batch = _fetch_one(
            connection,
            "SELECT status FROM control.batches WHERE batch_id = %s",
            (batch_id,),
        )
        if batch is None:
            raise ObservationMissingError(
                f"the control plane holds no batch record for peer {batch_id}"
            )
        report = _fetch_one(
            connection,
            f"SELECT status FROM {_safe_relation(reporting_relation)} "
            "WHERE batch_id = %s",
            (batch_id,),
        )
        observed.append(
            PeerObservation(
                batch_id=batch_id,
                status=str(batch[0]),
                reconciliation_status=(
                    "ABSENT" if report is None else str(report[0])
                ),
            )
        )
    return tuple(observed)


def control_plane_entry(observation: ControlPlaneObservation) -> Mapping[str, str]:
    """Return the finding observation entry for the control plane channel."""

    return {"reference": observation.reference}
