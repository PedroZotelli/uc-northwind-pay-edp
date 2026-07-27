"""Independent Type 01 transport and grammar parser.

Implements ``contracts/types/01-card-settlement/layout.yaml`` directly: ISO-8859-1,
LF line endings, a required final newline, no blank lines, exact record lengths,
fixed field positions, COBOL overpunch money, and the cross-record rules.

Nothing here consults the Java processor, its output, or the legacy database.
"""

from __future__ import annotations

import re
from datetime import date, time
from decimal import Decimal

from ...common.money import MoneyError, decode_overpunch, parse_unsigned, quantized
from .model import Detail, Header, ParsedBatch, Trailer

ENCODING = "ISO-8859-1"
HEADER_LENGTH = 40
DETAIL_LENGTH = 124
TRAILER_LENGTH = 46

BATCH_ID = re.compile(r"^B[0-9]{15}$")
ALNUM_16 = re.compile(r"^[A-Z0-9]{16}$")
ALNUM_6 = re.compile(r"^[A-Z0-9]{6}$")
FILENAME = re.compile(r"^NW_CARD_SETTLEMENT_([0-9]{8})_(B[0-9]{15})\.dat$")

FILE_TYPE_CODE = "CRD_SETTLE01"
LAYOUT_VERSION = "001"
CURRENCY = "BRL"
MOVEMENTS = ("P", "R")


