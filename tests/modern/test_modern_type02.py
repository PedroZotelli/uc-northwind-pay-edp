"""Modern Type 02 tests: escape-aware lexing, documents, signs, and timestamps."""

from __future__ import annotations

import csv
import io
import os
import unittest
from decimal import Decimal
from pathlib import Path

from northwind_pay.common import privacy
from northwind_pay.types.type02_instant_payment_events import parser, schema

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
MAIN = REPOSITORY_ROOT / "contracts" / "types" / "02-instant-payment-events" / "main"
DOCUMENT_KEY = "northwind-pay-edp-fixture-document-key-v1"


class LexerTest(unittest.TestCase):
    def test_an_escaped_delimiter_does_not_end_a_field(self) -> None:
        """Splitting first and unescaping later would invent a boundary."""

        self.assertEqual(parser._lex(r"a|b\|c|d"), ["a", "b|c", "d"])

    def test_an_escaped_backslash_decodes_exactly_once(self) -> None:
        self.assertEqual(parser._lex(r"a|b\\c"), ["a", "b\\c"])

    def test_a_dangling_escape_is_rejected(self) -> None:
        with self.assertRaises(parser.ParseError) as caught:
            parser._lex("a|b\\")
        self.assertEqual(caught.exception.code, "INVALID_ESCAPE_SEQUENCE")

    def test_an_unknown_escape_is_rejected(self) -> None:
        with self.assertRaises(parser.ParseError) as caught:
            parser._lex(r"a|b\nc")
        self.assertEqual(caught.exception.code, "INVALID_ESCAPE_SEQUENCE")


class ParserTest(unittest.TestCase):
    def _parse(self, name: str, batch_id: str, date: str = "20260723"):
        return parser.parse(
            (MAIN / f"{name}.txt").read_bytes(),
            source_filename=f"NW_INSTANT_PAYMENT_{date}_{batch_id}.txt",
        )

    def test_computes_credit_debit_and_net_independently(self) -> None:
        parsed = self._parse("valid-minimal", "B202607230000101")
        self.assertEqual(parsed.computed_event_count, 2)
        self.assertEqual(parsed.computed_credit_amount, Decimal("200.00"))
        self.assertEqual(parsed.computed_debit_amount, Decimal("26.55"))
        self.assertEqual(parsed.computed_net_amount, Decimal("173.45"))

    def test_preserves_a_wrong_declaration(self) -> None:
        parsed = self._parse("df-source-002", "B202607230000105")
        self.assertEqual(parsed.trailer.declared_net_amount, Decimal("173.44"))
        self.assertEqual(parsed.computed_net_amount, Decimal("173.45"))

    def test_rejects_the_malformed_batch(self) -> None:
        with self.assertRaises(parser.ParseError):
            self._parse("malformed", "B202607230000103")

    def test_signed_amount_follows_direction(self) -> None:
        parsed = self._parse("valid-minimal", "B202607230000101")
        credit = next(e for e in parsed.events if e.direction == "C")
        debit = next(e for e in parsed.events if e.direction == "D")
        self.assertGreater(credit.signed_amount, 0)
        self.assertLess(debit.signed_amount, 0)

    def test_timestamp_lexeme_is_preserved_not_renormalised(self) -> None:
        parsed = self._parse("valid-minimal", "B202607230000101")
        self.assertEqual(parsed.events[0].event_timestamp, "2026-07-23T09:00:00-03:00")


class DocumentPrivacyTest(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["NWP_DOCUMENT_TOKEN_KEY"] = DOCUMENT_KEY

    def test_token_matches_the_contract_shape(self) -> None:
        self.assertRegex(privacy.tokenize_document("12345678909"), r"^doc_[0-9a-f]{24}$")

    def test_one_correlation_scope_covers_payer_and_payee(self) -> None:
        """The same party must tokenize identically on either side."""

        self.assertEqual(
            privacy.tokenize_document("12345678909"),
            privacy.tokenize_document("12345678909"),
        )

    def test_mask_length_follows_document_length(self) -> None:
        self.assertEqual(privacy.mask_document("12345678909"), "*******8909")
        self.assertEqual(privacy.mask_document("12345678000195"), "**********0195")

    def test_a_missing_key_fails_closed(self) -> None:
        del os.environ["NWP_DOCUMENT_TOKEN_KEY"]
        try:
            with self.assertRaises(privacy.PrivacyError):
                privacy.tokenize_document("12345678909")
        finally:
            os.environ["NWP_DOCUMENT_TOKEN_KEY"] = DOCUMENT_KEY


class ContractAgreementTest(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["NWP_DOCUMENT_TOKEN_KEY"] = DOCUMENT_KEY

    def test_matches_the_approved_sanitized_csv(self) -> None:
        filename = "NW_INSTANT_PAYMENT_20260723_B202607230000101.txt"
        parsed = parser.parse(
            (MAIN / "valid-minimal.txt").read_bytes(), source_filename=filename
        )
        sanitized = schema.sanitize(parsed, source_filename=filename)
        expected = list(
            csv.DictReader(
                io.StringIO((MAIN / "expected-sanitized.csv").read_text(encoding="utf-8"))
            )
        )
        self.assertEqual(len(sanitized.records), len(expected))
        for record, want in zip(sanitized.records, expected):
            self.assertEqual(record.end_to_end_id, want["end_to_end_id"])
            self.assertEqual(record.payer_document_token, want["payer_document_token"])
            self.assertEqual(record.payer_document_masked, want["payer_document_masked"])
            self.assertEqual(record.payee_document_token, want["payee_document_token"])
            self.assertEqual(record.payee_document_masked, want["payee_document_masked"])
            self.assertEqual(f"{record.amount_brl:.2f}", want["amount_brl"])
            self.assertEqual(record.description, want["description"])

    def test_source_defect_produces_no_sanitized_output(self) -> None:
        filename = "NW_INSTANT_PAYMENT_20260723_B202607230000105.txt"
        parsed = parser.parse(
            (MAIN / "df-source-002.txt").read_bytes(), source_filename=filename
        )
        with self.assertRaises(schema.SchemaError) as caught:
            schema.sanitize(parsed, source_filename=filename)
        self.assertEqual(caught.exception.code, "SOURCE_CONTROL_NET_MISMATCH")


if __name__ == "__main__":
    unittest.main()
