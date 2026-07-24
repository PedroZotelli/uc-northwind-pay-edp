"""Read-only adapter over one immutable legacy evidence packet.

Opens files for reading and nothing else. The packet is the legacy runtime's
own record of what happened; this module never writes to it, never repairs it,
and refuses rather than filling a gap.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

from ..errors import (
    AmbiguousObservationError,
    CrossBatchObservationError,
    ObservationMissingError,
)
from .model import (
    CHANNEL_JAVA,
    CHANNEL_POSTGRES_DIAGNOSTIC,
    CHANNEL_SOURCE_MANIFEST,
    ControlSet,
    normalize_control,
)

DECLARED_PREFIX = "declared_"
COMPUTED_PREFIX = "computed_"


def _read_bytes(path: Path) -> bytes:
    """The single read primitive for this package. There is no write twin."""

    try:
        with path.open("rb") as stream:
            return stream.read()
    except OSError as exc:
        raise ObservationMissingError(
            f"evidence artifact is unreadable: {path.name}"
        ) from exc


def _read_json(path: Path) -> tuple[Mapping[str, Any], str]:
    payload = _read_bytes(path)
    try:
        document = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ObservationMissingError(
            f"evidence artifact is not valid JSON: {path.name}"
        ) from exc
    if not isinstance(document, dict):
        raise ObservationMissingError(
            f"evidence artifact is not a JSON object: {path.name}"
        )
    return document, f"sha256:{hashlib.sha256(payload).hexdigest()}"


@dataclass(frozen=True, slots=True)
class EvidencePacket:
    """One legacy evidence packet, read once and frozen."""

    batch_id: str
    directory: Path
    source_manifest: Mapping[str, Any]
    source_manifest_reference: str
    source_manifest_sha256: str
    java_run: Mapping[str, Any]
    java_reference: str
    postgres_diagnostic: Mapping[str, Any]
    postgres_diagnostic_reference: str
    postgres_load: Mapping[str, Any]
    final_status: Mapping[str, Any]
    raw_intake: Mapping[str, Any]
    raw_publication: Mapping[str, Any]
    expected_diff: Mapping[str, Any]
    raw_sha256: str
    raw_filename: str

    @property
    def diagnostic_independence_is_recomputation(self) -> bool:
        """Whether the PostgreSQL diagnostic recomputed rather than restated.

        Read from the artifact's own ``mode`` member so the classification comes
        from the data, not from a table maintained by hand. Type 01 publishes
        ``read_only`` (an independent SQL aggregation); Types 02-05 publish
        ``source-parser-observation`` (a projection of the Java result).
        """

        return self.postgres_diagnostic.get("mode") == "read_only"


def _require_batch(document: Mapping[str, Any], batch_id: str, name: str) -> None:
    observed = document.get("batch_id")
    if observed is not None and observed != batch_id:
        raise CrossBatchObservationError(
            f"{name} names a different batch than requested"
        )


def load_packet(evidence_root: Path, batch_id: str) -> EvidencePacket:
    """Load the one evidence packet for a batch, refusing anything ambiguous."""

    root = evidence_root.resolve()
    candidates = sorted(
        path
        for path in root.glob(f"*{batch_id}*")
        if path.is_dir()
    )
    if not candidates:
        raise ObservationMissingError(
            f"no legacy evidence packet exists for batch {batch_id}"
        )
    if len(candidates) > 1:
        raise AmbiguousObservationError(
            f"more than one evidence packet matches batch {batch_id}"
        )
    directory = candidates[0]
    if directory.name != batch_id:
        raise CrossBatchObservationError(
            "evidence packet directory does not match the requested batch"
        )

    source_manifest, manifest_reference = _read_json(
        directory / "source-manifest.json"
    )
    java_run, java_reference = _read_json(directory / "java-run.json")
    postgres_diagnostic, diagnostic_reference = _read_json(
        directory / "postgres-diagnostic.json"
    )
    postgres_load, _ = _read_json(directory / "postgres-load.json")
    final_status, _ = _read_json(directory / "final-status.json")
    raw_intake, _ = _read_json(directory / "raw-intake.json")
    raw_publication, _ = _read_json(directory / "raw-publication.json")
    expected_diff, _ = _read_json(directory / "expected-diff.json")

    for name, document in (
        ("source manifest", source_manifest),
        ("Java run", java_run),
        ("final status", final_status),
        ("raw intake", raw_intake),
        ("raw publication", raw_publication),
    ):
        _require_batch(document, batch_id, name)

    checksum_line = _read_bytes(directory / "raw-file.sha256").decode("ascii")
    parts = checksum_line.split()
    if len(parts) != 2:
        raise ObservationMissingError("raw checksum sidecar is malformed")
    raw_sha256, raw_filename = parts[0], parts[1]

    source_file = source_manifest.get("source_file")
    if not isinstance(source_file, dict):
        raise ObservationMissingError("source manifest has no source_file member")

    return EvidencePacket(
        batch_id=batch_id,
        directory=directory,
        source_manifest=MappingProxyType(dict(source_manifest)),
        source_manifest_reference=manifest_reference,
        source_manifest_sha256=manifest_reference.removeprefix("sha256:"),
        java_run=MappingProxyType(dict(java_run)),
        java_reference=java_reference,
        postgres_diagnostic=MappingProxyType(dict(postgres_diagnostic)),
        postgres_diagnostic_reference=diagnostic_reference,
        postgres_load=MappingProxyType(dict(postgres_load)),
        final_status=MappingProxyType(dict(final_status)),
        raw_intake=MappingProxyType(dict(raw_intake)),
        raw_publication=MappingProxyType(dict(raw_publication)),
        expected_diff=MappingProxyType(dict(expected_diff)),
        raw_sha256=raw_sha256,
        raw_filename=raw_filename,
    )


def _paired_controls(
    document: Mapping[str, Any],
    prefix: str,
    partner_prefix: str,
) -> dict[str, str]:
    """Extract control values that exist under both prefixes.

    Data-driven on purpose: the control names differ per type, so pairing
    ``declared_*`` with ``computed_*`` keeps one comparison for all five types
    without a hand-maintained per-type field list. A control reported on only
    one side has no counterpart to compare and is therefore not a control pair.
    """

    values: dict[str, str] = {}
    for key, value in document.items():
        if not key.startswith(prefix) or value is None:
            continue
        name = key[len(prefix) :]
        if f"{partner_prefix}{name}" not in document:
            continue
        if document[f"{partner_prefix}{name}"] is None:
            continue
        try:
            values[name] = normalize_control(value)
        except ValueError as exc:
            raise ObservationMissingError(
                f"control {name} is not a canonical count or money value"
            ) from exc
    return values


def java_declared(packet: EvidencePacket) -> ControlSet:
    """Controls the processor decoded from the raw file's own trailer."""

    return ControlSet.of(
        CHANNEL_JAVA,
        _paired_controls(packet.java_run, DECLARED_PREFIX, COMPUTED_PREFIX),
    )


