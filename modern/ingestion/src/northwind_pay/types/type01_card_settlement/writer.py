"""Deterministic Type 01 Parquet schema and table construction."""

from __future__ import annotations

from typing import Sequence

import pyarrow as pa  # type: ignore[import-untyped]  # pyarrow ships no py.typed marker

from ...common.parquet import canonical_metadata
from .model import SanitizedRecord

WRITER_VERSION = "1.0.0"

# Column order matches the sanitized CSV contract exactly, so a reader can put
# the two side by side without a mapping table.
SCHEMA_FIELDS: tuple[tuple[str, pa.DataType], ...] = (
    ("batch_id", pa.string()),
    ("source_file", pa.string()),
    ("source_record_number", pa.int32()),
    ("transaction_id", pa.string()),
    ("merchant_id", pa.string()),
    ("card_token", pa.string()),
    ("card_last4", pa.string()),
    ("cpf_masked", pa.string()),
    ("transaction_ts", pa.string()),
    ("amount_brl", pa.decimal128(18, 2)),
    ("movement_code", pa.string()),
    ("authorization_code", pa.string()),
    ("nsu", pa.string()),
    ("terminal_id", pa.string()),
)


def schema(
    *,
    batch_id: str,
    raw_sha256: str,
    contract_version: int = 1,
    layout_version: str = "001",
) -> pa.Schema:
    """Return the canonical schema with immutable provenance metadata."""

    return pa.schema(
        [pa.field(name, kind, nullable=False) for name, kind in SCHEMA_FIELDS],
        metadata=canonical_metadata(
            batch_id=batch_id,
            type_number="01",
            contract_code="CRD_SETTLE01",
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
    """Build the canonical table, ordered by source record number."""

    ordered = sorted(records, key=lambda record: record.source_record_number)
    columns = {
        "batch_id": [record.batch_id for record in ordered],
        "source_file": [record.source_file for record in ordered],
        "source_record_number": [record.source_record_number for record in ordered],
        "transaction_id": [record.transaction_id for record in ordered],
        "merchant_id": [record.merchant_id for record in ordered],
        "card_token": [record.card_token for record in ordered],
        "card_last4": [record.card_last4 for record in ordered],
        "cpf_masked": [record.cpf_masked for record in ordered],
        "transaction_ts": [record.transaction_ts for record in ordered],
        "amount_brl": [record.amount_brl for record in ordered],
        "movement_code": [record.movement_code for record in ordered],
        "authorization_code": [record.authorization_code for record in ordered],
        "nsu": [record.nsu for record in ordered],
        "terminal_id": [record.terminal_id for record in ordered],
    }
    target = schema(batch_id=batch_id, raw_sha256=raw_sha256)
    return pa.Table.from_pydict(columns, schema=target)
