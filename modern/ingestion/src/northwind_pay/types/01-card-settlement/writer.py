"""Atomic Parquet + readiness manifest under modern/landing/. Not SFTP."""

from __future__ import annotations

import hashlib
import json
import os
from decimal import Decimal
from pathlib import Path
from typing import Mapping

import pyarrow as pa
import pyarrow.parquet as pq

from model import LandingRow
from parser import MONEY_QUANTUM

LANDING_ZONE = "modern/landing/"
PARQUET_COLUMNS = (
    "batch_id",
    "source_file",
    "source_record_number",
    "transaction_id",
    "merchant_id",
    "card_token",
    "card_last4",
    "cpf_masked",
    "transaction_ts",
    "amount_brl",
    "movement_code",
    "authorization_code",
    "nsu",
    "terminal_id",
)
ARROW_SCHEMA = pa.schema(
    [
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
    ]
)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _money(value: Decimal) -> str:
    return f"{value.quantize(MONEY_QUANTUM):.2f}"


def _dump(payload: Mapping[str, object]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _table(rows: tuple[LandingRow, ...]) -> pa.Table:
    columns: dict[str, list[object]] = {name: [] for name in PARQUET_COLUMNS}
    for row in rows:
        mapping = row.as_mapping()
        for name in PARQUET_COLUMNS:
            columns[name].append(mapping[name])
    arrays = []
    for field in ARROW_SCHEMA:
        arrays.append(pa.array(columns[field.name], type=field.type))
    return pa.Table.from_arrays(arrays, schema=ARROW_SCHEMA)


def publish_landing(
    rows: tuple[LandingRow, ...],
    *,
    landing_root: Path,
    source_filename: str,
    raw_sha256: str,
    source_manifest_sha256: str,
    net_amount: Decimal,
) -> Path:
    if not rows:
        raise ValueError("refused batches must not publish Parquet")
    batch_id = rows[0].batch_id
    file_date = source_filename.split("_")[3]
    parquet_name = f"NW_CARD_SETTLEMENT_{file_date}_{batch_id}.parquet"
    dest_dir = landing_root / batch_id
    dest_dir.mkdir(parents=True, exist_ok=True)
    parquet_path = dest_dir / parquet_name
    manifest_path = dest_dir / "landing-manifest.json"
    staging = dest_dir / ".staging"
    staging.mkdir(exist_ok=True)
    staged_parquet = staging / parquet_name
    table = _table(rows)
    pq.write_table(
        table,
        staged_parquet,
        compression=None,
        use_dictionary=False,
        write_statistics=True,
        coerce_timestamps=None,
    )
    digest = sha256_file(staged_parquet)
    size_bytes = staged_parquet.stat().st_size
    manifest = {
        "batch_id": batch_id,
        "file_type": {
            "code": "CRD_SETTLE01",
            "contract_version": 1,
            "layout_version": "001",
            "number": "01",
        },
        "parquet_file": {
            "name": parquet_name,
            "row_count": len(rows),
            "sha256": digest,
            "size_bytes": size_bytes,
        },
        "schema_version": 1,
        "source_lineage": {
            "manifest_sha256": source_manifest_sha256,
            "raw_file": source_filename,
            "raw_sha256": raw_sha256,
        },
        "stage_controls": {
            "currency": "BRL",
            "net_amount": _money(net_amount),
            "row_count": len(rows),
        },
        "status": "READY",
        "zone": LANDING_ZONE,
    }
    staged_manifest = staging / "landing-manifest.json.part"
    staged_manifest.write_bytes(_dump(manifest))
    os.replace(staged_parquet, parquet_path)
    (dest_dir / f"{parquet_name}.sha256").write_text(digest + "\n", encoding="utf-8")
    os.replace(staged_manifest, manifest_path)
    try:
        staging.rmdir()
    except OSError:
        pass
    return parquet_path


def publish_finding(
    *,
    landing_root: Path,
    batch_id: str | None,
    source_filename: str,
    raw_sha256: str,
    finding: str,
    declared_net: Decimal | None,
    computed_net: Decimal | None,
) -> Path:
    dest = landing_root / "_quarantine"
    dest.mkdir(parents=True, exist_ok=True)
    identity = batch_id or "UNKNOWN"
    path = dest / f"{identity}.finding.json"
    payload = {
        "batch_id": identity,
        "computed_net_amount": None if computed_net is None else _money(computed_net),
        "declared_net_amount": None if declared_net is None else _money(declared_net),
        "finding": finding,
        "keep": None if declared_net is None else _money(declared_net),
        "parquet_produced": False,
        "quarantine_scope": "batch",
        "raw_file": source_filename,
        "raw_sha256": raw_sha256,
    }
    staging = path.with_suffix(".json.part")
    staging.write_bytes(_dump(payload))
    os.replace(staging, path)
    return path
