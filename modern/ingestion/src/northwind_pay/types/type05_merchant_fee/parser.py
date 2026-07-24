"""Independent Type 05 transport and grammar parser.

Implements ``contracts/types/05-merchant-fee-assessment/layout.yaml``: strict
UTF-8 with no BOM, NFC normalization, LF endings with a required final newline,
a single-pass quote-aware semicolon lexer, decimal commas, `dd/MM/yyyy` dates,
and the exact `HALF_UP` fee calculation.

Nothing here consults the Java processor, its output, or the legacy database.
"""

from __future__ import annotations

import re
import unicodedata
from datetime import date
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

from ...common.documents import DocumentError, validate_cnpj
from .model import Assessment, ParsedBatch

HEADER = (
    "assessment_id;batch_id;merchant_id;merchant_tax_id;fee_code;description;"
    "gross_amount_brl;rate_percent;assessed_fee_brl;assessment_date"
)
FIELD_COUNT = 10
FILENAME = re.compile(r"^NW_MERCHANT_FEES_([0-9]{8})_(B[0-9]{15})\.csv$")

ASSESSMENT_ID = re.compile(r"^FEE[0-9]{13}$")
BATCH_ID = re.compile(r"^B[0-9]{15}$")
MERCHANT_ID = re.compile(r"^MER[0-9]{13}$")
FEE_CODE = re.compile(r"^[A-Z][A-Z0-9_]{1,9}$")
GROSS = re.compile(r"^(0|[1-9][0-9]{0,11}),[0-9]{2}$")
RATE = re.compile(r"^(0|[1-9][0-9]{0,2}),[0-9]{3}$")
FEE = re.compile(r"^(0|[1-9][0-9]{0,11}),[0-9]{2}$")
DIGIT_RUN_11_19 = re.compile(r"[0-9]{11,19}")
FORMULA_PREFIXES = ("=", "+", "-", "@")
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


def _lex(line: str, record_number: int) -> list[str]:
    """Single-pass quote-aware semicolon lexer.

    Tracks whether each field was quoted so the contract's "description must be
    quoted, everything else must not be" rule can be enforced, which a
    quote-agnostic split cannot express.
    """

    fields: list[str] = []
    quoted: list[bool] = []
    buffer: list[str] = []
    in_quotes = False
    was_quoted = False
    index = 0
    while index < len(line):
        character = line[index]
        if in_quotes:
            if character == '"':
                if index + 1 < len(line) and line[index + 1] == '"':
                    buffer.append('"')
                    index += 2
                    continue
                in_quotes = False
                index += 1
                continue
            buffer.append(character)
            index += 1
            continue
        if character == '"':
            if buffer:
                raise ParseError(
                    "INVALID_CSV_QUOTING", "a quote opens in the middle of a field"
                )
            in_quotes = True
            was_quoted = True
            index += 1
            continue
        if character == ";":
            fields.append("".join(buffer))
            quoted.append(was_quoted)
            buffer.clear()
            was_quoted = False
            index += 1
            continue
        buffer.append(character)
        index += 1
    if in_quotes:
        raise ParseError("INVALID_CSV_QUOTING", "a quoted field is never closed")
    fields.append("".join(buffer))
    quoted.append(was_quoted)

    if len(fields) != FIELD_COUNT:
        raise ParseError(
            "INVALID_FIELD_COUNT",
            f"record {record_number} does not have exactly ten fields",
        )
    for position, (value, is_quoted) in enumerate(zip(fields, quoted), start=1):
        if position == 6 and not is_quoted:
            raise ParseError(
                "INVALID_CSV_QUOTING", "the description field must be quoted"
            )
        if position != 6 and is_quoted:
            raise ParseError(
                "INVALID_CSV_QUOTING", "only the description field may be quoted"
            )
        if position != 6 and value != value.strip():
            raise ParseError(
                "INVALID_TRANSPORT", "whitespace outside quotes is forbidden"
            )
        if not value:
            raise ParseError("INVALID_TRANSPORT", "empty fields are forbidden")
    return fields


def _locale_decimal(value: str, pattern: re.Pattern[str], code: str) -> Decimal:
    if not pattern.match(value):
        raise ParseError(code, "a locale decimal field is not canonical")
    try:
        return Decimal(value.replace(",", "."))
    except InvalidOperation as exc:
        raise ParseError(code, "a locale decimal field is not numeric") from exc


def _validate_description(value: str, tax_id: str) -> str:
    if unicodedata.normalize("NFC", value) != value:
        raise ParseError("INVALID_DESCRIPTION", "the description is not NFC")
    if not 1 <= len(value) <= MAX_DESCRIPTION_CODEPOINTS:
        raise ParseError("INVALID_DESCRIPTION", "the description length is out of range")
    for character in value:
        category = unicodedata.category(character)
        if category in {"Cc", "Cf"} or character in {"\r", "\n"}:
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
    if tax_id and tax_id in value:
        raise ParseError(
            "INVALID_DESCRIPTION", "the description carries a restricted identifier"
        )
    return value


