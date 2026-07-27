"""Recompute the legacy implementation/input manifest hash of a tree.

The boundary is the one published by the proof ledgers in ``plans/legacy.md``:
four root files plus every regular file under the six implementation roots,
with environments, caches, build output, runtime state, and evidence excluded.
Relative paths are byte-sorted and each file contributes one
``{sha256}  {relative_path}\\n`` record; the manifest hash is the SHA-256 of the
concatenated records.

This tool only reads. It is a measurement instrument for the proof ledger, not
part of the detector, and it never touches a frozen root.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

ROOT_FILES: tuple[str, ...] = (
    ".dockerignore",
    ".env.example",
    "Makefile",
    "compose.yaml",
)

ROOT_DIRECTORIES: tuple[str, ...] = (
    "contracts",
    "gen",
    "infra",
    "legacy",
    "tests",
    "validation",
)

EXCLUDED_DIRECTORY_NAMES: frozenset[str] = frozenset(
    {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".runtime",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "evidence",
        "node_modules",
        "output",
        "target",
        "venv",
    }
)

EXCLUDED_FILE_NAMES: frozenset[str] = frozenset({".DS_Store"})
EXCLUDED_SUFFIXES: frozenset[str] = frozenset({".pyc", ".pyo"})


class ManifestError(Exception):
    """The requested tree cannot be measured."""


def _directory_excluded(root: Path, directory: Path) -> bool:
    for part in directory.relative_to(root).parts:
        if part in EXCLUDED_DIRECTORY_NAMES or part.endswith(".egg-info"):
            return True
    return False


def _file_excluded(path: Path) -> bool:
    return path.name in EXCLUDED_FILE_NAMES or path.suffix in EXCLUDED_SUFFIXES


def collect(root: Path) -> list[Path]:
    """Return every in-boundary regular file below one tree root."""

    selected: list[Path] = []
    for name in ROOT_FILES:
        candidate = root / name
        if candidate.is_file() and not candidate.is_symlink():
            selected.append(candidate)
    for name in ROOT_DIRECTORIES:
        base = root / name
        if not base.is_dir():
            continue
        for candidate in base.rglob("*"):
            if candidate.is_symlink() or not candidate.is_file():
                continue
            if _directory_excluded(root, candidate.parent):
                continue
            if _file_excluded(candidate):
                continue
            selected.append(candidate)
    return selected


def manifest(root: Path) -> tuple[int, str, list[str]]:
    """Return the file count, manifest hash, and per-file records."""

    paths = collect(root)
    ordered = sorted(
        paths,
        key=lambda path: str(path.relative_to(root)).encode("utf-8"),
    )
    records: list[str] = []
    digest = hashlib.sha256()
    for path in ordered:
        record = (
            f"{hashlib.sha256(path.read_bytes()).hexdigest()}  "
            f"{path.relative_to(root)}\n"
        )
        digest.update(record.encode("utf-8"))
        records.append(record)
    return len(records), digest.hexdigest(), records


def _materialize_revision(repository: Path, revision: str, target: Path) -> None:
    """Extract one committed revision into an isolated temporary tree."""

    try:
        archive = subprocess.run(
            ["git", "archive", "--format=tar", revision],
            cwd=repository,
            check=True,
            capture_output=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ManifestError(f"Cannot read revision: {revision}") from exc
    with tempfile.TemporaryFile() as stream:
        stream.write(archive)
        stream.seek(0)
        with tarfile.open(fileobj=stream, mode="r|") as bundle:
            bundle.extractall(target, filter="data")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Recompute the legacy implementation/input manifest hash "
            "published by the proof ledgers."
        )
    )
    parser.add_argument(
        "--repository",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Repository root (default: this checkout).",
    )
    parser.add_argument(
        "--rev",
        default=None,
        help=(
            "Measure a committed revision instead of the working tree. "
            "Use the revision named by a ledger entry to reproduce its hash."
        ),
    )
    parser.add_argument(
        "--records",
        action="store_true",
        help="Print every per-file record before the summary.",
    )
    arguments = parser.parse_args(argv)

    repository: Path = arguments.repository.resolve()
    if arguments.rev is None:
        count, digest, records = manifest(repository)
        source = "working-tree"
    else:
        with tempfile.TemporaryDirectory(prefix=".df-manifest.") as temporary:
            _materialize_revision(repository, arguments.rev, Path(temporary))
            count, digest, records = manifest(Path(temporary))
        source = arguments.rev

    if arguments.records:
        sys.stdout.write("".join(records))
    print(
        json.dumps(
            {
                "files": count,
                "manifest_sha256": digest,
                "source": source,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ManifestError as error:
        print(f"tree-manifest error: {error}", file=sys.stderr)
        raise SystemExit(2) from error
