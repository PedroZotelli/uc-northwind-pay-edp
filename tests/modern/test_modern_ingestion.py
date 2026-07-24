"""Modern ingestion tests: money, privacy, parsing, and contract agreement.

Pure tests. They read the frozen contract fixtures and never need a runtime,
a lakehouse, or a legacy deployment.
"""

from __future__ import annotations

import csv
import io
import os
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from northwind_pay.common import money, privacy
from northwind_pay.intake.admission import AdmissionError, admit
from northwind_pay.types.type01_card_settlement import parser, schema, writer
from northwind_pay.types.type01_card_settlement.handler import process

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
MAIN = REPOSITORY_ROOT / "contracts" / "types" / "01-card-settlement" / "main"
FIXTURE_KEY = "northwind-pay-edp-fixture-key-v1"


class OverpunchTest(unittest.TestCase):
    def test_decodes_the_contract_examples(self) -> None:
        """Exactly the examples published in layout.yaml."""

        self.assertEqual(money.decode_overpunch("00000001234E"), Decimal("123.45"))
        self.assertEqual(money.decode_overpunch("00000000500{"), Decimal("50.00"))
        self.assertEqual(money.decode_overpunch("00000000123M"), Decimal("-12.34"))

    def test_every_sign_character_maps_to_its_index(self) -> None:
        for index, character in enumerate(money.POSITIVE_CHARACTERS):
            self.assertEqual(
                money.decode_overpunch(f"0000000000{character}"),
                Decimal(index).scaleb(-2),
            )
        for index, character in enumerate(money.NEGATIVE_CHARACTERS):
            self.assertEqual(
                money.decode_overpunch(f"0000000000{character}"),
                -Decimal(index).scaleb(-2),
            )

    def test_refuses_a_field_without_a_sign(self) -> None:
        with self.assertRaises(money.MoneyError):
            money.decode_overpunch("000000001234")

    def test_refuses_an_unknown_sign_character(self) -> None:
        with self.assertRaises(money.MoneyError):
            money.decode_overpunch("00000000123*")

    def test_money_never_becomes_a_float(self) -> None:
        value = money.decode_overpunch("00000001234E")
        self.assertIsInstance(value, Decimal)
        self.assertEqual(money.render(value), "123.45")


