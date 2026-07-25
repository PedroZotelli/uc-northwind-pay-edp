"""Evidence-based attribution of a control mismatch to its owner.

Implements the conclusiveness rule from DR-006. There is no prose explanation
member anywhere in this module's output: the basis list — each entry naming a
rule, the channels that contributed, and whether it was satisfied — *is* the
explanation, and unlike a sentence it is machine-checkable.
"""

from __future__ import annotations

from dataclasses import dataclass

from detection.control_mismatch import Detection
from observations.collect import ObservationSet
from observations.model import (
    CHANNEL_JAVA,
    CHANNEL_POSTGRES_CONTROL_PLANE,
    CHANNEL_POSTGRES_DIAGNOSTIC,
    CHANNEL_SOURCE_MANIFEST,
    INDEPENDENCE_INDEPENDENT,
)

OWNER_SOURCE_SYSTEM = "source_system_of_record"
OWNER_UNDETERMINED = "undetermined"

RULE_DECLARATION_CONSISTENT = "declaration-source-owned-and-consistent"
RULE_INDEPENDENT_AGREEMENT = "independent-computation-agreement"
RULE_DECLARED_DIFFERS = "declared-differs-from-computed"


@dataclass(frozen=True, slots=True)
class BasisEntry:
    """One named rule, the channels that fed it, and whether it held."""

    rule: str
    channels: tuple[str, ...]
    satisfied: bool

    def as_finding_entry(self) -> dict[str, object]:
        return {
            "channels": list(self.channels),
            "rule": self.rule,
            "satisfied": self.satisfied,
        }


@dataclass(frozen=True, slots=True)
class Attribution:
    """Who owns the discrepancy, on what basis, and how firmly."""

    owner: str
    confidence: str
    basis: tuple[BasisEntry, ...]

    @property
    def conclusive(self) -> bool:
        return self.confidence == "conclusive"

    def as_finding_entry(self) -> dict[str, object]:
        return {
            "basis": [entry.as_finding_entry() for entry in self.basis],
            "confidence": self.confidence,
            "owner": self.owner,
        }


# Each rule names the channels it requires. Requiring the complete expected set
# — rather than "at least two of them" — is what keeps the Step 4 gate from
# being vacuous: with three declarations and three computed reports available,
# an "at least two" rule survives the loss of any single channel, so no channel
# would be required and the withhold probe would prove nothing. Demanding the
# whole set turns redundancy into strength instead of slack, and matches the
# fail-closed posture the brief asks for.
DECLARATION_CHANNELS: tuple[str, ...] = (
    CHANNEL_SOURCE_MANIFEST,          # the source system's published manifest
    CHANNEL_JAVA,                     # the raw file's own trailer, decoded
    CHANNEL_POSTGRES_CONTROL_PLANE,   # the declaration persisted by the loader
)

COMPUTATION_CHANNELS: tuple[str, ...] = (
    CHANNEL_JAVA,                     # independent parse of the raw records
    CHANNEL_POSTGRES_DIAGNOSTIC,      # the diagnostic recomputation or restatement
    CHANNEL_POSTGRES_CONTROL_PLANE,   # the rejection controls persisted durably
)


def _all_agree(sets: tuple[object, ...]) -> bool:
    """Whether every pair of control sets agrees on the controls they share."""

    reference = sets[0].values  # type: ignore[attr-defined]
    for control_set in sets[1:]:
        values = control_set.values  # type: ignore[attr-defined]
        shared = set(reference) & set(values)
        if not shared or any(reference[name] != values[name] for name in shared):
            return False
    return True


def _declaration_consistent(observations: ObservationSet) -> BasisEntry:
    """A1: the wrong value is what the source declared, everywhere it declared it.

    The manifest declaration and the declaration the processor decoded from the
    raw file's own trailer are two distinct source-owned artifacts bound by
    hash; the control plane holds the declaration a third component persisted.
    Agreement across all three rules out transport damage and manifest-only
    error, which is what places the defect in the source system's own
    computation rather than anywhere downstream of it.
    """

    present = tuple(
        control_set
        for control_set in observations.declared
        if control_set.channel in DECLARATION_CHANNELS and control_set.values
    )
    channels = tuple(control_set.channel for control_set in present)
    satisfied = (
        set(channels) == set(DECLARATION_CHANNELS) and _all_agree(present)
    )
    return BasisEntry(
        rule=RULE_DECLARATION_CONSISTENT,
        channels=channels,
        satisfied=satisfied,
    )


def _independent_agreement(observations: ObservationSet) -> BasisEntry:
    """A2: every component that computed the controls agrees, and one is independent.

    At least one contributor must be an actual independent computation rather
    than a restatement, so a chain of projections can never look like
    corroboration. Types 02-05 satisfy that through the Java processor alone;
    Type 01 also has the read-only SQL recomputation.
    """

    present = tuple(
        control_set
        for control_set in observations.computed
        if control_set.channel in COMPUTATION_CHANNELS and control_set.values
    )
    channels = tuple(control_set.channel for control_set in present)
    independent = any(
        entry.independence == INDEPENDENCE_INDEPENDENT
        and entry.channel in channels
        for entry in observations.channels
    )
    satisfied = (
        set(channels) == set(COMPUTATION_CHANNELS)
        and independent
        and _all_agree(present)
    )
    return BasisEntry(
        rule=RULE_INDEPENDENT_AGREEMENT,
        channels=channels,
        satisfied=satisfied,
    )


def _declared_differs(
    observations: ObservationSet,
    detection: Detection,
) -> BasisEntry:
    """A3: at least one control actually differs."""

    channels = tuple(
        channel
        for channel in (
            CHANNEL_SOURCE_MANIFEST,
            CHANNEL_JAVA,
            CHANNEL_POSTGRES_DIAGNOSTIC,
            CHANNEL_POSTGRES_CONTROL_PLANE,
        )
        if channel not in observations.withheld
    )
    return BasisEntry(
        rule=RULE_DECLARED_DIFFERS,
        channels=channels,
        satisfied=detection.difference_count >= 1,
    )


def attribute(
    observations: ObservationSet,
    detection: Detection,
) -> Attribution:
    """Return the attribution, failing closed to ``undetermined``."""

    basis = (
        _declaration_consistent(observations),
        _independent_agreement(observations),
        _declared_differs(observations, detection),
    )
    conclusive = all(entry.satisfied for entry in basis)
    return Attribution(
        owner=OWNER_SOURCE_SYSTEM if conclusive else OWNER_UNDETERMINED,
        confidence="conclusive" if conclusive else "inconclusive",
        basis=basis,
    )
