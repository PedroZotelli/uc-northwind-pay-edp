"""dlt registers modern/landing/ Parquet only. Does not parse raw. Does not tokenize."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import dlt
import duckdb
import pyarrow.parquet as pq

REPO = Path(__file__).resolve().parents[3]
LANDING = REPO / "modern" / "landing"
LAKEHOUSE = REPO / "modern" / "lakehouse"
DUCKDB_PATH = LAKEHOUSE / "duckdb" / "northwind_modern.duckdb"
RECEIPT = LAKEHOUSE / "dlt" / "register-receipt.json"

FORBIDDEN_RAW_SUFFIXES = (".dat", ".rem", ".txt")


def landing_parquet_files() -> list[Path]:
    if not LANDING.is_dir():
        return []
    files = []
    for path in sorted(LANDING.glob("B*/*.parquet")):
        if path.parent.name.startswith("_"):
            continue
        files.append(path)
    return files


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dlt.resource(name="registered_landing", write_disposition="replace")
def registered_landing():
    files = landing_parquet_files()
    if not files:
        return
    for path in files:
        table = pq.read_table(path)
        yield {
            "batch_id": path.parent.name,
            "parquet_name": path.name,
            "parquet_path": str(path.resolve()),
            "row_count": int(table.num_rows),
            "sha256": _sha256(path),
        }


def _refuse_raw_inputs() -> None:
    for path in LANDING.rglob("*") if LANDING.is_dir() else []:
        if path.suffix.lower() in FORBIDDEN_RAW_SUFFIXES:
            raise RuntimeError(f"dlt must not register raw {path}")


def register() -> dict[str, object]:
    _refuse_raw_inputs()
    files = landing_parquet_files()
    DUCKDB_PATH.parent.mkdir(parents=True, exist_ok=True)
    pipeline = dlt.pipeline(
        pipeline_name="type01_register",
        destination=dlt.destinations.duckdb(str(DUCKDB_PATH)),
        dataset_name="dlt_register",
        pipelines_dir=str(LAKEHOUSE / ".dlt_pipelines"),
    )
    if files:
        info = pipeline.run(registered_landing())
        load_ids = [pkg.load_id for pkg in info.load_packages]
    else:
        load_ids = []
    con = duckdb.connect(str(DUCKDB_PATH))
    con.execute("CREATE SCHEMA IF NOT EXISTS landing")
    if files:
        listed = ", ".join("'" + str(p.resolve()) + "'" for p in files)
        con.execute(
            "CREATE OR REPLACE VIEW landing.type01_card_settlement AS "
            f"SELECT * FROM read_parquet([{listed}])"
        )
    else:
        con.execute("DROP VIEW IF EXISTS landing.type01_card_settlement")
    con.close()
    skipped = []
    quarantine = LANDING / "_quarantine"
    if quarantine.is_dir():
        for finding in sorted(quarantine.glob("*.finding.json")):
            skipped.append(finding.name.removesuffix(".finding.json"))
    receipt = {
        "role": "register-landing-only",
        "registered_batches": [p.parent.name for p in files],
        "registered_parquet": [str(p.relative_to(REPO)) for p in files],
        "skipped_zero_parquet": skipped,
        "dlt_load_ids": load_ids,
        "reparse_raw": False,
        "tokenize_pan": False,
    }
    RECEIPT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return receipt


def main() -> int:
    receipt = register()
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
