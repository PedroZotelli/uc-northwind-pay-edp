"""Read-only Dark Factory runtime settings and contract loading.

``.env`` is parsed here rather than through ``legacy/runner/config.py`` on
purpose: reusing the legacy loader would be the first thread of coupling
between an observer and the system it observes. See DR-002.
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import yaml

from .errors import ObservationMissingError

REPOSITORY_ROOT: Path = Path(__file__).resolve().parents[3]
CONTRACT_ROOT: Path = REPOSITORY_ROOT / "dark-factory" / "contracts"
DETECTOR_SOURCE_ROOT: Path = REPOSITORY_ROOT / "dark-factory" / "src" / "darkfactory"


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ObservationMissingError(
            f"contract artifact is unreadable: {path.name}"
        ) from exc


def read_yaml(path: Path) -> Any:
    """Load one YAML document read-only."""

    return yaml.safe_load(_read_text(path))


def read_bytes(path: Path) -> bytes:
    """Read one file read-only, refusing with a stable code when absent."""

    try:
        return path.read_bytes()
    except OSError as exc:
        raise ObservationMissingError(
            f"observation artifact is unreadable: {path.name}"
        ) from exc


@dataclass(frozen=True, slots=True)
class SftpCredentials:
    """One least-privilege SFTP actor used for observation only."""

    host: str
    port: int
    username: str
    password: str
    known_hosts: Path


@dataclass(frozen=True, slots=True)
class DetectorConfiguration:
    """Validated read-only connection settings for observing the runtime."""

    root: Path
    postgres_dsn: str
    sftp: SftpCredentials

    @classmethod
    def load(cls, root: Path | None = None) -> DetectorConfiguration:
        repository = (root or REPOSITORY_ROOT).resolve()
        environment = _environment(repository / ".env")
        host = environment["POSTGRES_HOST"]
        port = environment["POSTGRES_PORT"]
        database = environment["POSTGRES_DB"]
        user = environment["POSTGRES_USER"]
        password = environment["POSTGRES_PASSWORD"]
        return cls(
            root=repository,
            postgres_dsn=(
                f"host={host} port={port} dbname={database} "
                f"user={user} password={password} connect_timeout=10"
            ),
            sftp=SftpCredentials(
                host=environment["SFTP_HOST"],
                port=int(environment["SFTP_PORT"]),
                # The operator role is the least-privileged observer available.
                username=environment["SFTP_OPERATOR_USER"],
                password=environment["SFTP_OPERATOR_PASSWORD"],
                known_hosts=repository / ".runtime" / "known_hosts",
            ),
        )


def _environment(dotenv: Path) -> Mapping[str, str]:
    """Merge process environment over ``.env`` without mutating either."""

    values: dict[str, str] = {}
    if dotenv.is_file():
        for line in _read_text(dotenv).splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            name, value = stripped.split("=", 1)
            values[name.strip()] = value.strip()
    for name, value in os.environ.items():
        if name.startswith(("POSTGRES_", "SFTP_")):
            values[name] = value
    missing = sorted(
        name
        for name in (
            "POSTGRES_HOST",
            "POSTGRES_PORT",
            "POSTGRES_DB",
            "POSTGRES_USER",
            "POSTGRES_PASSWORD",
            "SFTP_HOST",
            "SFTP_PORT",
            "SFTP_OPERATOR_USER",
            "SFTP_OPERATOR_PASSWORD",
        )
        if name not in values or not values[name]
    )
    if missing:
        raise ObservationMissingError(
            "runtime settings are incomplete: " + ", ".join(missing)
        )
    return values


def detector_source_digest() -> str:
    """Return a stable digest over the detector's own Python source.

    Binds a finding to the exact code that produced it. Byte-sorted relative
    paths, one ``{sha256}  {relative_path}\\n`` record each, hashed as a whole —
    the same shape the proof ledgers use for the legacy implementation manifest.
    """

    records: list[bytes] = []
    for path in sorted(
        (
            candidate
            for candidate in DETECTOR_SOURCE_ROOT.rglob("*.py")
            if "__pycache__" not in candidate.parts
        ),
        key=lambda item: str(
            item.relative_to(DETECTOR_SOURCE_ROOT)
        ).encode("utf-8"),
    ):
        content = hashlib.sha256(path.read_bytes()).hexdigest()
        relative = path.relative_to(DETECTOR_SOURCE_ROOT)
        records.append(f"{content}  {relative}\n".encode("utf-8"))
    return f"sha256:{hashlib.sha256(b''.join(records)).hexdigest()}"
