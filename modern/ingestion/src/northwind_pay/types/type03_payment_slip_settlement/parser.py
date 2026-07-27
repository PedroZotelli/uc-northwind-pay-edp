"""Independent Type 03 transport and grammar parser.

Implements ``contracts/types/03-payment-slip-settlement/layout.yaml``: strict
US-ASCII, exact CRLF transport with a required final CRLF, exact 240-byte
records, visible ``~`` filler, and the ``H (L (A B)+ T)+ Z`` grammar where a
logical settlement is an adjacent A/B segment pair sharing lot, sequence, and
settlement identity.

Rejection codes come from the contract's ``canonical_rejection_codes``.
"""

from __future__ import annotations

import re
from datetime import date
from decimal import Decimal

from ...common.documents import DocumentError, validate_cnpj, validate_cpf
from .model import LogicalRow, ParsedBatch, Trailer

FILENAME = re.compile(r"^NW_PAYMENT_SLIP_([0-9]{8})_(B[0-9]{15})\.rem$")
BATCH_ID = re.compile(r"^B[0-9]{15}$")
LOT_NUMBER = re.compile(r"^(?!000000)[0-9]{6}$")
SETTLEMENT_ID = re.compile(r"^[A-Z][A-Z0-9]{15}$")
REFERENCE_20 = re.compile(r"^[A-Z][A-Z0-9]{19}$")
BANK_CODE = re.compile(r"^(?!000$)[0-9]{3}$")
NAME = re.compile(r"^[A-Z][A-Z0-9 .&/-]{0,39}$")

RECORD_LENGTH = 240
FILE_TYPE_CODE = "PAYSLIPSET03"
LAYOUT_VERSION = "001"
ORIGIN_BANK_CODE = "NWP00001"
SERVICE_CODE = "SLIPSETTLE01"
FILLER = "~"


class ParseError(ValueError):
    """The raw batch violates its transport or grammar contract.

    Codes come from ``canonical_rejection_codes`` in the type's own layout
    contract.
    """

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def _field(record: str, start: int, end: int) -> str:
    return record[start - 1 : end]


def _filler(record: str, start: int) -> None:
    if set(_field(record, start, RECORD_LENGTH)) != {FILLER}:
        raise ParseError("INVALID_FILLER", "reserved filler is not the contract byte")


def _implied(digits: str, code: str = "INVALID_FIELD") -> Decimal:
    if not digits.isdigit():
        raise ParseError(code, "an implied-decimal field is not numeric")
    return Decimal(digits).scaleb(-2)


def _date(value: str, code: str = "INVALID_FIELD") -> date:
    try:
        return date(int(value[0:4]), int(value[4:6]), int(value[6:8]))
    except ValueError as exc:
        raise ParseError(code, "a date field is not a valid calendar date") from exc


def _tax_id(tax_id_type: str, transport: str) -> str:
    if tax_id_type == "1":
        if not transport.startswith("000"):
            raise ParseError("INVALID_DOCUMENT", "a natural-person document is unpadded")
        try:
            return validate_cpf(transport[3:])
        except DocumentError as exc:
            raise ParseError("INVALID_DOCUMENT", "a beneficiary document is invalid") from exc
    if tax_id_type == "2":
        try:
            return validate_cnpj(transport)
        except DocumentError as exc:
            raise ParseError("INVALID_DOCUMENT", "a beneficiary document is invalid") from exc
    raise ParseError("INVALID_FIELD", "a tax identifier type is not 1 or 2")


