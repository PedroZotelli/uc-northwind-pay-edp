"""Independent Type 02 transport and grammar parser.

Implements ``contracts/types/02-instant-payment-events/layout.yaml``: strict
UTF-8 with no BOM, LF endings with a required final newline, and a single-pass
escape-aware pipe lexer where ``\\|`` and ``\\\\`` decode exactly once and any
other escape — including a dangling one — is a rejection.

Rejection codes come from the contract's ``canonical_rejection_codes``.
Nothing here consults the Java processor, its output, or the legacy database.
"""

from __future__ import annotations

import re
import unicodedata
from datetime import date
from decimal import Decimal, InvalidOperation

from ...common.documents import DocumentError, validate_cnpj, validate_cpf
from .model import Event, Header, ParsedBatch, Trailer

FILENAME = re.compile(r"^NW_INSTANT_PAYMENT_([0-9]{8})_(B[0-9]{15})\.txt$")
BATCH_ID = re.compile(r"^B[0-9]{15}$")
END_TO_END = re.compile(r"^E[0-9]{31}$")
TRANSACTION_ID = re.compile(r"^(?=.*[A-Z])[A-Z0-9]{16}$")
RETURN_CODE = re.compile(r"^[A-Z0-9]{0,4}$")
UNSIGNED = re.compile(r"^(0|[1-9][0-9]{0,15})\.[0-9]{2}$")
SIGNED = re.compile(r"^-?(0|[1-9][0-9]{0,15})\.[0-9]{2}$")
TIMESTAMP = re.compile(
    r"^([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}"
    r"(Z|[+-][0-9]{2}:[0-9]{2})$"
)
DIGIT_RUN_11_19 = re.compile(r"[0-9]{11,19}")
FORMULA_PREFIXES = ("=", "+", "-", "@")

FILE_TYPE_CODE = "PIX_EVENTS01"
LAYOUT_VERSION = "001"
MAX_RECORD_BYTES = 512
MAX_DESCRIPTION_CODEPOINTS = 80


class ParseError(ValueError):
    """The raw batch violates its transport or grammar contract.

    Codes come from ``canonical_rejection_codes`` in the type's own layout
    contract. An independent implementation that invents its own vocabulary
    turns every rejection into a spurious golden-match difference.
    """

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def _lex(line: str) -> list[str]:
    """Single-pass escape-aware pipe lexer.

    The field split happens *after* escape-aware scanning, so an escaped
    delimiter never ends a field. Splitting first and unescaping afterwards
    would decode ``\\|`` into a field boundary that the source never wrote.
    """

    fields: list[str] = []
    buffer: list[str] = []
    index = 0
    while index < len(line):
        character = line[index]
        if character == "\\":
            if index + 1 >= len(line):
                raise ParseError(
                    "INVALID_ESCAPE_SEQUENCE", "the record ends with a dangling escape"
                )
            following = line[index + 1]
            if following not in {"|", "\\"}:
                raise ParseError(
                    "INVALID_ESCAPE_SEQUENCE", "an unknown escape sequence appears"
                )
            buffer.append(following)
            index += 2
            continue
        if character == "|":
            fields.append("".join(buffer))
            buffer.clear()
            index += 1
            continue
        buffer.append(character)
        index += 1
    fields.append("".join(buffer))
    return fields


def _decimal(value: str, pattern: re.Pattern[str], code: str) -> Decimal:
    if not pattern.match(value):
        raise ParseError(code, "a decimal field is not canonical")
    try:
        return Decimal(value)
    except InvalidOperation as exc:
        raise ParseError(code, "a decimal field is not numeric") from exc


def _validate_document(document_type: str, value: str) -> str:
    if document_type not in {"CPF", "CNPJ"}:
        raise ParseError("INVALID_DOCUMENT", "the document type is not CPF or CNPJ")
    try:
        return validate_cpf(value) if document_type == "CPF" else validate_cnpj(value)
    except DocumentError as exc:
        raise ParseError("INVALID_DOCUMENT", "a document identifier is invalid") from exc


