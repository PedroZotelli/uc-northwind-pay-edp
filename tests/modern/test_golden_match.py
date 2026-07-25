"""Unit proof for the golden-match referee itself.

The referee decides whether a batch may be served, and it had no unit tests: it
was exercised only end to end, where a check that cannot fail is invisible. Two
of these tests are regression guards for defects found by review rather than by
a failing gate.
"""

from __future__ import annotations

import sys
import unittest
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "validation" / "golden-match"))

import golden_match  # noqa: E402


def _csv(directory: Path, text: str) -> Path:
    path = directory / "expected.csv"
    path.write_text(text, encoding="utf-8")
    return path


class MoneyNormalizationTest(unittest.TestCase):
    """A referee compares observations; it never repairs them."""

    def test_exact_two_place_values_render_unchanged(self) -> None:
        for value in ("173.45", "0.00", "-12.30", Decimal("173.45")):
            self.assertEqual(golden_match._money(value), f"{Decimal(str(value)):.2f}")

    def test_a_sub_cent_value_is_refused_rather_than_rounded(self) -> None:
        # The previous implementation returned "173.44" here: it rounded, and it
        # rounded HALF_EVEN where the contract mandates HALF_UP. Either way a
        # sub-cent difference would have been absorbed silently.
        with self.assertRaises(golden_match.GoldenMatchError):
            golden_match._money("173.445")

    def test_an_unpadded_value_is_refused_rather_than_padded(self) -> None:
        self.assertEqual(golden_match._money("173.40"), "173.40")
        with self.assertRaises(golden_match.GoldenMatchError):
            golden_match._money("173.4001")


class ResolutionTest(unittest.TestCase):
    def test_an_unexplained_difference_blocks_resolution(self) -> None:
        comparison = golden_match.Comparison("B1", "01", "accepted")
        comparison.checks["gold_present"] = True
        comparison.differences.append(
            golden_match.Difference(
                "record", "B1:1", "amount_brl", "1.00", "2.00",
                "contract", golden_match.MODERN_DEFECT,
            )
        )
        self.assertFalse(comparison.resolved)

    def test_an_explained_difference_does_not_block_resolution(self) -> None:
        comparison = golden_match.Comparison("B1", "01", "rejected")
        comparison.differences.append(
            golden_match.Difference(
                "controls", "B1", "net_amount", "173.45", "173.44",
                "source-declaration", golden_match.CONFIRMED_SOURCE_DEFECT,
            )
        )
        self.assertTrue(comparison.resolved)

    def test_a_failing_check_blocks_resolution_with_no_differences(self) -> None:
        comparison = golden_match.Comparison("B1", "01", "accepted")
        comparison.checks["gold_present"] = False
        self.assertFalse(comparison.resolved)


class RecordComparisonTest(unittest.TestCase):
    def test_a_missing_modern_row_is_a_modern_defect(self) -> None:
        with TemporaryDirectory() as directory:
            expected = _csv(
                Path(directory), "source_record_number,amount_brl\n1,10.00\n"
            )
            differences = golden_match.compare_records(
                [], expected, batch_id="B1", reference_name="contract"
            )
        self.assertEqual(len(differences), 1)
        self.assertEqual(differences[0].classification, golden_match.MODERN_DEFECT)
        self.assertEqual(differences[0].modern, "<absent>")

    def test_a_decimal_is_compared_at_the_scale_the_artifact_uses(self) -> None:
        with TemporaryDirectory() as directory:
            expected = _csv(
                Path(directory),
                "source_record_number,amount_brl,rate_percent\n1,10.00,2.500\n",
            )
            differences = golden_match.compare_records(
                [
                    {
                        "source_record_number": 1,
                        "amount_brl": Decimal("10.00"),
                        "rate_percent": Decimal("2.500"),
                    }
                ],
                expected,
                batch_id="B1",
                reference_name="contract",
            )
        self.assertEqual(differences, [])


