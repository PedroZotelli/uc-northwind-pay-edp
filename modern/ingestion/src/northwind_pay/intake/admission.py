"""Source admission: identity, checksum, readiness, and replay.

Modern reads the same approved raw bytes and source manifest legacy reads. It
never reads legacy CSV, legacy PostgreSQL, or legacy evidence — those are
comparison observations, not inputs.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


class AdmissionError(ValueError):
    """The source bundle is not admissible."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True, slots=True)
class AdmittedSource:
    """One validated, immutable source bundle."""

    batch_id: str
    type_number: str
    contract_code: str
    contract_version: int
    layout_version: str
    source_filename: str
    raw_path: Path
    raw_sha256: str
    manifest_sha256: str
    declared_controls: Mapping[str, Any]
    payload: bytes


def admit(bundle: Path, *, expected_type: str) -> AdmittedSource:
    """Validate one raw bundle against its own manifest, reading only."""

    bundle = bundle.resolve()
    manifest_path = bundle / "source-manifest.json"
    if not manifest_path.is_file():
        raise AdmissionError("MISSING_MANIFEST", "the bundle has no source manifest")
    manifest_bytes = manifest_path.read_bytes()
    try:
        manifest = json.loads(manifest_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AdmissionError("INVALID_MANIFEST", "the source manifest is not JSON") from exc

    file_type = manifest.get("file_type")
    source_file = manifest.get("source_file")
    if not isinstance(file_type, dict) or not isinstance(source_file, dict):
        raise AdmissionError("INVALID_MANIFEST", "the source manifest is incomplete")
    if file_type.get("number") != expected_type:
        raise AdmissionError(
            "TYPE_MISMATCH", "the manifest declares a different file type"
        )

    filename = str(source_file.get("name", ""))
    raw_path = bundle / filename
    if not filename or not raw_path.is_file():
        raise AdmissionError("MISSING_RAW_FILE", "the declared raw file is absent")

    payload = raw_path.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != source_file.get("sha256"):
        raise AdmissionError(
            "CHECKSUM_MISMATCH", "the raw bytes do not match the declared checksum"
        )
    if len(payload) != source_file.get("size_bytes"):
        raise AdmissionError(
            "SIZE_MISMATCH", "the raw bytes do not match the declared size"
        )

    sidecar = bundle / f"{filename}.sha256"
    if sidecar.is_file():
        recorded = sidecar.read_text(encoding="ascii").split()
        if not recorded or recorded[0] != digest:
            raise AdmissionError(
                "CHECKSUM_MISMATCH", "the checksum sidecar disagrees with the bytes"
            )

    return AdmittedSource(
        batch_id=str(manifest["batch_id"]),
        type_number=str(file_type["number"]),
        contract_code=str(file_type["code"]),
        contract_version=int(file_type["contract_version"]),
        layout_version=str(file_type["layout_version"]),
        source_filename=filename,
        raw_path=raw_path,
        raw_sha256=digest,
        manifest_sha256=hashlib.sha256(manifest_bytes).hexdigest(),
        declared_controls=dict(manifest.get("source_controls", {})),
        payload=payload,
    )
