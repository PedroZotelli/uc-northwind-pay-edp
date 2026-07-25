"""Deterministic comparison of declared against independently computed controls.

Detection answers one question and carries no opinion about blame: which
controls does the source declare, which did the legacy components compute, and
where do they differ. Ownership reasoning lives in ``attribution``.
"""

from __future__ import annotations

from dataclasses import dataclass

from errors import ContradictoryObservationError, NoMismatchError
from observations.collect import ObservationSet
from observations.model import classify_control


@dataclass(frozen=True, slots=True)
class ComparedControl:
    """One control seen from both sides."""

    control: str
    value_class: str
    declared: str
    computed: str
    matches: bool

    def as_finding_entry(self) -> dict[str, object]:
        return {
            "computed": self.computed,
            "control": self.control,
            "declared": self.declared,
            "matches": self.matches,
            "value_class": self.value_class,
        }


@dataclass(frozen=True, slots=True)
class Detection:
    """The complete deterministic comparison for one batch."""

    compared: tuple[ComparedControl, ...]
    differences: tuple[ComparedControl, ...]

    @property
    def difference_count(self) -> int:
        return len(self.differences)


def _merge(sets: tuple[object, ...], side: str) -> dict[str, str]:
    """Merge control values across channels, refusing any disagreement."""

    merged: dict[str, str] = {}
    for control_set in sets:
        for name, value in control_set.values.items():  # type: ignore[attr-defined]
            existing = merged.get(name)
            if existing is not None and existing != value:
                raise ContradictoryObservationError(
                    f"{side} control {name} differs between channels"
                )
            merged[name] = value
    return merged


def detect(observations: ObservationSet) -> Detection:
    """Compare declared and computed controls, refusing when nothing differs.

    A matched batch is not a finding. Producing one anyway would make the
    detector's output meaningless as a signal, so a healthy batch is a stable
    refusal (``DF-E-NO-MISMATCH``) rather than an empty finding.
    """

    declared = _merge(observations.declared, "declared")
    computed = _merge(observations.computed, "computed")

    shared = sorted(set(declared) & set(computed))
    if not shared:
        raise ContradictoryObservationError(
            "no control is reported on both the declared and computed sides"
        )

    compared: list[ComparedControl] = []
    for name in shared:
        declared_value = declared[name]
        computed_value = computed[name]
        declared_class = classify_control(declared_value)
        computed_class = classify_control(computed_value)
        if declared_class != computed_class:
            raise ContradictoryObservationError(
                f"control {name} is declared and computed in different classes"
            )
        compared.append(
            ComparedControl(
                control=name,
                value_class=declared_class,
                declared=declared_value,
                computed=computed_value,
                matches=declared_value == computed_value,
            )
        )

    differences = tuple(entry for entry in compared if not entry.matches)
    if not differences:
        raise NoMismatchError(
            "declared and computed controls agree; no finding is produced"
        )
    return Detection(compared=tuple(compared), differences=differences)