class ParseError(ValueError):
    """The raw batch violates its transport or grammar contract."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def _field(record: str, start: int, end: int) -> str:
    return record[start - 1 : end]


def _parse_date(value: str, code: str) -> date:
    try:
        return date(int(value[0:4]), int(value[4:6]), int(value[6:8]))
    except ValueError as exc:
        raise ParseError(code, "date field is not a valid calendar date") from exc


def _parse_time(value: str, code: str) -> time:
    try:
        return time(int(value[0:2]), int(value[2:4]), int(value[4:6]))
    except ValueError as exc:
        raise ParseError(code, "time field is not a valid wall time") from exc


def _split_records(payload: bytes) -> list[str]:
    if not payload:
        raise ParseError("EMPTY_FILE", "the raw file is empty")
    if not payload.endswith(b"\n"):
        raise ParseError("MISSING_FINAL_NEWLINE", "the raw file has no final newline")
    if b"\r" in payload:
        raise ParseError("INVALID_LINE_ENDING", "the raw file uses CR bytes")
    text = payload.decode(ENCODING)
    records = text.split("\n")[:-1]
    if any(not record for record in records):
        raise ParseError("BLANK_LINE", "the raw file contains a blank line")
    return records


def _parse_header(record: str) -> Header:
    if len(record) != HEADER_LENGTH:
        raise ParseError("INVALID_RECORD_LENGTH", "header length is not 40 bytes")
    if _field(record, 26, 37) != FILE_TYPE_CODE:
        raise ParseError("INVALID_FILE_TYPE", "header file type code is wrong")
    if _field(record, 38, 40) != LAYOUT_VERSION:
        raise ParseError("INVALID_LAYOUT_VERSION", "header layout version is wrong")
    batch_id = _field(record, 10, 25)
    if not BATCH_ID.match(batch_id):
        raise ParseError("INVALID_BATCH_ID", "header batch identity is malformed")
    return Header(
        file_date=_parse_date(_field(record, 2, 9), "INVALID_FILE_DATE"),
        batch_id=batch_id,
        file_type_code=FILE_TYPE_CODE,
        layout_version=LAYOUT_VERSION,
    )


def _parse_detail(record: str, physical_record_number: int) -> Detail:
    if len(record) != DETAIL_LENGTH:
        raise ParseError("INVALID_RECORD_LENGTH", "detail length is not 124 bytes")

    transaction_id = _field(record, 2, 17)
    merchant_id = _field(record, 18, 33)
    pan = _field(record, 34, 49)
    cpf = _field(record, 50, 60)
    currency = _field(record, 87, 89)
    movement_code = _field(record, 90, 90)
    authorization_code = _field(record, 91, 96)
    nsu = _field(record, 97, 108)
    terminal_id = _field(record, 109, 124)

    if not ALNUM_16.match(transaction_id):
        raise ParseError("INVALID_TRANSACTION_ID", "transaction identity is malformed")
    if not ALNUM_16.match(merchant_id):
        raise ParseError("INVALID_MERCHANT_ID", "merchant identity is malformed")
    if not pan.isdigit():
        raise ParseError("INVALID_PAN", "the card number field is not numeric")
    if not cpf.isdigit():
        raise ParseError("INVALID_CPF", "the document field is not numeric")
    if currency != CURRENCY:
        raise ParseError("INVALID_CURRENCY", "detail currency is not BRL")
    if movement_code not in MOVEMENTS:
        raise ParseError("INVALID_MOVEMENT_CODE", "movement code is not P or R")
    if not ALNUM_6.match(authorization_code):
        raise ParseError("INVALID_AUTHORIZATION", "authorization code is malformed")
    if not nsu.isdigit():
        raise ParseError("INVALID_NSU", "the NSU field is not numeric")
    if not ALNUM_16.match(terminal_id):
        raise ParseError("INVALID_TERMINAL_ID", "terminal identity is malformed")

    try:
        amount = quantized(decode_overpunch(_field(record, 75, 86)))
    except MoneyError as exc:
        raise ParseError("INVALID_OVERPUNCH", "detail amount is not decodable") from exc

    if movement_code == "P" and amount <= 0:
        raise ParseError(
            "INVALID_MOVEMENT_SIGN", "a purchase must carry a positive amount"
        )
    if movement_code == "R" and amount >= 0:
        raise ParseError(
            "INVALID_MOVEMENT_SIGN", "a refund must carry a negative amount"
        )

    return Detail(
        physical_record_number=physical_record_number,
        transaction_id=transaction_id,
        merchant_id=merchant_id,
        pan=pan,
        cpf=cpf,
        transaction_date=_parse_date(
            _field(record, 61, 68), "INVALID_TRANSACTION_DATE"
        ),
        transaction_time=_parse_time(
            _field(record, 69, 74), "INVALID_TRANSACTION_TIME"
        ),
        amount_brl=amount,
        currency=CURRENCY,
        movement_code=movement_code,
        authorization_code=authorization_code,
        nsu=nsu,
        terminal_id=terminal_id,
    )


def _parse_trailer(record: str) -> Trailer:
    if len(record) != TRAILER_LENGTH:
        raise ParseError("INVALID_RECORD_LENGTH", "trailer length is not 46 bytes")
    batch_id = _field(record, 31, 46)
    if not BATCH_ID.match(batch_id):
        raise ParseError("INVALID_BATCH_ID", "trailer batch identity is malformed")
    try:
        declared_count = parse_unsigned(_field(record, 10, 15))
        declared_net = quantized(decode_overpunch(_field(record, 16, 30)))
    except MoneyError as exc:
        raise ParseError(
            "INVALID_TRAILER_CONTROL", "trailer control is not decodable"
        ) from exc
    return Trailer(
        file_date=_parse_date(_field(record, 2, 9), "INVALID_FILE_DATE"),
        declared_detail_count=declared_count,
        declared_net_amount=declared_net,
        batch_id=batch_id,
    )


def parse(payload: bytes, *, source_filename: str) -> ParsedBatch:
    """Parse one raw batch and compute its controls independently.

    Returns the parsed batch even when the source-declared controls disagree
    with the computed ones. Preserving that disagreement is the point: the
    source-owned declaration is never corrected, and deciding what to do about
    the mismatch belongs to the schema layer.
    """

    filename_match = FILENAME.match(source_filename)
    if filename_match is None:
        raise ParseError("INVALID_FILENAME", "the source filename is malformed")

    records = _split_records(payload)
    if len(records) < 3:
        raise ParseError("INVALID_RECORD_SEQUENCE", "the batch has too few records")
    if records[0][:1] != "H" or records[-1][:1] != "T":
        raise ParseError(
            "INVALID_RECORD_SEQUENCE", "the batch is not header-detail-trailer"
        )

    header = _parse_header(records[0])
    trailer = _parse_trailer(records[-1])

    details: list[Detail] = []
    seen: set[str] = set()
    for offset, record in enumerate(records[1:-1], start=2):
        if record[:1] != "D":
            raise ParseError(
                "INVALID_RECORD_SEQUENCE", "a non-detail record is inside the body"
            )
        detail = _parse_detail(record, offset)
        if detail.transaction_id in seen:
            raise ParseError(
                "DUPLICATE_TRANSACTION_ID",
                "a transaction identity repeats inside the batch",
            )
        seen.add(detail.transaction_id)
        details.append(detail)

    if not details:
        raise ParseError("INVALID_RECORD_SEQUENCE", "the batch has no detail records")

    if header.file_date != trailer.file_date:
        raise ParseError("CONTROL_DATE_MISMATCH", "header and trailer dates differ")
    if header.batch_id != trailer.batch_id:
        raise ParseError("CONTROL_BATCH_MISMATCH", "header and trailer batches differ")
    if filename_match.group(2) != header.batch_id:
        raise ParseError(
            "FILENAME_BATCH_MISMATCH", "the filename batch differs from the header"
        )
    if filename_match.group(1) != header.file_date.strftime("%Y%m%d"):
        raise ParseError(
            "FILENAME_DATE_MISMATCH", "the filename date differs from the header"
        )

    computed_net = quantized(
        sum((detail.amount_brl for detail in details), start=Decimal("0.00"))
    )
    return ParsedBatch(
        header=header,
        details=tuple(details),
        trailer=trailer,
        computed_detail_count=len(details),
        computed_net_amount=computed_net,
    )
