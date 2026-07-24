"""Modern Type 03 and Type 04 tests: pairing, padding, linkage, and privacy."""

from __future__ import annotations

import os
import unittest
from decimal import Decimal
from pathlib import Path

from northwind_pay.common import privacy
from northwind_pay.types.type03_payment_slip import parser as type03_parser
from northwind_pay.types.type03_payment_slip import schema as type03_schema
from northwind_pay.types.type04_ted_transfer import parser as type04_parser
from northwind_pay.types.type04_ted_transfer import schema as type04_schema

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
TYPE03 = REPOSITORY_ROOT / "contracts" / "types" / "03-payment-slip-settlement" / "main"
TYPE04 = REPOSITORY_ROOT / "contracts" / "types" / "04-ted-transfer-settlement" / "main"

KEYS = {
    "NWP_PAYMENT_REFERENCE_KEY": "northwind-pay-edp-fixture-payment-reference-key-v1",
    "NWP_PARTY_TOKEN_KEY": "northwind-pay-edp-fixture-party-key-v1",
    "NWP_ACCOUNT_TOKEN_KEY": "northwind-pay-edp-fixture-account-key-v1",
    "NWP_TED_ACCOUNT_TOKEN_KEY": "northwind-pay-edp-fixture-ted-account-key-v1",
}


class Type03Test(unittest.TestCase):
    def setUp(self) -> None:
        os.environ.update(KEYS)

    def _parse(self, name: str, batch_id: str, date: str = "20260723"):
        return type03_parser.parse(
            (TYPE03 / f"{name}.rem").read_bytes(),
            source_filename=f"NW_PAYMENT_SLIP_{date}_{batch_id}.rem",
        )

    def test_assembles_logical_rows_from_segment_pairs(self) -> None:
        parsed = self._parse("valid-minimal", "B202607230000201")
        self.assertEqual(parsed.computed_logical_count, 2)
        self.assertEqual(parsed.computed_physical_record_count, 8)
        self.assertEqual(parsed.computed_lot_count, 1)

    def test_net_is_face_minus_discount_plus_fee(self) -> None:
        parsed = self._parse("valid-minimal", "B202607230000201")
        first = parsed.rows[0]
        self.assertEqual(first.face_amount, Decimal("150.00"))
        self.assertEqual(first.discount, Decimal("5.00"))
        self.assertEqual(first.fee, Decimal("2.50"))
        self.assertEqual(first.net_amount, Decimal("147.50"))
        self.assertEqual(parsed.computed_net_amount, Decimal("198.50"))

    def test_multi_lot_batch_counts_every_lot(self) -> None:
        parsed = self._parse("multi-lot", "B202607230000204")
        self.assertGreater(parsed.computed_lot_count, 1)

    def test_rejects_the_malformed_batch(self) -> None:
        with self.assertRaises(type03_parser.ParseError):
            self._parse("malformed", "B202607230000203")

    def test_preserves_a_wrong_declaration(self) -> None:
        parsed = self._parse("df-source-003", "B202607230000205")
        self.assertEqual(parsed.trailer.declared_net_amount, Decimal("198.49"))
        self.assertEqual(parsed.computed_net_amount, Decimal("198.50"))
        with self.assertRaises(type03_schema.SchemaError) as caught:
            type03_schema.sanitize(
                parsed,
                source_filename="NW_PAYMENT_SLIP_20260723_B202607230000205.rem",
            )
        self.assertEqual(caught.exception.code, "SOURCE_CONTROL_NET_MISMATCH")

    def test_a_record_that_is_not_240_bytes_is_rejected(self) -> None:
        payload = (TYPE03 / "valid-minimal.rem").read_bytes().replace(b"~\r\n", b"\r\n", 1)
        with self.assertRaises(type03_parser.ParseError) as caught:
            type03_parser.parse(
                payload,
                source_filename="NW_PAYMENT_SLIP_20260723_B202607230000201.rem",
            )
        self.assertEqual(caught.exception.code, "INVALID_RECORD_LENGTH")

    def test_three_token_scopes_use_three_separate_keys(self) -> None:
        """A token from one scope must not be derivable from another's key."""

        reference = privacy.tokenize_with_prefix(
            "1", prefix="payref", key_variable="NWP_PAYMENT_REFERENCE_KEY"
        )
        party = privacy.tokenize_with_prefix(
            "1", prefix="party", key_variable="NWP_PARTY_TOKEN_KEY"
        )
        account = privacy.tokenize_with_prefix(
            "1", prefix="acct", key_variable="NWP_ACCOUNT_TOKEN_KEY"
        )
        digests = {value.split("_", 1)[1] for value in (reference, party, account)}
        self.assertEqual(len(digests), 3)


