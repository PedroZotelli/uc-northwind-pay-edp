"""Compose Type 01 parse → schema → landing write. Does not import Java."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_BATCH_IN_NAME = re.compile(r"(B[0-9]{15})")

_DIR = Path(__file__).resolve().parent
if str(_DIR) not in sys.path:
    sys.path.insert(0, str(_DIR))

from model import landing_row_from_detail
from parser import parse_card_settlement
from schema import validate_rows
from writer import publish_finding, publish_landing, sha256_file


@dataclass(frozen=True)
class EmitResult:
    accepted: bool
    batch_id: str | None
    rejection_code: str | None
    parquet_path: str | None
    finding_path: str | None


def emit_batch(
    raw_path: Path,
    *,
    landing_root: Path,
    source_filename: str | None = None,
    source_manifest_path: Path | None = None,
    tokenization_key: bytes | None = None,
) -> EmitResult:
    payload = raw_path.read_bytes()
    filename = source_filename or raw_path.name
    raw_sha256 = sha256_file(raw_path)
    manifest_sha256 = (
        sha256_file(source_manifest_path) if source_manifest_path else raw_sha256
    )
    parsed = parse_card_settlement(
        payload, filename=filename, tokenization_key=tokenization_key
    )
    if not parsed.accepted:
        named = None
        match = _BATCH_IN_NAME.search(filename)
        if match:
            named = match.group(1)
        finding = publish_finding(
            landing_root=landing_root,
            batch_id=parsed.batch_id or named,
            source_filename=filename,
            raw_sha256=raw_sha256,
            finding=parsed.rejection_code or "REJECTED",
            declared_net=parsed.declared_net_amount,
            computed_net=parsed.computed_net_amount,
        )
        return EmitResult(
            accepted=False,
            batch_id=parsed.batch_id or named,
            rejection_code=parsed.rejection_code,
            parquet_path=None,
            finding_path=str(finding),
        )
    rows = validate_rows(
        tuple(landing_row_from_detail(detail, filename) for detail in parsed.details)
    )
    parquet = publish_landing(
        rows,
        landing_root=landing_root,
        source_filename=filename,
        raw_sha256=raw_sha256,
        source_manifest_sha256=manifest_sha256,
        net_amount=parsed.computed_net_amount,
    )
    return EmitResult(
        accepted=True,
        batch_id=parsed.batch_id,
        rejection_code=None,
        parquet_path=str(parquet),
        finding_path=None,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Emit Type 01 landing Parquet.")
    parser.add_argument("--raw", required=True, type=Path)
    parser.add_argument("--landing", required=True, type=Path)
    parser.add_argument("--source-filename", default=None)
    parser.add_argument("--source-manifest", type=Path, default=None)
    args = parser.parse_args(argv)
    result = emit_batch(
        args.raw,
        landing_root=args.landing,
        source_filename=args.source_filename,
        source_manifest_path=args.source_manifest,
    )
    print(
        f"accepted={result.accepted} batch_id={result.batch_id} "
        f"code={result.rejection_code} parquet={result.parquet_path} "
        f"finding={result.finding_path}"
    )
    return 0 if result.accepted or result.rejection_code else 1


if __name__ == "__main__":
    raise SystemExit(main())
