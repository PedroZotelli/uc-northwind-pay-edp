"""Canonical JSON encoding and finding identity.

Canonical form is ``sort_keys=True, ensure_ascii=True, separators=(",", ":")``
encoded UTF-8. Sorted keys make the byte sequence independent of construction
order; ASCII escaping removes any dependence on the reader's encoding and gives
the restricted-value scan a known alphabet.

Identity is SHA-256 over the canonical encoding with ``finding_id`` and
``created_at`` removed, so two runs against the same immutable observations
produce the same identity while still recording when each ran. See DR-003.
"""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any, Mapping

IDENTITY_EXCLUSIONS: tuple[tuple[str, ...], ...] = (
    ("finding_id",),
    ("created_at",),
)

# Additionally elided when a finding is compared against a frozen expected
# fixture: it changes whenever the detector's own source changes, which is
# correct for identity but would make the fixture a build artifact.
FIXTURE_EXCLUSIONS: tuple[tuple[str, ...], ...] = IDENTITY_EXCLUSIONS + (
    ("references", "detector_source_sha256"),
)


def encode(value: Any) -> bytes:
    """Return the canonical byte encoding of one JSON-compatible value."""

    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("utf-8")


def digest(payload: bytes) -> str:
    """Return the prefixed hex SHA-256 of raw bytes."""

    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


def without(
    value: Mapping[str, Any],
    exclusions: tuple[tuple[str, ...], ...],
) -> dict[str, Any]:
    """Return a deep copy with each dotted path removed when present."""

    reduced: dict[str, Any] = copy.deepcopy(dict(value))
    for path in exclusions:
        cursor: Any = reduced
        for part in path[:-1]:
            if not isinstance(cursor, dict) or part not in cursor:
                cursor = None
                break
            cursor = cursor[part]
        if isinstance(cursor, dict):
            cursor.pop(path[-1], None)
    return reduced


def identity_bytes(finding: Mapping[str, Any]) -> bytes:
    """Return the canonical bytes that define a finding's identity."""

    return encode(without(finding, IDENTITY_EXCLUSIONS))


def finding_identity(finding: Mapping[str, Any]) -> str:
    """Return the stable ``sha256:`` identity of one finding."""

    return digest(identity_bytes(finding))


def fixture_projection(finding: Mapping[str, Any]) -> dict[str, Any]:
    """Return the finding members a frozen expected fixture pins exactly."""

    return without(finding, FIXTURE_EXCLUSIONS)


def serialize(finding: Mapping[str, Any]) -> bytes:
    """Return the published file bytes: canonical JSON plus one newline."""

    return encode(finding) + b"\n"
