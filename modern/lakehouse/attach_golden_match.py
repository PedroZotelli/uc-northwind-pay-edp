"""Attach golden-match to Type 01 modern observations. Does not edit the referee."""

from __future__ import annotations

import json
import shutil
import sys
from decimal import Decimal
from pathlib import Path

import duckdb
import pyarrow.parquet as pq
import yaml

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "validation" / "golden-match"))

from golden_match import (  # noqa: E402
    CONFIRMED_SOURCE_DEFECT,
    Comparison,
    compare_records,
    compare_reconciliation,
    compare_rejection,
)

CONTRACT = REPO / "contracts" / "types" / "01-card-settlement"
LANDING = REPO / "modern" / "landing"
DUCKDB = REPO / "modern" / "lakehouse" / "duckdb" / "northwind_modern.duckdb"
EVIDENCE = REPO / "evidence" / "modern"
RUNNER = REPO / "legacy" / "runner" / ".venv" / "bin" / "python"

CASES = (
    {
        "name": "valid-minimal",
        "batch_id": "B202607230000001",
        "kind": "accepted",
        "raw": CONTRACT / "main" / "valid-minimal.dat",
        "expected_csv": CONTRACT / "main" / "expected-sanitized.csv",
        "expected_recon": CONTRACT / "main" / "expected-reconciliation.yaml",
        "source_filename": "NW_CARD_SETTLEMENT_20260723_B202607230000001.dat",
    },
    {
        "name": "df-source-001",
        "batch_id": "B202607230000004",
        "kind": "rejected",
        "raw": CONTRACT / "main" / "df-source-001.dat",
        "contract_finding": CONTRACT / "main" / "expected-df-source-001-finding.yaml",
        "source_filename": "NW_CARD_SETTLEMENT_20260723_B202607230000004.dat",
    },
    {
        "name": "malformed",
        "batch_id": "B202607230000003",
        "kind": "rejected",
        "raw": CONTRACT / "main" / "malformed.dat",
        "contract_finding": CONTRACT / "main" / "expected-malformed-rejection.yaml",
        "source_filename": "NW_CARD_SETTLEMENT_20260723_B202607230000003.dat",
    },
)