class Type04Test(unittest.TestCase):
    def setUp(self) -> None:
        os.environ.update(KEYS)

    def _parse(self, name: str, batch_id: str, date: str = "20260723"):
        return type04_parser.parse(
            (TYPE04 / f"{name}.dat").read_bytes(),
            source_filename=f"NW_TED_SETTLEMENT_{date}_{batch_id}.dat",
        )

    def test_pairs_a_returned_transfer_with_its_return(self) -> None:
        parsed = self._parse("valid-minimal", "B202607230000301")
        self.assertEqual(parsed.computed_transfer_count, 2)
        self.assertEqual(parsed.computed_return_count, 1)
        transfer, entry = parsed.returns[0]
        self.assertEqual(entry.original_transfer_id, transfer.transfer_id)
        self.assertEqual(entry.amount, -transfer.amount)

    def test_net_is_gross_plus_returned(self) -> None:
        parsed = self._parse("valid-minimal", "B202607230000301")
        self.assertEqual(parsed.computed_gross_amount, Decimal("1250.00"))
        self.assertEqual(parsed.computed_return_amount, Decimal("-250.00"))
        self.assertEqual(parsed.computed_net_amount, Decimal("1000.00"))

    def test_all_returned_batch_nets_to_zero(self) -> None:
        parsed = self._parse("all-returned-zero-net", "B202607230000304")
        self.assertEqual(parsed.computed_net_amount, Decimal("0.00"))

    def test_rejects_the_malformed_batch(self) -> None:
        with self.assertRaises(type04_parser.ParseError):
            self._parse("malformed", "B202607230000303")

    def test_preserves_a_wrong_declaration(self) -> None:
        parsed = self._parse("df-source-004", "B202607230000305")
        self.assertEqual(parsed.trailer.declared_net_amount, Decimal("999.99"))
        self.assertEqual(parsed.computed_net_amount, Decimal("1000.00"))
        with self.assertRaises(type04_schema.SchemaError) as caught:
            type04_schema.sanitize(
                parsed,
                source_filename="NW_TED_SETTLEMENT_20260723_B202607230000305.dat",
            )
        self.assertEqual(caught.exception.code, "SOURCE_CONTROL_NET_MISMATCH")

    def test_visible_padding_inside_a_value_is_rejected(self) -> None:
        with self.assertRaises(type04_parser.ParseError) as caught:
            type04_parser._right_trim("ABC~DEF~~")
        self.assertEqual(caught.exception.code, "INVALID_PADDING")

    def test_negative_zero_is_rejected(self) -> None:
        with self.assertRaises(type04_parser.ParseError):
            type04_parser._implied_decimal("00000000000000", "-")

    def test_account_token_binds_institution_and_branch(self) -> None:
        """The same account number at two institutions must not correlate."""

        first = privacy.tokenize_account("60701190", "0001", "000000123456")
        second = privacy.tokenize_account("87654321", "0001", "000000123456")
        self.assertNotEqual(first, second)

    def test_beneficiary_name_never_reaches_a_sanitized_record(self) -> None:
        parsed = self._parse("valid-minimal", "B202607230000301")
        sanitized = type04_schema.sanitize(
            parsed,
            source_filename="NW_TED_SETTLEMENT_20260723_B202607230000301.dat",
        )
        self.assertTrue(
            all(
                not hasattr(record, "beneficiary_name")
                for record in sanitized.records
            )
        )


if __name__ == "__main__":
    unittest.main()
