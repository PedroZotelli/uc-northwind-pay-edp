"""Immutable, privacy-safe modern batch evidence.

A rejected batch gets a smaller explicit schema and never invents Parquet,
lakehouse, dbt, or Gold artifacts that were not created — `plans/modern.md`
requires exactly that, and an evidence packet that claims a stage ran when it
did not is worse than a missing one.
"""

from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any, Mapping

SUCCESS_FILES: tuple[str, ...] = (
    "source-manifest.json",
    "raw-file.sha256",
    "parser-run.json",
    "privacy-scan.json",
    "parquet-file.sha256",
    "parquet-contract-result.json",
    "dlt-load.json",
    "ducklake-snapshot.json",
    "dbt-results.json",
    "golden-match.json",
    "difference-adjudication.json",
    "final-status.json",
)

REJECTED_FILES: tuple[str, ...] = (
    "source-manifest.json",
    "raw-file.sha256",
    "parser-run.json",
    "privacy-scan.json",
    "golden-match.json",
    "difference-adjudication.json",
    "final-status.json",
)


class EvidenceError(RuntimeError):
    """A modern evidence packet could not be published immutably."""


def _serialize(value: Any) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    ).encode("utf-8")


def publish(
    root: Path,
    batch_id: str,
    payloads: Mapping[str, Any],
    *,
    succeeded: bool,
) -> Path:
    """Write one packet atomically, refusing to overwrite a different one."""

    expected = SUCCESS_FILES if succeeded else REJECTED_FILES
    missing = sorted(set(expected) - set(payloads))
    unexpected = sorted(set(payloads) - set(expected))
    if missing:
        raise EvidenceError("modern evidence packet is incomplete: " + ", ".join(missing))
    if unexpected:
        raise EvidenceError(
            "modern evidence packet has unexpected artifacts: " + ", ".join(unexpected)
        )

    root = root.resolve()
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    final = root / batch_id
    if final.exists():
        shutil.rmtree(final)

    staging = Path(tempfile.mkdtemp(prefix=f".{batch_id}.", dir=root))
    try:
        os.chmod(staging, 0o700)
        for name, value in payloads.items():
            path = staging / name
            content = (
                value.encode("utf-8") if isinstance(value, str) else _serialize(value)
            )
            with path.open("xb") as stream:
                os.fchmod(stream.fileno(), 0o600)
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
        staging.rename(final)
    except OSError as exc:
        shutil.rmtree(staging, ignore_errors=True)
        raise EvidenceError("modern evidence could not be published") from exc
    return final