def _validate_description(value: str, documents: tuple[str, ...]) -> str:
    if unicodedata.normalize("NFC", value) != value:
        raise ParseError("INVALID_DESCRIPTION", "the description is not NFC")
    if not 1 <= len(value) <= MAX_DESCRIPTION_CODEPOINTS:
        raise ParseError("INVALID_DESCRIPTION", "the description length is out of range")
    for character in value:
        if unicodedata.category(character) in {"Cc", "Cf"}:
            raise ParseError(
                "INVALID_DESCRIPTION", "the description carries a control character"
            )
    if value.startswith(FORMULA_PREFIXES):
        raise ParseError(
            "INVALID_DESCRIPTION", "the description starts with a formula prefix"
        )
    if DIGIT_RUN_11_19.search(value):
        raise ParseError(
            "INVALID_DESCRIPTION", "the description carries a long digit run"
        )
    for document in documents:
        if document and document in value:
            raise ParseError(
                "INVALID_DESCRIPTION", "the description carries a restricted identifier"
            )
    return value


def _validate_timestamp(value: str, file_date: date) -> str:
    """Validate the instant and return the source lexeme unchanged.

    The contract requires the validated canonical source lexeme to be preserved,
    so the text is returned rather than a re-rendered instant: re-rendering
    would silently normalise an offset the source chose deliberately.
    """

    match = TIMESTAMP.match(value)
    if match is None:
        raise ParseError("INVALID_TIMESTAMP", "the event timestamp is not canonical")
    offset = match.group(4)
    if offset in {"+00:00", "-00:00"}:
        raise ParseError(
            "INVALID_TIMESTAMP", "a zero offset must be spelled Z"
        )
    try:
        stamp = date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    except ValueError as exc:
        raise ParseError("INVALID_TIMESTAMP", "the event date is not valid") from exc
    if stamp != file_date:
        raise ParseError(
            "INVALID_TIMESTAMP", "an event date differs from the header file date"
        )
    return value


