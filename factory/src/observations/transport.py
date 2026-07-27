"""Read-only adapter over the legacy SFTP transport zones.

Authenticates as the least-privileged ``operator`` role and exposes only
directory listing and reading. It deliberately does not construct the legacy
``SftpClient``, which carries ``put``, ``rename``, and ``remove``: reusing it
would turn "no write path" into a claim about how it is called. See DR-005.
"""

from __future__ import annotations

import hashlib
import json
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Iterator

import paramiko  # type: ignore[import-untyped]  # no stubs in the frozen dependency set

from canonical import encode
from detector_config import DetectorConfiguration
from errors import RuntimeUnavailableError

RAW_ZONES: tuple[str, ...] = (
    "raw/incoming",
    "raw/processing",
    "raw/archive",
    "raw/quarantine",
)
CSV_ZONES: tuple[str, ...] = (
    "csv/outgoing",
    "csv/processing",
    "csv/archive",
    "csv/quarantine",
)


@contextmanager
def read_only_transport(
    configuration: DetectorConfiguration,
) -> Iterator[paramiko.SFTPClient]:
    """Yield an SFTP channel used only for listing and reading."""

    client = paramiko.SSHClient()
    try:
        client.load_host_keys(str(configuration.sftp.known_hosts))
        client.set_missing_host_key_policy(paramiko.RejectPolicy())
        client.connect(
            hostname=configuration.sftp.host,
            port=configuration.sftp.port,
            username=configuration.sftp.username,
            password=configuration.sftp.password,
            allow_agent=False,
            look_for_keys=False,
            timeout=15,
        )
        channel = client.open_sftp()
        try:
            yield channel
        finally:
            channel.close()
    except (OSError, paramiko.SSHException) as exc:
        raise RuntimeUnavailableError(
            "the legacy SFTP runtime is not reachable read-only"
        ) from exc
    finally:
        client.close()


def _listdir(channel: paramiko.SFTPClient, path: str) -> list[str]:
    try:
        return sorted(channel.listdir(path))
    except FileNotFoundError:
        return []
    except OSError as exc:
        raise RuntimeUnavailableError(
            f"transport zone is not listable: {path}"
        ) from exc


@dataclass(frozen=True, slots=True)
class TransportObservation:
    """Where the transport left one batch, and what it did not produce."""

    batch_id: str
    raw_zones: tuple[str, ...]
    csv_zones: tuple[str, ...]
    quarantine_reason: dict[str, Any]
    reference: str

    @property
    def raw_quarantine_present(self) -> bool:
        return "raw/quarantine" in self.raw_zones

    @property
    def sanitized_csv_present(self) -> bool:
        return bool(self.csv_zones)


def observe_transport(
    channel: paramiko.SFTPClient,
    *,
    batch_id: str,
) -> TransportObservation:
    """Observe which zones hold the batch, reading nothing it does not need."""

    raw_zones = tuple(
        zone for zone in RAW_ZONES if batch_id in _listdir(channel, zone)
    )
    csv_zones = tuple(
        zone for zone in CSV_ZONES if batch_id in _listdir(channel, zone)
    )

    reason: dict[str, Any] = {}
    if "raw/quarantine" in raw_zones:
        path = f"raw/quarantine/{batch_id}/quarantine-reason.json"
        try:
            with channel.open(path, "r") as stream:
                loaded = json.loads(stream.read().decode("utf-8"))
            if isinstance(loaded, dict):
                reason = loaded
        except (OSError, ValueError):
            reason = {}

    projection = {
        "batch_id": batch_id,
        "csv_zones": list(csv_zones),
        "quarantine_reason": reason,
        "raw_zones": list(raw_zones),
    }
    return TransportObservation(
        batch_id=batch_id,
        raw_zones=raw_zones,
        csv_zones=csv_zones,
        quarantine_reason=reason,
        reference="sha256:" + hashlib.sha256(encode(projection)).hexdigest(),
    )
