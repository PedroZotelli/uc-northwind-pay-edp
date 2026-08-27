"""Clean local rebuild: dlt register landing → Bronze → Silver → Gold.

DuckLake / DuckDB only. Does not read PostgreSQL. Does not start Dagster.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import duckdb

REPO = Path(__file__).resolve().parents[2]
LAKEHOUSE = REPO / "modern" / "lakehouse"
DBT = REPO / "modern" / "dbt"
DUCKDB_DIR = LAKEHOUSE / "duckdb"
DUCKDB_PATH = DUCKDB_DIR / "northwind_modern.duckdb"
DUCKLAKE_DIR = LAKEHOUSE / "ducklake"
CATALOG = DUCKLAKE_DIR / "catalog.duckdb"
DATA_PATH = DUCKLAKE_DIR / "data"
REGISTER = LAKEHOUSE / "dlt" / "register_landing.py"


def _dbt() -> str:
    return str(Path(sys.executable).with_name("dbt"))


def _run(cmd: list[str]) -> None:
    print("+", " ".join(cmd), flush=True)
    env = os.environ.copy()
    env["NWP_DUCKDB_PATH"] = str(DUCKDB_PATH)
    subprocess.run(cmd, check=True, cwd=str(REPO), env=env)


def clean() -> None:
    for path in (DUCKDB_DIR, DUCKLAKE_DIR, LAKEHOUSE / ".dlt_pipelines", DBT / "target"):
        if path.exists():
            shutil.rmtree(path)
    DUCKDB_DIR.mkdir(parents=True, exist_ok=True)
    DATA_PATH.mkdir(parents=True, exist_ok=True)


def snapshot_ducklake() -> None:
    con = duckdb.connect(str(DUCKDB_PATH))
    try:
        con.execute("INSTALL ducklake")
        con.execute("LOAD ducklake")
        con.execute(
            f"ATTACH 'ducklake:{CATALOG}' AS lake (DATA_PATH '{DATA_PATH}')"
        )
        con.execute(
            "CREATE OR REPLACE TABLE lake.bronze_type01 AS "
            "SELECT * FROM bronze.type01_card_settlement"
        )
        con.execute(
            "CREATE OR REPLACE TABLE lake.silver_type01 AS "
            "SELECT * FROM silver.type01_card_settlement"
        )
        con.execute(
            "CREATE OR REPLACE TABLE lake.gold_type01 AS "
            "SELECT * FROM gold.type01_card_settlement"
        )
        gold = con.execute(
            "SELECT batch_id, currency, applied_count, applied_net_amount, status "
            "FROM lake.gold_type01"
        ).fetchall()
        print("ducklake gold:", gold)
    finally:
        con.close()


def main() -> int:
    python = sys.executable
    dbt = _dbt()
    clean()
    _run([python, str(REGISTER)])
    _run([dbt, "run", "--project-dir", str(DBT), "--profiles-dir", str(DBT)])
    snapshot_ducklake()
    _run([dbt, "test", "--project-dir", str(DBT), "--profiles-dir", str(DBT)])
    receipt = json.loads((LAKEHOUSE / "dlt" / "register-receipt.json").read_text())
    print(json.dumps({"register": receipt, "gold": "rebuilt-from-landing"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
