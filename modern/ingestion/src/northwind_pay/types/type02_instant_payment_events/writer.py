"""Deterministic Type 02 Parquet schema and table construction."""

from __future__ import annotations

from typing import Sequence

import pyarrow as pa  # type: ignore[import-untyped]  # pyarrow ships no py.typed marker

from ...common.parquet import canonical_metadata
from .model import SanitizedRecord

WRITER_VERSION = "1.0.0"

SCHEMA_FIELDS: tuple[tuple[str, pa.DataType], ...] = (
    ("batch_id", pa.string()),
    ("source_file", pa.string()),
    ("source_record_number", pa.int32()),
    ("end_to_end_id", pa.string()),
    ("transaction_id", pa.string()),
    ("payer_document_token", pa.string()),
    ("payer_document_masked", pa.string()),
    ("payee_document_token", pa.string()),
    ("payee_document_masked", pa.string()),
    ("event_timestamp", pa.string()),
    ("amount_brl", pa.decimal128(18, 2)),
    ("direction", pa.string()),
    ("status", pa.string()),
    ("return_code", pa.string()),
    ("description", pa.string()),
)


def schema(
    *,
    batch_id: str,
    raw_sha256: str,
    contract_version: int = 1,
    layout_version: str = "001",
) -> pa.Schema:
    return pa.schema(
        [pa.field(name, kind, nullable=False) for name, kind in SCHEMA_FIELDS],
        metadata=canonical_metadata(
            batch_id=batch_id,
            type_number="02",
            contract_code="PIX_EVENTS01",
            contract_version=contract_version,
            layout_version=layout_version,
            raw_sha256=raw_sha256,
            writer_version=WRITER_VERSION,
        ),
    )


def table(
    records: Sequence[SanitizedRecord],
    *,
    batch_id: str,
    raw_sha256: str,
) -> pa.Table:
    ordered = sorted(records, key=lambda record: record.source_record_number)
    columns = {
        name: [getattr(record, name) for record in ordered]
        for name, _ in SCHEMA_FIELDS
    }
    return pa.Table.from_pydict(
        columns, schema=schema(batch_id=batch_id, raw_sha256=raw_sha256)
    )