class PrivacyTest(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["NWP_TOKENIZATION_KEY"] = FIXTURE_KEY

    def test_token_matches_the_contract_shape(self) -> None:
        token = privacy.tokenize_pan("4111111111111111")
        self.assertRegex(token, r"^tok_[0-9a-f]{24}$")

    def test_tokenization_is_deterministic_for_one_key(self) -> None:
        self.assertEqual(
            privacy.tokenize_pan("4111111111111111"),
            privacy.tokenize_pan("4111111111111111"),
        )

    def test_a_missing_key_fails_closed(self) -> None:
        del os.environ["NWP_TOKENIZATION_KEY"]
        try:
            with self.assertRaises(privacy.PrivacyError):
                privacy.tokenize_pan("4111111111111111")
        finally:
            os.environ["NWP_TOKENIZATION_KEY"] = FIXTURE_KEY

    def test_cpf_mask_matches_the_contract_shape(self) -> None:
        self.assertEqual(privacy.mask_cpf("12345678909"), "*******8909")

    def test_error_messages_never_carry_the_value(self) -> None:
        with self.assertRaises(privacy.PrivacyError) as caught:
            privacy.tokenize_pan("41111")
        self.assertNotIn("41111", str(caught.exception))

    def test_candidate_scan_refuses_a_surviving_restricted_value(self) -> None:
        with self.assertRaises(privacy.PrivacyError):
            privacy.assert_no_restricted_values(
                "a,b,4111111111111111", ("4111111111111111",)
            )


class ParserTest(unittest.TestCase):
    def _parse(self, name: str, batch_id: str):
        payload = (MAIN / f"{name}.dat").read_bytes()
        return parser.parse(
            payload,
            source_filename=f"NW_CARD_SETTLEMENT_20260723_{batch_id}.dat",
        )

    def test_parses_the_minimal_batch_and_computes_its_controls(self) -> None:
        parsed = self._parse("valid-minimal", "B202607230000001")
        self.assertEqual(parsed.computed_detail_count, 2)
        self.assertEqual(parsed.computed_net_amount, Decimal("173.45"))
        self.assertEqual(parsed.trailer.declared_net_amount, Decimal("173.45"))

    def test_preserves_a_wrong_source_declaration_rather_than_correcting_it(self) -> None:
        parsed = self._parse("df-source-001", "B202607230000004")
        self.assertEqual(parsed.trailer.declared_net_amount, Decimal("173.44"))
        self.assertEqual(parsed.computed_net_amount, Decimal("173.45"))

    def test_rejects_the_malformed_batch(self) -> None:
        with self.assertRaises(parser.ParseError):
            self._parse("malformed", "B202607230000003")

    def test_refuses_a_filename_that_disagrees_with_the_header(self) -> None:
        payload = (MAIN / "valid-minimal.dat").read_bytes()
        with self.assertRaises(parser.ParseError) as caught:
            parser.parse(
                payload,
                source_filename="NW_CARD_SETTLEMENT_20260723_B202607230000999.dat",
            )
        self.assertEqual(caught.exception.code, "FILENAME_BATCH_MISMATCH")

    def test_refuses_a_missing_final_newline(self) -> None:
        payload = (MAIN / "valid-minimal.dat").read_bytes().rstrip(b"\n")
        with self.assertRaises(parser.ParseError) as caught:
            parser.parse(
                payload,
                source_filename="NW_CARD_SETTLEMENT_20260723_B202607230000001.dat",
            )
        self.assertEqual(caught.exception.code, "MISSING_FINAL_NEWLINE")

    def test_refuses_carriage_returns(self) -> None:
        payload = (MAIN / "valid-minimal.dat").read_bytes().replace(b"\n", b"\r\n")
        with self.assertRaises(parser.ParseError) as caught:
            parser.parse(
                payload,
                source_filename="NW_CARD_SETTLEMENT_20260723_B202607230000001.dat",
            )
        self.assertEqual(caught.exception.code, "INVALID_LINE_ENDING")


class ContractAgreementTest(unittest.TestCase):
    """The modern implementation must reproduce the approved sanitized output.

    This is the business-correctness half of golden-match, asserted against the
    frozen contract rather than against legacy, so it holds with no runtime.
    """

    def setUp(self) -> None:
        os.environ["NWP_TOKENIZATION_KEY"] = FIXTURE_KEY

    def _sanitize(self, name: str, batch_id: str):
        filename = f"NW_CARD_SETTLEMENT_20260723_{batch_id}.dat"
        if batch_id.startswith("B2024"):
            filename = f"NW_CARD_SETTLEMENT_20240229_{batch_id}.dat"
        parsed = parser.parse((MAIN / f"{name}.dat").read_bytes(), source_filename=filename)
        return schema.sanitize(parsed, source_filename=filename)

    def _expected(self, name: str) -> list[dict[str, str]]:
        return list(
            csv.DictReader(
                io.StringIO((MAIN / name).read_text(encoding="utf-8"))
            )
        )

    def test_minimal_batch_matches_the_approved_sanitized_csv(self) -> None:
        sanitized = self._sanitize("valid-minimal", "B202607230000001")
        expected = self._expected("expected-sanitized.csv")
        self.assertEqual(len(sanitized.records), len(expected))
        for record, want in zip(sanitized.records, expected):
            self.assertEqual(record.transaction_id, want["transaction_id"])
            self.assertEqual(record.card_token, want["card_token"])
            self.assertEqual(record.card_last4, want["card_last4"])
            self.assertEqual(record.cpf_masked, want["cpf_masked"])
            self.assertEqual(record.transaction_ts, want["transaction_ts"])
            self.assertEqual(money.render(record.amount_brl), want["amount_brl"])

    def test_negative_overpunch_batch_matches_the_approved_sanitized_csv(self) -> None:
        sanitized = self._sanitize("negative-overpunch", "B202607230000002")
        expected = self._expected("expected-negative-overpunch-sanitized.csv")
        self.assertEqual(
            [money.render(record.amount_brl) for record in sanitized.records],
            [row["amount_brl"] for row in expected],
        )

    def test_source_defect_produces_no_sanitized_output(self) -> None:
        with self.assertRaises(schema.SchemaError) as caught:
            self._sanitize("df-source-001", "B202607230000004")
        self.assertEqual(caught.exception.code, "SOURCE_CONTROL_TOTAL_MISMATCH")

    def test_no_record_carries_a_clear_restricted_value(self) -> None:
        sanitized = self._sanitize("valid-minimal", "B202607230000001")
        rendered = repr(sanitized.records)
        for record in sanitized.records:
            self.assertNotIn(record.card_last4 * 4, rendered)
        self.assertNotRegex(rendered, r"\b\d{16}\b")
        self.assertNotRegex(rendered, r"\b\d{11}\b")


class WriterDeterminismTest(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["NWP_TOKENIZATION_KEY"] = FIXTURE_KEY

    def test_identical_input_produces_identical_parquet_bytes(self) -> None:
        """The Parquet hash is itself the determinism check (DR-008)."""

        from northwind_pay.common.parquet import write_table

        filename = "NW_CARD_SETTLEMENT_20260723_B202607230000001.dat"
        parsed = parser.parse(
            (MAIN / "valid-minimal.dat").read_bytes(), source_filename=filename
        )
        sanitized = schema.sanitize(parsed, source_filename=filename)
        table = writer.table(
            sanitized.records, batch_id=sanitized.batch_id, raw_sha256="a" * 64
        )
        with tempfile.TemporaryDirectory() as temporary:
            first = Path(temporary) / "first.parquet"
            second = Path(temporary) / "second.parquet"
            write_table(table, first)
            write_table(table, second)
            self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_schema_pins_money_as_exact_decimal(self) -> None:
        target = writer.schema(batch_id="B202607230000001", raw_sha256="a" * 64)
        field = target.field("amount_brl")
        self.assertEqual(str(field.type), "decimal128(18, 2)")

    def test_schema_carries_immutable_provenance(self) -> None:
        target = writer.schema(batch_id="B202607230000001", raw_sha256="b" * 64)
        metadata = {key.decode(): value.decode() for key, value in target.metadata.items()}
        self.assertEqual(metadata["northwind.batch_id"], "B202607230000001")
        self.assertEqual(metadata["northwind.raw_sha256"], "b" * 64)
        self.assertEqual(metadata["northwind.contract_code"], "CRD_SETTLE01")


class AdmissionTest(unittest.TestCase):
    def test_refuses_a_bundle_without_a_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(AdmissionError) as caught:
                admit(Path(temporary), expected_type="01")
            self.assertEqual(caught.exception.code, "MISSING_MANIFEST")


class RejectedBatchPublishesNothingTest(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["NWP_TOKENIZATION_KEY"] = FIXTURE_KEY

    def test_a_source_defect_creates_no_landing_artifact(self) -> None:
        bundle = REPOSITORY_ROOT / "gen" / "output" / "B202607230000004"
        if not bundle.is_dir():
            self.skipTest("canonical bundle has not been generated")
        with tempfile.TemporaryDirectory() as temporary:
            landing = Path(temporary)
            outcome = process(bundle, landing_root=landing)
            self.assertEqual(outcome.status, "quarantined")
            self.assertEqual(outcome.code, "SOURCE_CONTROL_TOTAL_MISMATCH")
            self.assertIsNone(outcome.parquet_sha256)
            self.assertEqual(list(landing.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