def calculate_fee(gross: Decimal, rate: Decimal) -> Decimal:
    """gross x rate / 100, HALF_UP at scale two, in exact decimal arithmetic."""

    return (gross * rate / Decimal(100)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )


def parse(payload: bytes, *, source_filename: str) -> ParsedBatch:
    """Parse one raw batch and compute its controls independently."""

    filename_match = FILENAME.match(source_filename)
    if filename_match is None:
        raise ParseError("INVALID_TRANSPORT", "the source filename is malformed")
    filename_date, filename_batch = filename_match.group(1), filename_match.group(2)

    if payload.startswith(b"\xef\xbb\xbf"):
        raise ParseError("INVALID_TRANSPORT", "a byte-order mark is forbidden")
    if b"\r" in payload:
        raise ParseError("INVALID_TRANSPORT", "bare CR bytes are forbidden")
    if not payload.endswith(b"\n"):
        raise ParseError("INVALID_TRANSPORT", "the file has no final newline")
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ParseError("INVALID_UTF8", "the file is not strict UTF-8") from exc

    lines = text.split("\n")[:-1]
    if any(not line for line in lines):
        raise ParseError("INVALID_TRANSPORT", "blank lines are forbidden")
    if len(lines) < 2:
        raise ParseError("INVALID_TRANSPORT", "the file has no detail rows")
    if lines[0] != HEADER:
        raise ParseError("INVALID_HEADER", "the header line is not the exact contract")

    rows: list[Assessment] = []
    seen: set[str] = set()
    for number, line in enumerate(lines[1:], start=2):
        fields = _lex(line, number)
        (
            assessment_id,
            batch_id,
            merchant_id,
            merchant_tax_id,
            fee_code,
            description,
            gross_text,
            rate_text,
            assessed_text,
            date_text,
        ) = fields

        if not ASSESSMENT_ID.match(assessment_id):
            raise ParseError("INVALID_IDENTIFIER", "the assessment identity is malformed")
        if assessment_id in seen:
            raise ParseError("DUPLICATE_IDENTIFIER", "an assessment identity repeats")
        seen.add(assessment_id)
        if not BATCH_ID.match(batch_id) or batch_id != filename_batch:
            raise ParseError("INVALID_IDENTIFIER", "a row batch differs from the filename")
        if not MERCHANT_ID.match(merchant_id):
            raise ParseError("INVALID_IDENTIFIER", "the merchant identity is malformed")
        try:
            validate_cnpj(merchant_tax_id)
        except DocumentError as exc:
            raise ParseError("INVALID_DOCUMENT", "the merchant tax identity is invalid") from exc
        if not FEE_CODE.match(fee_code):
            raise ParseError("INVALID_IDENTIFIER", "the fee code is malformed")

        gross = _locale_decimal(gross_text, GROSS, "INVALID_FIELD")
        rate = _locale_decimal(rate_text, RATE, "INVALID_FIELD")
        assessed = _locale_decimal(assessed_text, FEE, "INVALID_FIELD")
        if gross <= 0 or rate <= 0 or rate > Decimal("100.000"):
            raise ParseError("INVALID_FIELD", "gross or rate is outside its range")

        calculated = calculate_fee(gross, rate)
        if assessed != calculated:
            # The contract requires assessed_fee_must_equal_calculated_fee at
            # row level, with its own stable code. The row's declared fee is
            # never corrected to the calculated one.
            raise ParseError(
                "FEE_CALCULATION_MISMATCH",
                "an assessed fee disagrees with its HALF_UP calculation",
            )

        try:
            day, month, year = (int(part) for part in date_text.split("/"))
            assessment_date = date(year, month, day)
        except ValueError as exc:
            raise ParseError("INVALID_BUSINESS_DATE", "the assessment date is not valid") from exc
        if assessment_date.strftime("%Y%m%d") != filename_date:
            raise ParseError("INVALID_BUSINESS_DATE", "a row date differs from the filename")

        rows.append(
            Assessment(
                physical_record_number=number,
                assessment_id=assessment_id,
                batch_id=batch_id,
                merchant_id=merchant_id,
                merchant_tax_id=merchant_tax_id,
                fee_code=fee_code,
                description=_validate_description(description, merchant_tax_id),
                gross_amount=gross,
                rate_percent=rate,
                assessed_fee=assessed,
                calculated_fee=calculated,
                assessment_date=assessment_date,
            )
        )

    return ParsedBatch(
        batch_id=filename_batch,
        rows=tuple(rows),
        computed_row_count=len(rows),
        computed_gross_amount=sum(
            (row.gross_amount for row in rows), start=Decimal("0.00")
        ),
        computed_assessed_fee=sum(
            (row.assessed_fee for row in rows), start=Decimal("0.00")
        ),
        computed_calculated_fee=sum(
            (row.calculated_fee for row in rows), start=Decimal("0.00")
        ),
    )