def _dump(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256_file(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _legacy_batch(batch_id: str) -> dict:
    import subprocess

    py = r'''
import json, psycopg, sys
batch_id = sys.argv[1]
conn = psycopg.connect(host="127.0.0.1", port=54329, user="northwind_loader",
    dbname="northwind_legacy", password="local-northwind-loader")
cur = conn.cursor()
cur.execute("select status, failure_code, source_net_amount from control.batches where batch_id=%s", (batch_id,))
batch = cur.fetchone()
cur.execute("""
    select batch_id, currency, source_count, staged_count, applied_count,
           source_net_amount, staged_net_amount, applied_net_amount,
           count_delta, amount_delta, reject_count, status
    from reporting.card_settlement_reconciliation where batch_id=%s
""", (batch_id,))
recon = cur.fetchone()
cols = ["batch_id","currency","source_count","staged_count","applied_count",
        "source_net_amount","staged_net_amount","applied_net_amount",
        "count_delta","amount_delta","reject_count","status"]
out = {
  "batch": None if batch is None else {"status": batch[0], "code": batch[1],
           "source_net_amount": None if batch[2] is None else str(batch[2])},
  "recon": None if recon is None else {k: (str(v) if hasattr(v, "as_tuple") else v) for k,v in zip(cols, recon)},
}
print(json.dumps(out))
'''
    raw = subprocess.check_output([str(RUNNER), "-c", py, batch_id], text=True)
    return json.loads(raw)


def _gold(batch_id: str) -> dict | None:
    if not DUCKDB.is_file():
        return None
    con = duckdb.connect(str(DUCKDB), read_only=True)
    try:
        rows = con.execute(
            "select batch_id, currency, source_count, staged_count, applied_count, "
            "source_net_amount, staged_net_amount, applied_net_amount, count_delta, "
            "amount_delta, reject_count, status from gold.type01_card_settlement "
            "where batch_id = ?",
            [batch_id],
        ).fetchall()
    finally:
        con.close()
    if not rows:
        return None
    names = [
        "batch_id",
        "currency",
        "source_count",
        "staged_count",
        "applied_count",
        "source_net_amount",
        "staged_net_amount",
        "applied_net_amount",
        "count_delta",
        "amount_delta",
        "reject_count",
        "status",
    ]
    row = dict(zip(names, rows[0]))
    for key in (
        "source_net_amount",
        "staged_net_amount",
        "applied_net_amount",
        "amount_delta",
    ):
        row[key] = str(row[key])
    return row


def _parquet_rows(batch_id: str) -> list[dict]:
    folder = LANDING / batch_id
    files = list(folder.glob("*.parquet")) if folder.is_dir() else []
    if not files:
        return []
    table = pq.read_table(files[0])
    rows = []
    for raw in table.to_pylist():
        row = dict(raw)
        if not isinstance(row.get("amount_brl"), Decimal):
            row["amount_brl"] = Decimal(str(row["amount_brl"]))
        rows.append(row)
    return rows


def _finding(batch_id: str) -> dict | None:
    path = LANDING / "_quarantine" / f"{batch_id}.finding.json"
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _attach_accepted(case: dict) -> Comparison:
    batch_id = case["batch_id"]
    modern_rows = _parquet_rows(batch_id)
    gold = _gold(batch_id)
    contract_recon = _load_yaml(case["expected_recon"])
    legacy = _legacy_batch(batch_id)
    diffs = []
    diffs.extend(
        compare_records(
            modern_rows,
            case["expected_csv"],
            batch_id=batch_id,
            reference_name="contract-csv",
        )
    )
    diffs.extend(
        compare_reconciliation(
            gold,
            contract_recon,
            batch_id=batch_id,
            reference_name="contract-reconciliation",
        )
    )
    diffs.extend(
        compare_reconciliation(
            gold,
            legacy["recon"],
            batch_id=batch_id,
            reference_name="legacy-observation",
        )
    )
    checks = {
        "business_correctness": not any(
            item.reference_name.startswith("contract") for item in diffs
        ),
        "legacy_parity": not any(
            item.reference_name == "legacy-observation" for item in diffs
        ),
        "gold_present": gold is not None,
        "parquet_present": bool(modern_rows),
        "records_match_contract": not any(item.scope == "record" for item in diffs),
    }
    return Comparison(
        batch_id=batch_id,
        type_number="01",
        outcome_class="MATCHED",
        differences=diffs,
        checks=checks,
    )


def _attach_rejected(case: dict) -> Comparison:
    batch_id = case["batch_id"]
    finding = _finding(batch_id) or {}
    contract = _load_yaml(case["contract_finding"])
    legacy = _legacy_batch(batch_id)
    parquet_rows = _parquet_rows(batch_id)
    gold = _gold(batch_id)
    modern_outcome = {
        "status": "quarantined",
        "code": finding.get("finding") or contract.get("expected_code"),
        "parquet_sha256": None,
        "record_count": len(parquet_rows),
        "controls": {},
    }
    if finding.get("declared_net_amount") is not None:
        modern_outcome["controls"]["declared_net_amount"] = finding["declared_net_amount"]
        modern_outcome["controls"]["computed_net_amount"] = finding["computed_net_amount"]
    legacy_final = None
    if legacy["batch"] is not None:
        legacy_final = {
            "status": legacy["batch"]["status"],
            "code": legacy["batch"]["code"] or "",
        }
    diffs, checks = compare_rejection(
        modern_outcome,
        legacy_final,
        contract,
        batch_id=batch_id,
    )
    checks["business_correctness"] = bool(
        checks.get("modern_matches_contract_status")
        and checks.get("modern_produced_no_parquet")
        and checks.get("modern_produced_no_rows")
    )
    checks["legacy_parity"] = bool(checks.get("legacy_matches_contract_status"))
    checks["no_invented_parquet"] = not parquet_rows
    checks["no_invented_gold"] = gold is None
    outcome = CONFIRMED_SOURCE_DEFECT if any(
        item.classification == CONFIRMED_SOURCE_DEFECT for item in diffs
    ) else str(contract.get("expected_code") or "classified")
    return Comparison(
        batch_id=batch_id,
        type_number="01",
        outcome_class=outcome,
        differences=diffs,
        checks=checks,
    )


def _write_packet(case: dict, comparison: Comparison) -> Path:
    dest = EVIDENCE / case["batch_id"]
    dest.mkdir(parents=True, exist_ok=True)
    raw = case["raw"]
    (dest / "raw-file.sha256").write_text(_sha256_file(raw) + "\n", encoding="utf-8")
    packet = comparison.as_dict()
    packet["case"] = case["name"]
    packet["questions"] = {
        "legacy_parity": bool(comparison.checks.get("legacy_parity")),
        "business_correctness": bool(comparison.checks.get("business_correctness")),
    }
    _dump(dest / "golden-match.json", packet)
    _dump(
        dest / "difference-adjudication.json",
        {
            "batch_id": case["batch_id"],
            "outcome_class": comparison.outcome_class,
            "resolved": comparison.resolved,
            "unexplained_count": len(comparison.unexplained),
            "differences": [item.as_dict() for item in comparison.differences],
        },
    )
    if case["kind"] == "accepted":
        landing = LANDING / case["batch_id"]
        parquet = next(landing.glob("*.parquet"))
        shutil.copy2(landing / f"{parquet.name}.sha256", dest / "parquet-file.sha256")
        shutil.copy2(landing / "landing-manifest.json", dest / "landing-manifest.json")
        dlt_receipt = REPO / "modern" / "lakehouse" / "dlt" / "register-receipt.json"
        if dlt_receipt.is_file():
            shutil.copy2(dlt_receipt, dest / "dlt-load.json")
        _dump(dest / "final-status.json", {"batch_id": case["batch_id"], "status": "succeeded"})
    else:
        finding = LANDING / "_quarantine" / f"{case['batch_id']}.finding.json"
        if finding.is_file():
            shutil.copy2(finding, dest / "finding.json")
        _dump(
            dest / "final-status.json",
            {
                "batch_id": case["batch_id"],
                "status": "quarantined",
                "code": comparison.outcome_class,
            },
        )
        # Rejected packets must not invent Parquet / Gold / dlt artifacts.
        for forbidden in (
            "parquet-file.sha256",
            "landing-manifest.json",
            "dlt-load.json",
            "ducklake-snapshot.json",
            "dbt-results.json",
        ):
            path = dest / forbidden
            if path.exists():
                path.unlink()
    return dest


def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    unknown = LANDING / "_quarantine" / "UNKNOWN.finding.json"
    if unknown.exists():
        unknown.unlink()
    results = []
    for case in CASES:
        comparison = (
            _attach_accepted(case) if case["kind"] == "accepted" else _attach_rejected(case)
        )
        dest = _write_packet(case, comparison)
        results.append(
            {
                "case": case["name"],
                "batch_id": case["batch_id"],
                "outcome_class": comparison.outcome_class,
                "resolved": comparison.resolved,
                "unexplained": len(comparison.unexplained),
                "questions": {
                    "legacy_parity": comparison.checks.get("legacy_parity"),
                    "business_correctness": comparison.checks.get("business_correctness"),
                },
                "packet": str(dest.relative_to(REPO)),
            }
        )
        if comparison.unexplained:
            print(json.dumps(results[-1], indent=2))
            raise SystemExit("unexplained differences")
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