class RejectionComparisonTest(unittest.TestCase):
    """The legacy-parity half of a rejected batch."""

    MODERN = {
        "status": "quarantined",
        "code": "INVALID_OVERPUNCH",
        "record_count": 0,
        "controls": {},
    }
    CONTRACT = {
        "expected_status": "quarantined",
        "expected_code": "INVALID_OVERPUNCH",
    }

    def test_a_live_legacy_observation_is_compared_and_recorded(self) -> None:
        legacy = {"status": "quarantined", "code": "INVALID_OVERPUNCH"}
        differences, checks = golden_match.compare_rejection(
            self.MODERN, legacy, self.CONTRACT, batch_id="B1"
        )
        self.assertEqual(differences, [])
        self.assertTrue(checks["legacy_terminal_observed"])
        self.assertTrue(checks["legacy_matches_contract_status"])
        self.assertTrue(checks["legacy_matches_contract_code"])

    def test_a_legacy_status_disagreement_is_a_modern_defect(self) -> None:
        legacy = {"status": "succeeded", "code": ""}
        differences, checks = golden_match.compare_rejection(
            self.MODERN, legacy, self.CONTRACT, batch_id="B1"
        )
        classifications = [item.classification for item in differences]
        self.assertIn(golden_match.MODERN_DEFECT, classifications)
        self.assertFalse(checks["legacy_matches_contract_status"])

    def test_a_differing_code_is_an_approved_behavior_change(self) -> None:
        legacy = {"status": "quarantined", "code": "LEGACY_SPECIFIC_CODE"}
        differences, _ = golden_match.compare_rejection(
            self.MODERN, legacy, self.CONTRACT, batch_id="B1"
        )
        codes = [item for item in differences if item.field_name == "code"]
        self.assertEqual(len(codes), 1)
        self.assertEqual(
            codes[0].classification, golden_match.APPROVED_BEHAVIOR_CHANGE
        )

    def test_skipping_legacy_asserts_nothing_about_legacy(self) -> None:
        """Regression guard.

        `compare_rejection` used to be called with a `legacy_final_status` built
        from the contract expectation, which made `legacy_matches_contract_*`
        compare the contract with itself — two checks that could not fail, and
        differences labelled `legacy-observation` although legacy was never
        read. When legacy is not consulted, the legacy checks must be absent
        rather than trivially true.
        """

        differences, checks = golden_match.compare_rejection(
            self.MODERN, None, self.CONTRACT, batch_id="B1"
        )
        self.assertEqual(differences, [])
        self.assertNotIn("legacy_matches_contract_status", checks)
        self.assertNotIn("legacy_matches_contract_code", checks)
        self.assertNotIn("legacy_terminal_observed", checks)
        self.assertTrue(checks["legacy_terminal_comparison_skipped_by_request"])
        self.assertTrue(checks["modern_matches_contract_status"])

    def test_a_preserved_source_declaration_is_a_confirmed_source_defect(self) -> None:
        modern = dict(self.MODERN)
        modern["controls"] = {
            "declared_net_amount": "173.44",
            "computed_net_amount": "173.45",
        }
        differences, checks = golden_match.compare_rejection(
            modern,
            {"status": "quarantined", "code": "INVALID_OVERPUNCH"},
            self.CONTRACT,
            batch_id="B1",
        )
        controls = [item for item in differences if item.scope == "controls"]
        self.assertEqual(len(controls), 1)
        self.assertEqual(
            controls[0].classification, golden_match.CONFIRMED_SOURCE_DEFECT
        )
        self.assertTrue(checks["source_declaration_preserved"])


class ClassificationVocabularyTest(unittest.TestCase):
    def test_no_tolerance_classification_exists(self) -> None:
        self.assertNotIn("TOLERANCE", " ".join(golden_match.CLASSIFICATIONS))

    def test_only_settled_classifications_are_explained(self) -> None:
        self.assertNotIn(golden_match.MODERN_DEFECT, golden_match.EXPLAINED)
        self.assertNotIn(golden_match.UNRESOLVED, golden_match.EXPLAINED)
        self.assertNotIn(golden_match.CONTRACT_AMBIGUITY, golden_match.EXPLAINED)


if __name__ == "__main__":
    unittest.main()
