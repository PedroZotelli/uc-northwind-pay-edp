"""Compose admission, parsing, schema, and publication for one Type 01 batch.

The handler is the only place the four boundaries meet, and it is what both the
CLI and the Dagster asset call — which is what makes "direct and orchestrated
execution produce the same result" a property of the code rather than a hope.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ...common.money import render
from ...common.parquet import publish
from ...common.privacy import PrivacyError
from ...intake.admission import AdmissionError, AdmittedSource, admit
from . import parser, writer
from .schema import SchemaError, controls_of, sanitize

TYPE_NUMBER = "01"


@dataclass(frozen=True, slots=True)
class BatchOutcome:
    """The terminal result of one modern batch, successful or quarantined."""

    batch_id: str
    type_number: str
    status: str
    code: str | None
    stage: str
    raw_sha256: str
    parquet_sha256: str | None
    record_count: int
    controls: dict[str, Any]

    def as_evidence(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "batch_id": self.batch_id,
            "controls": self.controls,
            "raw_sha256": f"sha256:{self.raw_sha256}",
            "record_count": self.record_count,
            "stage": self.stage,
            "status": self.status,
            "type_number": self.type_number,
        }
        if self.code is not None:
            value["code"] = self.code
        if self.parquet_sha256 is not None:
            value["parquet_sha256"] = f"sha256:{self.parquet_sha256}"
        return value


def _quarantined(
    source: AdmittedSource | None,
    *,
    batch_id: str,
    code: str,
    stage: str,
    raw_sha256: str,
    controls: dict[str, Any],
) -> BatchOutcome:
    """A rejected batch produces no Parquet and no Gold. Nothing partial."""

    return BatchOutcome(
        batch_id=batch_id,
        type_number=TYPE_NUMBER,
        status="quarantined",
        code=code,
        stage=stage,
        raw_sha256=raw_sha256,
        parquet_sha256=None,
        record_count=0,
        controls=controls,
    )


def process(bundle: Path, *, landing_root: Path) -> BatchOutcome:
    """Run one batch from raw bytes to canonical Parquet, or to quarantine."""

    try:
        source = admit(bundle, expected_type=TYPE_NUMBER)
    except AdmissionError as error:
        return _quarantined(
            None,
            batch_id=bundle.name,
            code=error.code,
            stage="intake",
            raw_sha256="",
            controls={},
        )

    try:
        parsed = parser.parse(source.payload, source_filename=source.source_filename)
    except parser.ParseError as error:
        return _quarantined(
            source,
            batch_id=source.batch_id,
            code=error.code,
            stage="parse",
            raw_sha256=source.raw_sha256,
            controls={},
        )

    controls = controls_of(parsed)
    try:
        sanitized = sanitize(parsed, source_filename=source.source_filename)
    except SchemaError as error:
        # The source-owned declaration stays exactly as the source published it.
        return _quarantined(
            source,
            batch_id=source.batch_id,
            code=error.code,
            stage="validate",
            raw_sha256=source.raw_sha256,
            controls=controls.as_evidence(),
        )
    except PrivacyError:
        return _quarantined(
            source,
            batch_id=source.batch_id,
            code="PRIVACY_VIOLATION",
            stage="validate",
            raw_sha256=source.raw_sha256,
            controls=controls.as_evidence(),
        )

    parquet_name = source.source_filename.replace(".dat", ".parquet")
    table = writer.table(
        sanitized.records,
        batch_id=sanitized.batch_id,
        raw_sha256=source.raw_sha256,
    )
    result = publish(
        table,
        directory=landing_root,
        filename=parquet_name,
        manifest={
            "batch_id": sanitized.batch_id,
            "computed_detail_count": controls.computed_detail_count,
            "computed_net_amount": render(controls.computed_net_amount),
            "contract_code": source.contract_code,
            "contract_version": source.contract_version,
            "currency": "BRL",
            # The source-owned declaration is carried forward unchanged, even
            # when it is wrong, so downstream models can compare rather than
            # inherit a corrected value.
            "declared_detail_count": controls.declared_detail_count,
            "declared_net_amount": render(controls.declared_net_amount),
            "layout_version": source.layout_version,
            "parquet_file": parquet_name,
            "raw_sha256": source.raw_sha256,
            "record_count": len(sanitized.records),
            "source_file": source.source_filename,
            "source_manifest_sha256": source.manifest_sha256,
            "type_number": TYPE_NUMBER,
            "writer_version": writer.WRITER_VERSION,
        },
    )
    return BatchOutcome(
        batch_id=sanitized.batch_id,
        type_number=TYPE_NUMBER,
        status="succeeded",
        code=None,
        stage="published",
        raw_sha256=source.raw_sha256,
        parquet_sha256=result["parquet_sha256"],
        record_count=len(sanitized.records),
        controls=controls.as_evidence(),
    )
