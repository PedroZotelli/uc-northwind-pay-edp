"""Modern Type 05 tests: locale decimals, HALF_UP, CNPJ, quoting, and privacy."""

from __future__ import annotations

import csv
import io
import unittest
from decimal import Decimal
from pathlib import Path

from northwind_pay.common.documents import DocumentError, mask_cnpj, validate_cnpj
from northwind_pay.types.type05_merchant_fee_assessment import parser, schema, writer

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
MAIN = REPOSITORY_ROOT / "contracts" / "types" / "05-merchant-fee-assessment" / "main"


class DocumentTest(unittest.TestCase):
    def test_accepts_the_fixture_identifiers(self) -> None:
        for value in ("12345678000195", "98765432000198", "11222333000181"):
            self.assertEqual(validate_cnpj(value), value)

    def test_rejects_a_wrong_check_digit(self) -> None:
        with self.assertRaises(DocumentError):
            validate_cnpj("12345678000196")

    def test_rejects_a_repeated_digit_identifier(self) -> None:
        with self.assertRaises(DocumentError):
            validate_cnpj("11111111111111")

    def test_mask_matches_the_contract_shape(self) -> None:
        self.assertEqual(mask_cnpj("12345678000195"), "**********0195")

    def test_masking_validates_before_it_masks(self) -> None:
        """Masking an invalid identifier would launder bad data."""

        with self.assertRaises(DocumentError):
            mask_cnpj("12345678000196")


class CalculationTest(unittest.TestCase):
    def test_half_up_rounds_a_half_cent_upward(self) -> None:
        self.assertEqual(
            parser.calculate_fee(Decimal("1.00"), Decimal("0.500")),
            Decimal("0.01"),
        )

    def test_exact_calculation_needs_no_rounding(self) -> None:
        self.assertEqual(
            parser.calculate_fee(Decimal("1000.00"), Decimal("1.235")),
            Decimal("12.35"),
        )

    def test_calculation_never_uses_binary_floating_point(self) -> None:
        value = parser.calculate_fee(Decimal("0.10"), Decimal("3.000"))
        self.assertIsInstance(value, Decimal)
        self.assertEqual(value, Decimal("0.00"))


class LexerTest(unittest.TestCase):
    def _parse(self, name: str, batch_id: str, date: str = "20260723"):
        return parser.parse(
            (MAIN / f"{name}.csv").read_bytes(),
            source_filename=f"NW_MERCHANT_FEES_{date}_{batch_id}.csv",
        )

    def test_decodes_a_doubled_quote_and_an_embedded_delimiter(self) -> None:
        parsed = self._parse("valid-minimal", "B202607230000401")
        self.assertEqual(
            parsed.rows[0].description, 'Tarifa "VIP"; julho, lote A'
        )

    def test_rejects_the_malformed_batch_with_the_contract_code(self) -> None:
        with self.assertRaises(parser.ParseError) as caught:
            self._parse("malformed", "B202607230000403")
        self.assertEqual(caught.exception.code, "INVALID_CSV_QUOTING")

    def test_computes_controls_independently(self) -> None:
        parsed = self._parse("valid-minimal", "B202607230000401")
        self.assertEqual(parsed.computed_row_count, 2)
        self.assertEqual(parsed.computed_gross_amount, Decimal("1001.00"))
        self.assertEqual(parsed.computed_assessed_fee, Decimal("12.36"))

    def test_rejects_a_carriage_return(self) -> None:
        payload = (MAIN / "valid-minimal.csv").read_bytes().replace(b"\n", b"\r\n")
        with self.assertRaises(parser.ParseError) as caught:
            parser.parse(
                payload,
                source_filename="NW_MERCHANT_FEES_20260723_B202607230000401.csv",
            )
        self.assertEqual(caught.exception.code, "INVALID_TRANSPORT")


class ContractAgreementTest(unittest.TestCase):
    def test_matches_the_approved_sanitized_csv(self) -> None:
        filename = "NW_MERCHANT_FEES_20260723_B202607230000401.csv"
        parsed = parser.parse(
            (MAIN / "valid-minimal.csv").read_bytes(), source_filename=filename
        )
        declared = {
            "row_count": 2,
            "gross_amount": "1001.00",
            "assessed_fee": "12.36",
            "calculated_fee": "12.36",
        }
        sanitized = schema.sanitize(
            parsed, source_filename=filename, declared=declared
        )
        expected = list(
            csv.DictReader(
                io.StringIO((MAIN / "expected-sanitized.csv").read_text(encoding="utf-8"))
            )
        )
        self.assertEqual(len(sanitized.records), len(expected))
        for record, want in zip(sanitized.records, expected):
            self.assertEqual(record.assessment_id, want["assessment_id"])
            self.assertEqual(
                record.merchant_tax_id_masked, want["merchant_tax_id_masked"]
            )
            self.assertEqual(record.description, want["description"])
            self.assertEqual(f"{record.gross_amount_brl:.2f}", want["gross_amount_brl"])
            self.assertEqual(f"{record.rate_percent:.3f}", want["rate_percent"])
            self.assertEqual(f"{record.assessed_fee_brl:.2f}", want["assessed_fee_brl"])
            self.assertEqual(record.assessment_date, want["assessment_date"])
            self.assertEqual(record.rounding_mode, "HALF_UP")

    def test_a_wrong_declaration_is_preserved_and_rejected(self) -> None:
        filename = "NW_MERCHANT_FEES_20260723_B202607230000405.csv"
        parsed = parser.parse(
            (MAIN / "df-source-005.csv").read_bytes(), source_filename=filename
        )
        declared = {
            "row_count": 1,
            "gross_amount": "100.00",
            "assessed_fee": "0.99",
            "calculated_fee": "1.00",
        }
        with self.assertRaises(schema.SchemaError) as caught:
            schema.sanitize(parsed, source_filename=filename, declared=declared)
        self.assertEqual(
            caught.exception.code, "SOURCE_CONTROL_ASSESSED_FEE_MISMATCH"
        )
        controls = schema.controls_of(parsed, declared)
        self.assertEqual(controls.declared_assessed_fee, Decimal("0.99"))
        self.assertEqual(controls.computed_assessed_fee, Decimal("1.00"))


class WriterTest(unittest.TestCase):
    def test_schema_pins_money_and_rate_at_their_contract_scales(self) -> None:
        target = writer.schema(batch_id="B202607230000401", raw_sha256="a" * 64)
        self.assertEqual(str(target.field("gross_amount_brl").type), "decimal128(18, 2)")
        self.assertEqual(str(target.field("rate_percent").type), "decimal128(6, 3)")


if __name__ == "__main__":
    unittest.main()
