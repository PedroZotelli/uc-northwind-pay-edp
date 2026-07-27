"""Immutable observation values shared by every read-only adapter.

Each observation carries its own independence class so that a reader of a
finding never has to guess how much a corroboration is worth. See DR-006.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

MONEY = re.compile(r"^-?\d+\.\d{2}$")

CHANNEL_SOURCE_MANIFEST = "legacy-source-manifest"
CHANNEL_JAVA = "legacy-java-processor"
CHANNEL_POSTGRES_DIAGNOSTIC = "legacy-postgres-diagnostic"
CHANNEL_POSTGRES_CONTROL_PLANE = "legacy-postgres-control-plane"
CHANNEL_TRANSPORT = "legacy-sftp-transport"
CHANNEL_CONTRACT_ORACLE = "legacy-contract-oracle"

ROLE_SYSTEM_OF_RECORD = "system_of_record"
ROLE_OBSERVATION = "source_of_observation"
ROLE_CORRECTNESS = "source_of_correctness"

INDEPENDENCE_SOURCE_DECLARATION = "source_declaration"
INDEPENDENCE_INDEPENDENT = "independent_computation"
INDEPENDENCE_PERSISTED = "persisted_record"
INDEPENDENCE_DERIVED = "derived_projection"
INDEPENDENCE_TRANSPORT = "transport_observation"
INDEPENDENCE_CONTRACT = "contract_comparison"


def normalize_control(value: object) -> str:
    """Render one control value as its canonical comparison text.

    Counts become plain digits and money keeps exact scale-two text. Booleans
    are rejected before they can masquerade as counts.
    """

    if isinstance(value, bool):
        raise ValueError("control value must not be boolean")
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str) and (MONEY.match(value) or value.isdigit()):
        return value
    raise ValueError("control value is not a canonical count or money text")


def classify_control(value: str) -> str:
    """Return the value class of an already normalized control value."""

    return "money" if MONEY.match(value) else "count"


@dataclass(frozen=True, slots=True)
class ChannelObservation:
    """One consumed observation channel and the exact bytes it was read from."""

    channel: str
    role: str
    independence: str
    reference: str

    def as_finding_entry(self) -> dict[str, str]:
        return {
            "channel": self.channel,
            "independence": self.independence,
            "reference": self.reference,
            "role": self.role,
        }


@dataclass(frozen=True, slots=True)
class ControlSet:
    """Declared or computed controls reported by exactly one channel."""

    channel: str
    values: Mapping[str, str]

    @staticmethod
    def of(channel: str, values: Mapping[str, str]) -> ControlSet:
        return ControlSet(channel=channel, values=MappingProxyType(dict(values)))


@dataclass(frozen=True, slots=True)
class Lineage:
    """The immutable identity every channel must agree on."""

    batch_id: str
    type_number: str
    raw_sha256: str
    manifest_sha256: str
    contract_code: str
    contract_version: int
    layout_version: str
