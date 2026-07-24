"""Deterministic Type 03 Parquet schema and table construction."""

from __future__ import annotations

from typing import Sequence

import pyarrow as pa  # type: ignore[import-untyped]  # pyarrow ships no py.typed marker

from ...common.parquet import canonical_metadata
from .model import SanitizedRecord

WRITER_VERSION = "1.0.0"

SCHEMA_FIELDS: tuple[tuple[str, pa.DataType], ...] = (
    ("batch_id", pa.string()),
    ("source_file", pa.string()),
    ("source_record_number_a", pa.int32()),
    ("source_record_number_b", pa.int32()),
    ("lot_number", pa.string()),
    ("sequence", pa.string()),
    ("settlement_id", pa.string()),
    ("payment_reference_token", pa.string()),
    ("payment_reference_last4", pa.string()),
    ("beneficiary_token", pa.string()),
    ("beneficiary_tax_id_type", pa.string()),
    ("beneficiary_tax_id_masked", pa.string()),
    ("bank_account_token", pa.string()),
    ("bank_account_last4", pa.string()),
    ("due_date", pa.string()),
    ("payment_date", pa.string()),
    ("face_amount_brl", pa.decimal128(18, 2)),
    ("discount_brl", pa.decimal128(18, 2)),
    ("fee_brl", pa.decimal128(18, 2)),
    ("net_amount_brl", pa.decimal128(18, 2)),
    ("status", pa.string()),
    ("bank_reference", pa.string()),
    ("client_reference", pa.string()),
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
            type_number="03",
            contract_code="PAYSLIPSET03",
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
    ordered = sorted(records, key=lambda record: record.source_record_number_a)
    columns = {
        name: [getattr(record, name) for record in ordered]
        for name, _ in SCHEMA_FIELDS
    }
    return pa.Table.from_pydict(
        columns, schema=schema(batch_id=batch_id, raw_sha256=raw_sha256)
    )