def parse(payload: bytes, *, source_filename: str) -> ParsedBatch:
    """Parse one raw batch and compute its controls independently."""

    filename_match = FILENAME.match(source_filename)
    if filename_match is None:
        raise ParseError("INVALID_TRANSPORT", "the source filename is malformed")
    filename_date, filename_batch = filename_match.group(1), filename_match.group(2)

    if payload.startswith(b"\xef\xbb\xbf"):
        raise ParseError("INVALID_TRANSPORT", "a byte-order mark is forbidden")
    if b"\r" in payload:
        raise ParseError("INVALID_TRANSPORT", "CR bytes are forbidden")
    if not payload.endswith(b"\n"):
        raise ParseError("INVALID_TRANSPORT", "the file has no final newline")
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ParseError("INVALID_UTF8", "the file is not strict UTF-8") from exc

    lines = text.split("\n")[:-1]
    if any(not line for line in lines):
        raise ParseError("INVALID_TRANSPORT", "blank lines are forbidden")
    if any(len(line.encode("utf-8")) > MAX_RECORD_BYTES for line in lines):
        raise ParseError("INVALID_TRANSPORT", "a record exceeds its byte limit")
    if len(lines) < 3:
        raise ParseError("INVALID_RECORD_SEQUENCE", "the batch has too few records")

    header_fields = _lex(lines[0])
    if len(header_fields) != 5:
        raise ParseError("INVALID_FIELD_COUNT", "the header field count is wrong")
    if (
        header_fields[0] != "H"
        or header_fields[1] != FILE_TYPE_CODE
        or header_fields[2] != LAYOUT_VERSION
    ):
        raise ParseError("INVALID_RECORD_SEQUENCE", "the header is not the contract")
    if not BATCH_ID.match(header_fields[4]) or header_fields[4] != filename_batch:
        raise ParseError("INVALID_RECORD_SEQUENCE", "the header batch is wrong")
    if header_fields[3] != filename_date:
        raise ParseError("INVALID_RECORD_SEQUENCE", "the header date is wrong")
    try:
        file_date = date(
            int(header_fields[3][0:4]),
            int(header_fields[3][4:6]),
            int(header_fields[3][6:8]),
        )
    except ValueError as exc:
        raise ParseError("INVALID_RECORD_SEQUENCE", "the header date is invalid") from exc
    header = Header(file_date=file_date, batch_id=header_fields[4])

    trailer_fields = _lex(lines[-1])
    if len(trailer_fields) != 5:
        raise ParseError("INVALID_FIELD_COUNT", "the trailer field count is wrong")
    if trailer_fields[0] != "T":
        raise ParseError("INVALID_RECORD_SEQUENCE", "the last record is not a trailer")
    if not trailer_fields[1].isdigit():
        raise ParseError("INVALID_FIELD_COUNT", "the trailer count is not numeric")
    declared_net = _decimal(trailer_fields[4], SIGNED, "INVALID_AMOUNT")
    if trailer_fields[4] == "-0.00":
        raise ParseError("INVALID_AMOUNT", "negative zero is forbidden")
    trailer = Trailer(
        declared_event_count=int(trailer_fields[1]),
        declared_credit_amount=_decimal(trailer_fields[2], UNSIGNED, "INVALID_AMOUNT"),
        declared_debit_amount=_decimal(trailer_fields[3], UNSIGNED, "INVALID_AMOUNT"),
        declared_net_amount=declared_net,
    )

    events: list[Event] = []
    seen_end_to_end: set[str] = set()
    seen_transaction: set[str] = set()
    for number, line in enumerate(lines[1:-1], start=2):
        fields = _lex(line)
        if len(fields) != 13:
            raise ParseError("INVALID_FIELD_COUNT", "an event field count is wrong")
        if fields[0] != "D":
            raise ParseError(
                "INVALID_RECORD_SEQUENCE", "a non-event record is inside the body"
            )
        (
            _,
            end_to_end_id,
            transaction_id,
            payer_type,
            payer_document,
            payee_type,
            payee_document,
            timestamp,
            amount_text,
            direction,
            status,
            return_code,
            description,
        ) = fields

        if not END_TO_END.match(end_to_end_id):
            raise ParseError("INVALID_IDENTIFIER", "the end-to-end identity is malformed")
        if not TRANSACTION_ID.match(transaction_id):
            raise ParseError("INVALID_IDENTIFIER", "the transaction identity is malformed")
        if end_to_end_id in seen_end_to_end or transaction_id in seen_transaction:
            raise ParseError("DUPLICATE_IDENTIFIER", "an identity repeats in the batch")
        seen_end_to_end.add(end_to_end_id)
        seen_transaction.add(transaction_id)

        _validate_document(payer_type, payer_document)
        _validate_document(payee_type, payee_document)

        amount = _decimal(amount_text, UNSIGNED, "INVALID_AMOUNT")
        if amount <= 0:
            raise ParseError("INVALID_AMOUNT", "an event amount is not positive")
        if direction not in {"C", "D"}:
            raise ParseError("INVALID_AMOUNT", "the direction is not C or D")
        if status not in {"SETTLED", "RETURNED"}:
            raise ParseError(
                "INVALID_STATUS_RETURN_CODE", "the status is not SETTLED or RETURNED"
            )
        if not RETURN_CODE.match(return_code):
            raise ParseError(
                "INVALID_STATUS_RETURN_CODE", "the return code is malformed"
            )
        if status == "SETTLED" and return_code:
            raise ParseError(
                "INVALID_STATUS_RETURN_CODE", "a settled event carries a return code"
            )
        if status == "RETURNED" and not return_code:
            raise ParseError(
                "INVALID_STATUS_RETURN_CODE", "a returned event has no return code"
            )

        events.append(
            Event(
                physical_record_number=number,
                end_to_end_id=end_to_end_id,
                transaction_id=transaction_id,
                payer_document_type=payer_type,
                payer_document=payer_document,
                payee_document_type=payee_type,
                payee_document=payee_document,
                event_timestamp=_validate_timestamp(timestamp, header.file_date),
                amount_brl=amount,
                direction=direction,
                status=status,
                return_code=return_code,
                description=_validate_description(
                    description, (payer_document, payee_document)
                ),
            )
        )

    if not events:
        raise ParseError("INVALID_RECORD_SEQUENCE", "the batch has no event records")

    credit = sum(
        (event.amount_brl for event in events if event.direction == "C"),
        start=Decimal("0.00"),
    )
    debit = sum(
        (event.amount_brl for event in events if event.direction == "D"),
        start=Decimal("0.00"),
    )
    return ParsedBatch(
        header=header,
        events=tuple(events),
        trailer=trailer,
        computed_event_count=len(events),
        computed_credit_amount=credit,
        computed_debit_amount=debit,
        computed_net_amount=credit - debit,
    )