def _pair(
    a_record: str,
    b_record: str,
    number_a: int,
    number_b: int,
    settlement_date: date,
) -> LogicalRow:
    """Assemble one logical row from an adjacent A/B pair."""

    lot_number = _field(a_record, 2, 7)
    sequence = _field(a_record, 8, 13)
    settlement_id = _field(a_record, 14, 29)
    for value, pattern, code in (
        (lot_number, LOT_NUMBER, "INVALID_FIELD"),
        (sequence, LOT_NUMBER, "INVALID_FIELD"),
        (settlement_id, SETTLEMENT_ID, "INVALID_IDENTIFIER"),
    ):
        if not pattern.match(value):
            raise ParseError(code, "a segment key field is malformed")

    # The pair must agree on all three keys; a disagreement means the file's
    # segments are misaligned, which is a pairing failure rather than a field
    # failure and has its own code.
    if (
        _field(b_record, 2, 7) != lot_number
        or _field(b_record, 8, 13) != sequence
        or _field(b_record, 14, 29) != settlement_id
    ):
        raise ParseError(
            "SEGMENT_PAIR_MISMATCH", "an A and B segment pair does not agree on its keys"
        )

    payment_reference = _field(a_record, 30, 77)
    if not payment_reference.isdigit():
        raise ParseError("INVALID_FIELD", "a payment reference is not numeric")
    face = _implied(_field(a_record, 78, 92))
    if face <= 0:
        raise ParseError("INVALID_FIELD", "a face amount is not positive")
    due_date = _date(_field(a_record, 93, 100))
    payment_date = _date(_field(a_record, 101, 108))
    discount = _implied(_field(a_record, 109, 120))
    fee = _implied(_field(a_record, 121, 132))
    if discount > face:
        raise ParseError("INVALID_FIELD", "a discount exceeds its face amount")
    if payment_date != settlement_date:
        raise ParseError(
            "INVALID_BUSINESS_DATE", "a payment date differs from its lot settlement date"
        )
    if payment_date > due_date:
        raise ParseError("INVALID_BUSINESS_DATE", "a payment date is after its due date")
    if _field(a_record, 133, 134) != "00":
        raise ParseError("INVALID_FIELD", "a settlement status is not the contract value")
    bank_reference = _field(a_record, 135, 154)
    if not REFERENCE_20.match(bank_reference):
        raise ParseError("INVALID_IDENTIFIER", "a bank reference is malformed")
    _filler(a_record, 155)

    tax_id_type = _field(b_record, 30, 30)
    beneficiary_tax_id = _tax_id(tax_id_type, _field(b_record, 31, 44))
    beneficiary_name = _field(b_record, 45, 84).rstrip(" ")
    if not NAME.match(beneficiary_name):
        raise ParseError("INVALID_IDENTIFIER", "a beneficiary name is malformed")
    bank_code = _field(b_record, 85, 87)
    branch_number = _field(b_record, 88, 92)
    account_number = _field(b_record, 93, 104)
    account_check_digit = _field(b_record, 105, 105)
    client_reference = _field(b_record, 106, 125)
    if not BANK_CODE.match(bank_code):
        raise ParseError("INVALID_FIELD", "a bank code is malformed")
    if not branch_number.isdigit() or not account_number.isdigit():
        raise ParseError("INVALID_FIELD", "a branch or account number is malformed")
    if not re.match(r"^[A-Z0-9]$", account_check_digit):
        raise ParseError("INVALID_FIELD", "an account check digit is malformed")
    if not REFERENCE_20.match(client_reference):
        raise ParseError("INVALID_IDENTIFIER", "a client reference is malformed")
    _filler(b_record, 126)

    return LogicalRow(
        record_number_a=number_a,
        record_number_b=number_b,
        lot_number=lot_number,
        sequence=sequence,
        settlement_id=settlement_id,
        payment_reference=payment_reference,
        face_amount=face,
        due_date=due_date,
        payment_date=payment_date,
        discount=discount,
        fee=fee,
        status_code="SETTLED",
        bank_reference=bank_reference,
        tax_id_type=tax_id_type,
        beneficiary_tax_id=beneficiary_tax_id,
        beneficiary_name=beneficiary_name,
        bank_code=bank_code,
        branch_number=branch_number,
        account_number=account_number,
        account_check_digit=account_check_digit,
        client_reference=client_reference,
    )