def java_computed(packet: EvidencePacket) -> ControlSet:
    """Controls the processor computed independently from the raw records."""

    return ControlSet.of(
        CHANNEL_JAVA,
        _paired_controls(packet.java_run, COMPUTED_PREFIX, DECLARED_PREFIX),
    )


def diagnostic_computed(packet: EvidencePacket) -> ControlSet:
    """Controls reported by the PostgreSQL diagnostic artifact."""

    document = packet.postgres_diagnostic
    values: dict[str, str] = {}
    for key, value in document.items():
        if not key.startswith(COMPUTED_PREFIX) or value is None:
            continue
        try:
            values[key[len(COMPUTED_PREFIX) :]] = normalize_control(value)
        except ValueError as exc:
            raise ObservationMissingError(
                "PostgreSQL diagnostic control is not canonical"
            ) from exc
    return ControlSet.of(CHANNEL_POSTGRES_DIAGNOSTIC, values)


def manifest_declared(packet: EvidencePacket) -> ControlSet:
    """The source system's own declaration, as published in its manifest."""

    controls = packet.source_manifest.get("source_controls")
    if not isinstance(controls, dict):
        raise ObservationMissingError("source manifest has no source_controls")
    values: dict[str, str] = {}
    for key, value in controls.items():
        if key == "currency":
            continue
        try:
            values[key] = normalize_control(value)
        except ValueError as exc:
            raise ObservationMissingError(
                f"source-declared control {key} is not canonical"
            ) from exc
    return ControlSet.of(CHANNEL_SOURCE_MANIFEST, values)
