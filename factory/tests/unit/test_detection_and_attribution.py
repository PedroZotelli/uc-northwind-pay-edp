"""Unit tests for deterministic detection and evidence-based attribution."""

from __future__ import annotations

import unittest

from attribution.source_system import attribute
from detection.control_mismatch import detect
from errors import (
    ContradictoryObservationError,
    NoMismatchError,
)
from observations.collect import WITHHOLDABLE_CHANNELS
from observations.model import (
    CHANNEL_JAVA,
    CHANNEL_POSTGRES_CONTROL_PLANE,
    CHANNEL_POSTGRES_DIAGNOSTIC,
    CHANNEL_SOURCE_MANIFEST,
)

import factories


class DetectionTest(unittest.TestCase):
    def test_detects_exactly_the_one_cent_difference(self) -> None:
        detection = detect(factories.observation_set())
        self.assertEqual(detection.difference_count, 1)
        difference = detection.differences[0]
        self.assertEqual(difference.control, "net_amount")
        self.assertEqual(difference.declared, "173.44")
        self.assertEqual(difference.computed, "173.45")
        self.assertEqual(difference.value_class, "money")

    def test_compares_every_shared_control_not_only_the_differing_one(self) -> None:
        detection = detect(factories.observation_set())
        self.assertEqual(
            sorted(entry.control for entry in detection.compared),
            ["detail_count", "net_amount"],
        )

    def test_matched_controls_produce_no_finding(self) -> None:
        matched = {
            CHANNEL_JAVA: factories.DECLARED,
            CHANNEL_POSTGRES_DIAGNOSTIC: factories.DECLARED,
            CHANNEL_POSTGRES_CONTROL_PLANE: factories.DECLARED,
        }
        with self.assertRaises(NoMismatchError):
            detect(factories.observation_set(computed=matched))

    def test_refuses_when_two_channels_report_different_computed_values(self) -> None:
        conflicting = {
            CHANNEL_JAVA: {"detail_count": "2", "net_amount": "173.45"},
            CHANNEL_POSTGRES_DIAGNOSTIC: {"detail_count": "2", "net_amount": "173.46"},
            CHANNEL_POSTGRES_CONTROL_PLANE: {"detail_count": "2", "net_amount": "173.45"},
        }
        with self.assertRaises(ContradictoryObservationError):
            detect(factories.observation_set(computed=conflicting))

    def test_refuses_when_a_control_changes_value_class(self) -> None:
        mixed = {
            CHANNEL_JAVA: {"detail_count": "2", "net_amount": "17345"},
            CHANNEL_POSTGRES_DIAGNOSTIC: {"detail_count": "2", "net_amount": "17345"},
            CHANNEL_POSTGRES_CONTROL_PLANE: {
                "detail_count": "2",
                "net_amount": "17345",
            },
        }
        with self.assertRaises(ContradictoryObservationError):
            detect(factories.observation_set(computed=mixed))


class AttributionTest(unittest.TestCase):
    def test_complete_observations_attribute_to_the_source_system(self) -> None:
        observations = factories.observation_set()
        attribution = attribute(observations, detect(observations))
        self.assertEqual(attribution.owner, "source_system_of_record")
        self.assertEqual(attribution.confidence, "conclusive")
        self.assertTrue(all(entry.satisfied for entry in attribution.basis))

    def test_withholding_any_required_channel_prevents_a_conclusion(self) -> None:
        """The Step 4 gate, executed once per required channel."""

        for channel in WITHHOLDABLE_CHANNELS:
            with self.subTest(channel=channel):
                observations = factories.observation_set(
                    withheld=frozenset({channel})
                )
                attribution = attribute(observations, detect(observations))
                self.assertEqual(attribution.confidence, "inconclusive")
                self.assertEqual(attribution.owner, "undetermined")
                self.assertFalse(
                    all(entry.satisfied for entry in attribution.basis),
                    "a rule should have failed",
                )

    def test_derived_projections_alone_cannot_corroborate(self) -> None:
        """A chain of restatements is not independent computation."""

        observations = factories.observation_set(
            withheld=frozenset({CHANNEL_JAVA}),
            diagnostic_independent=False,
        )
        attribution = attribute(observations, detect(observations))
        self.assertEqual(attribution.confidence, "inconclusive")

    def test_a_disagreeing_declaration_is_refused_before_attribution(self) -> None:
        """If the manifest and the raw trailer disagree about what the source
        declared, the observation set does not describe one declaration.

        Detection refuses first, so this never reaches attribution at all —
        stricter than degrading to inconclusive, and correct: there is no single
        declared value to attribute.
        """

        observations = factories.observation_set(
            declared={
                CHANNEL_SOURCE_MANIFEST: {"detail_count": "2", "net_amount": "173.44"},
                CHANNEL_JAVA: {"detail_count": "2", "net_amount": "173.43"},
                CHANNEL_POSTGRES_CONTROL_PLANE: {
                    "detail_count": "2",
                    "net_amount": "173.44",
                },
            }
        )
        with self.assertRaises(ContradictoryObservationError):
            detect(observations)

    def test_a_disagreeing_declaration_also_fails_the_attribution_rule(self) -> None:
        """The rule itself does not depend on detection having refused first."""

        from attribution.source_system import _declaration_consistent

        observations = factories.observation_set(
            declared={
                CHANNEL_SOURCE_MANIFEST: {"detail_count": "2", "net_amount": "173.44"},
                CHANNEL_JAVA: {"detail_count": "2", "net_amount": "173.43"},
                CHANNEL_POSTGRES_CONTROL_PLANE: {
                    "detail_count": "2",
                    "net_amount": "173.44",
                },
            }
        )
        self.assertFalse(_declaration_consistent(observations).satisfied)

    def test_basis_names_rules_and_channels_rather_than_prose(self) -> None:
        observations = factories.observation_set()
        attribution = attribute(observations, detect(observations))
        entry = attribution.as_finding_entry()
        self.assertEqual(
            sorted(item["rule"] for item in entry["basis"]),
            [
                "declaration-source-owned-and-consistent",
                "declared-differs-from-computed",
                "independent-computation-agreement",
            ],
        )
        for item in entry["basis"]:
            self.assertEqual(sorted(item), ["channels", "rule", "satisfied"])


if __name__ == "__main__":
    unittest.main()