def parse(payload: bytes, *, source_filename: str) -> ParsedBatch:
    """Parse one raw batch and compute its controls independently."""

    filename_match = FILENAME.match(source_filename)
    if filename_match is None:
        raise ParseError("INVALID_TRANSPORT", "the source filename is malformed")
    filename_date, filename_batch = filename_match.group(1), filename_match.group(2)

    try:
        text = payload.decode("ascii")
    except UnicodeDecodeError as exc:
        raise ParseError("INVALID_ASCII", "the file is not strict US-ASCII") from exc
    if not text.endswith("\r\n"):
        raise ParseError("INVALID_TRANSPORT", "the file has no final CRLF")
    records = text.split("\r\n")[:-1]
    if any("\r" in record or "\n" in record for record in records):
        raise ParseError("INVALID_TRANSPORT", "a bare CR or LF byte appears")
    if any(len(record) != RECORD_LENGTH for record in records):
        raise ParseError("INVALID_RECORD_LENGTH", "a record is not exactly 240 bytes")
    if len(records) < 6:
        raise ParseError("INVALID_RECORD_SEQUENCE", "the batch has too few records")

    header = records[0]
    if header[:1] != "H":
        raise ParseError("INVALID_RECORD_SEQUENCE", "the first record is not a header")
    if _field(header, 26, 37) != FILE_TYPE_CODE or _field(header, 38, 40) != LAYOUT_VERSION:
        raise ParseError("INVALID_FIELD", "the header identity is wrong")
    if _field(header, 41, 48) != ORIGIN_BANK_CODE:
        raise ParseError("INVALID_FIELD", "the origin bank code is wrong")
    batch_id = _field(header, 10, 25)
    if not BATCH_ID.match(batch_id) or batch_id != filename_batch:
        raise ParseError("INVALID_RECORD_SEQUENCE", "the header batch is wrong")
    file_date = _date(_field(header, 2, 9))
    if file_date.strftime("%Y%m%d") != filename_date:
        raise ParseError("INVALID_RECORD_SEQUENCE", "the header date is wrong")
    file_sequence = _field(header, 49, 54)
    if file_sequence != batch_id[-6:]:
        raise ParseError(
            "INVALID_FIELD", "the file sequence is not the batch identity suffix"
        )
    _filler(header, 55)

    trailer_record = records[-1]
    if trailer_record[:1] != "Z":
        raise ParseError("INVALID_RECORD_SEQUENCE", "the last record is not a trailer")
    for start, end in ((2, 7), (8, 13), (14, 19)):
        if not _field(trailer_record, start, end).isdigit():
            raise ParseError("INVALID_FIELD", "a file trailer count is not numeric")
    if _field(trailer_record, 35, 50) != batch_id:
        raise ParseError("INVALID_RECORD_SEQUENCE", "the file trailer batch is wrong")
    _filler(trailer_record, 51)
    trailer = Trailer(
        declared_lot_count=int(_field(trailer_record, 2, 7)),
        declared_physical_record_count=int(_field(trailer_record, 8, 13)),
        declared_logical_count=int(_field(trailer_record, 14, 19)),
        declared_net_amount=_implied(_field(trailer_record, 20, 34)),
    )

    rows: list[LogicalRow] = []
    settlement_ids: set[str] = set()
    lot_numbers: set[str] = set()
    declared_face = Decimal("0.00")
    declared_discount = Decimal("0.00")
    declared_fee = Decimal("0.00")
    lot_count = 0
    orphan_segments = 0

    index = 1
    while index < len(records) - 1:
        lot_header = records[index]
        if lot_header[:1] != "L":
            raise ParseError("INVALID_RECORD_SEQUENCE", "a lot header was expected")
        lot_number = _field(lot_header, 2, 7)
        if not LOT_NUMBER.match(lot_number):
            raise ParseError("INVALID_FIELD", "a lot number is malformed")
        if lot_number in lot_numbers:
            raise ParseError("DUPLICATE_IDENTIFIER", "a lot number repeats in the batch")
        lot_numbers.add(lot_number)
        if _field(lot_header, 8, 19) != SERVICE_CODE:
            raise ParseError("INVALID_FIELD", "a lot service code is wrong")
        if _field(lot_header, 20, 22) != "BRL":
            raise ParseError("INVALID_FIELD", "a lot currency is not BRL")
        settlement_date = _date(_field(lot_header, 23, 30))
        if _field(lot_header, 31, 46) != batch_id:
            raise ParseError("INVALID_RECORD_SEQUENCE", "a lot batch is wrong")
        if not SETTLEMENT_ID.match(_field(lot_header, 47, 62)):
            raise ParseError("INVALID_IDENTIFIER", "a lot originator is malformed")
        _filler(lot_header, 63)
        lot_count += 1
        index += 1

        lot_rows: list[LogicalRow] = []
        sequences: set[str] = set()
        while index < len(records) - 1 and records[index][:1] == "A":
            if index + 1 >= len(records) - 1 or records[index + 1][:1] != "B":
                orphan_segments += 1
                raise ParseError(
                    "SEGMENT_PAIR_MISMATCH", "a financial segment has no beneficiary pair"
                )
            row = _pair(
                records[index], records[index + 1], index + 1, index + 2, settlement_date
            )
            if row.lot_number != lot_number:
                raise ParseError(
                    "INVALID_RECORD_SEQUENCE", "a segment belongs to a different lot"
                )
            if row.sequence in sequences:
                raise ParseError("DUPLICATE_IDENTIFIER", "a segment sequence repeats")
            if row.settlement_id in settlement_ids:
                raise ParseError("DUPLICATE_IDENTIFIER", "a settlement identity repeats")
            sequences.add(row.sequence)
            settlement_ids.add(row.settlement_id)
            lot_rows.append(row)
            index += 2

        if not lot_rows:
            raise ParseError("INVALID_RECORD_SEQUENCE", "a lot has no settlements")
        if index >= len(records) - 1 or records[index][:1] != "T":
            raise ParseError("INVALID_RECORD_SEQUENCE", "a lot trailer was expected")

        lot_trailer = records[index]
        if _field(lot_trailer, 2, 7) != lot_number:
            raise ParseError("INVALID_RECORD_SEQUENCE", "a lot trailer names another lot")
        if _field(lot_trailer, 74, 89) != batch_id:
            raise ParseError("INVALID_RECORD_SEQUENCE", "a lot trailer batch is wrong")
        if not _field(lot_trailer, 8, 13).isdigit():
            raise ParseError("INVALID_FIELD", "a lot trailer count is not numeric")
        _filler(lot_trailer, 90)

        # Lot-level declarations are accumulated rather than enforced here: the
        # schema layer owns control comparison so that a disagreement becomes a
        # source-control finding rather than a parse failure.
        declared_face += _implied(_field(lot_trailer, 14, 28))
        declared_discount += _implied(_field(lot_trailer, 29, 43))
        declared_fee += _implied(_field(lot_trailer, 44, 58))
        rows.extend(lot_rows)
        index += 1

    if not rows:
        raise ParseError("INVALID_RECORD_SEQUENCE", "the batch has no settlements")

    return ParsedBatch(
        batch_id=batch_id,
        rows=tuple(rows),
        trailer=trailer,
        declared_face_amount=declared_face,
        declared_discount_amount=declared_discount,
        declared_fee_amount=declared_fee,
        computed_lot_count=lot_count,
        computed_physical_record_count=len(records),
        computed_logical_count=len(rows),
        computed_face_amount=sum(
            (row.face_amount for row in rows), start=Decimal("0.00")
        ),
        computed_discount_amount=sum(
            (row.discount for row in rows), start=Decimal("0.00")
        ),
        computed_fee_amount=sum((row.fee for row in rows), start=Decimal("0.00")),
        computed_net_amount=sum(
            (row.net_amount for row in rows), start=Decimal("0.00")
        ),
        computed_orphan_segment_count=orphan_segments,
    )
