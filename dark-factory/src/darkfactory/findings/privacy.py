"""The three-layer privacy boundary described in DR-004.

Layer 1 is the closed schema, enforced separately in ``findings.writer``.
Layer 2 is a positive field allowlist plus an identity binding: every leaf must
be an approved path holding an approved value class, and every identity-bearing
value must equal a value that comes from the frozen scenario contract.
Layer 3 is a restricted-corpus scan over the digit identifiers that actually
exist in the frozen raw fixture.

Restricted tokens live in memory only. They are never written, never logged, and
never included in a violation message; a violation names the finding path and
the value class, never the value.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from ..canonical import encode
from ..errors import PrivacyViolationError

_DIGIT_RUN = re.compile(r"\d+")


def _paths(value: Any, prefix: str = "") -> Iterable[tuple[str, Any]]:
    """Yield every leaf as ``(allowlist path, value)``."""

    if isinstance(value, dict):
        for key in sorted(value):
            child = f"{prefix}.{key}" if prefix else str(key)
            yield from _paths(value[key], child)
    elif isinstance(value, list):
        for item in value:
            yield from _paths(item, f"{prefix}[]")
    else:
        yield prefix, value


def _matches_class(value: Any, definition: Mapping[str, Any]) -> bool:
    kind = definition["kind"]
    if kind == "boolean":
        return isinstance(value, bool)
    if kind == "integer":
        if isinstance(value, bool) or not isinstance(value, int):
            return False
        minimum = int(definition.get("minimum", 0))
        maximum = int(definition.get("maximum", 2**63))
        return bool(minimum <= value <= maximum)
    if kind == "string":
        if not isinstance(value, str):
            return False
        allowed = definition.get("enum")
        if allowed is not None:
            return bool(value in allowed)
        pattern = definition.get("pattern")
        return pattern is not None and re.match(pattern, value) is not None
    return False


def enforce_allowlist(finding: Mapping[str, Any], allowlist: Mapping[str, Any]) -> None:
    """Layer 2a. Refuse any leaf that is not approved, or not of its class."""

    paths: Mapping[str, str] = allowlist["paths"]
    classes: Mapping[str, Mapping[str, Any]] = allowlist["value_classes"]
    for path, value in _paths(finding):
        class_name = paths.get(path)
        if class_name is None:
            raise PrivacyViolationError(
                f"finding member is not on the privacy allowlist: {path}"
            )
        definition = classes.get(class_name)
        if definition is None:
            raise PrivacyViolationError(
                f"privacy allowlist names an undefined value class: {class_name}"
            )
        if not _matches_class(value, definition):
            raise PrivacyViolationError(
                f"finding member does not match its approved value class "
                f"{class_name}: {path}"
            )


def enforce_identity_binding(
    finding: Mapping[str, Any],
    *,
    scenario: str,
    batch_id: str,
    contract_code: str,
    terminal_code: str,
    type_number: str,
    peers: Sequence[str],
) -> None:
    """Layer 2b. Every identity-bearing value must come from frozen contract truth.

    Layer 2a proves a value has an approved *shape*. This proves the
    identity-bearing values are the *expected* ones, which is what removes the
    last route by which an unapproved string could ride along inside a
    correctly shaped member.
    """

    permitted_batches = {batch_id, *peers}
    expectations: tuple[tuple[str, Any, Any], ...] = (
        ("scenario", finding.get("scenario"), scenario),
        ("batch.batch_id", finding.get("batch", {}).get("batch_id"), batch_id),
        (
            "batch.contract_code",
            finding.get("batch", {}).get("contract_code"),
            contract_code,
        ),
        (
            "batch.type_number",
            finding.get("batch", {}).get("type_number"),
            type_number,
        ),
        ("terminal.code", finding.get("terminal", {}).get("code"), terminal_code),
    )
    for path, observed, expected in expectations:
        if observed != expected:
            raise PrivacyViolationError(
                f"finding identity member is not bound to contract truth: {path}"
            )
    for peer in finding.get("continuation", {}).get("peers", []):
        if peer.get("batch_id") not in permitted_batches:
            raise PrivacyViolationError(
                "finding names a peer batch outside the frozen scenario contract"
            )


def extract_restricted_digits(
    raw_fixture: Path,
    encoding: str,
    allowlist: Mapping[str, Any],
) -> frozenset[str]:
    """Layer 3, part one. Derive restricted digit identifiers from the fixture.

    The fixture is opened read-only and its content is never retained beyond
    this function; only the derived comparison forms leave it.
    """

    corpus = allowlist["restricted_corpus"]
    lengths = sorted(
        {
            int(entry["digit-runs-of-length"])
            for entry in corpus["extract"]
            if "digit-runs-of-length" in entry
        }
    )
    if not lengths:
        raise PrivacyViolationError(
            "the privacy contract declares no restricted digit lengths"
        )

    try:
        text = raw_fixture.read_bytes().decode(encoding, errors="replace")
    except OSError as exc:
        raise PrivacyViolationError(
            "the restricted-value scan cannot read its frozen fixture"
        ) from exc

    tokens: set[str] = set()
    for match in _DIGIT_RUN.finditer(text):
        run = match.group()
        for length in lengths:
            if len(run) < length:
                continue
            for start in range(0, len(run) - length + 1):
                window = run[start : start + length]
                # Fixed-width layouts zero-pad their numeric fields, so a run of
                # one repeated digit is padding, not an identifier. Keeping it
                # would flag every finding that contains a hash of zeros.
                if len(set(window)) == 1:
                    continue
                tokens.add(window)
    return frozenset(tokens)


def scannable_text(
    finding: Mapping[str, Any],
    allowlist: Mapping[str, Any],
) -> str:
    """Return the finding values a restricted identifier could actually occupy.

    Digest-classed members are excluded. A digest's value is determined by the
    bytes it references, not chosen by the detector, so a restricted identifier
    cannot be *placed* in one — while a 64-character hex string coincidentally
    containing an eleven-digit run is common enough to make the scan report
    violations that carry no restricted content.
    """

    paths: Mapping[str, str] = allowlist["paths"]
    return "\n".join(
        str(value)
        for path, value in _paths(finding)
        if paths.get(path) != "digest"
    )


def structural_digits(identities: Sequence[str]) -> frozenset[str]:
    """Return the digit forms of contract-bound identities.

    A batch identity is fifteen digits, so the fixture — which carries the
    batch identity in its own header and trailer — yields digit windows that
    are structural rather than restricted. Exempting them by derivation from
    the frozen scenario contract keeps the scan free of a hand-maintained list
    of "allowed numbers".
    """

    return frozenset(
        "".join(character for character in identity if character.isdigit())
        for identity in identities
    )


def enforce_restricted_corpus(
    finding: Mapping[str, Any],
    tokens: frozenset[str],
    exempt: frozenset[str] = frozenset(),
    allowlist: Mapping[str, Any] | None = None,
) -> None:
    """Layer 3, part two. Prove no restricted identifier reached the output.

    Matching runs against the finding's placeable values. It deliberately does
    not also run against a digits-only projection of the whole document: that
    projection glues unrelated numbers together, so it manufactures matches
    across field boundaries that no real leak would produce, while a leak that
    only exists after every delimiter is stripped is not a leak of a readable
    value.
    """

    haystack = (
        encode(finding).decode("ascii")
        if allowlist is None
        else scannable_text(finding, allowlist)
    )
    for token in tokens:
        if any(token in identity for identity in exempt):
            continue
        if token in haystack:
            raise PrivacyViolationError(
                "a restricted identifier from the frozen raw fixture reached "
                "the candidate finding"
            )


def scan(
    finding: Mapping[str, Any],
    *,
    allowlist: Mapping[str, Any],
    raw_fixture: Path,
    raw_encoding: str,
    scenario: str,
    batch_id: str,
    contract_code: str,
    terminal_code: str,
    type_number: str,
    peers: Sequence[str],
) -> None:
    """Run layers 2 and 3. Layer 1 is enforced by the closed schema."""

    enforce_allowlist(finding, allowlist)
    enforce_identity_binding(
        finding,
        scenario=scenario,
        batch_id=batch_id,
        contract_code=contract_code,
        terminal_code=terminal_code,
        type_number=type_number,
        peers=peers,
    )
    enforce_restricted_corpus(
        finding,
        extract_restricted_digits(raw_fixture, raw_encoding, allowlist),
        structural_digits((batch_id, *peers)),
        allowlist,
    )
