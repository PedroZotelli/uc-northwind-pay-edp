"""Independent Type 04 transport and grammar parser.

Implements ``contracts/types/04-ted-transfer-settlement/layout.yaml``: strict
US-ASCII, exact CRLF transport with a required final CRLF, heterogeneous record
lengths selected by discriminator, visible tilde padding, implied decimals with
a separate sign character, and the conditional ``H (D | D R)+ T`` grammar where
status ``RT`` requires exactly one immediately following return.

Rejection codes come from the contract's ``canonical_rejection_codes``.
"""

from __future__ import annotations

import re
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal

from ...common.documents import DocumentError, validate_cnpj, validate_cpf
from .model import Header, ParsedBatch, Return, Trailer, Transfer

FILENAME = re.compile(r"^NW_TED_SETTLEMENT_([0-9]{8})_(B[0-9]{15})\.dat$")
BATCH_ID = re.compile(r"^B[0-9]{15}$")
MOVEMENT_ID = re.compile(r"^[A-Z][A-Z0-9]{15}$")
PURPOSE_CODE = re.compile(r"^[A-Z][A-Z0-9_]{1,9}$")
REASON_CODE = re.compile(r"^[A-Z][A-Z0-9]{4}$")
SAFE_TEXT = re.compile(r"^[A-Z][A-Z0-9 .&/-]{0,23}$")
ISPB = re.compile(r"^[0-9]{8}$")

HEADER_LENGTH = 56
TRANSFER_LENGTH = 162
RETURN_LENGTH = 91
TRAILER_LENGTH = 82

FILE_TYPE_CODE = "TED_SETTLE04"
LAYOUT_VERSION = "001"
PADDING = "~"

# The contract fixes America/Sao_Paulo, which has had no DST transition since
# 2019, so the offset is applied as a contract constant rather than through a
# platform timezone database whose contents can change under the same code.
SAO_PAULO = timezone(timedelta(hours=-3))


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


def _right_trim(value: str, code: str = "INVALID_PADDING") -> str:
    """Strip visible tilde padding, refusing padding inside the value."""

    trimmed = value.rstrip(PADDING)
    if PADDING in trimmed:
        raise ParseError(code, "visible padding appears inside a field")
    return trimmed


def _implied_decimal(digits: str, sign: str, code: str = "INVALID_FIELD") -> Decimal:
    if not digits.isdigit():
        raise ParseError(code, "an implied-decimal field is not numeric")
    if sign not in {"+", "-"}:
        raise ParseError(code, "an amount sign is not plus or minus")
    value = Decimal(digits).scaleb(-2)
    if sign == "-" and value == 0:
        raise ParseError(code, "negative zero is forbidden")
    return -value if sign == "-" else value


def _date(value: str, code: str = "INVALID_FIELD") -> date:
    try:
        return date(int(value[0:4]), int(value[4:6]), int(value[6:8]))
    except ValueError as exc:
        raise ParseError(code, "a date field is not a valid calendar date") from exc


def _time(value: str, code: str = "INVALID_FIELD") -> time:
    try:
        return time(int(value[0:2]), int(value[2:4]), int(value[4:6]))
    except ValueError as exc:
        raise ParseError(code, "a time field is not a valid wall time") from exc


def _document(party_type: str, transport: str) -> str:
    """Validate a party document under its transport rule.

    Type ``F`` arrives as ``000`` plus an 11-digit CPF; type ``J`` is a 14-digit
    CNPJ. Returning the logical document — not the transport padding — is what
    lets masking be length-aware downstream.
    """

    if party_type == "F":
        if not transport.startswith("000"):
            raise ParseError("INVALID_DOCUMENT", "a natural-person document is unpadded")
        document = transport[3:]
        try:
            return validate_cpf(document)
        except DocumentError as exc:
            raise ParseError("INVALID_DOCUMENT", "a party document is invalid") from exc
    if party_type == "J":
        try:
            return validate_cnpj(transport)
        except DocumentError as exc:
            raise ParseError("INVALID_DOCUMENT", "a party document is invalid") from exc
    raise ParseError("INVALID_FIELD", "a party type is not F or J")


def _parse_header(record: str, filename_date: str, filename_batch: str) -> Header:
    if _field(record, 26, 37) != FILE_TYPE_CODE:
        raise ParseError("INVALID_FIELD", "the header file type code is wrong")
    if _field(record, 38, 40) != LAYOUT_VERSION:
        raise ParseError("INVALID_FIELD", "the header layout version is wrong")
    batch_id = _field(record, 10, 25)
    if not BATCH_ID.match(batch_id) or batch_id != filename_batch:
        raise ParseError("INVALID_RECORD_SEQUENCE", "the header batch is wrong")
    file_date = _date(_field(record, 2, 9))
    settlement_date = _date(_field(record, 41, 48))
    if file_date.strftime("%Y%m%d") != filename_date:
        raise ParseError("INVALID_RECORD_SEQUENCE", "the header date is wrong")
    if settlement_date != file_date:
        raise ParseError(
            "INVALID_RECORD_SEQUENCE", "the settlement date differs from the file date"
        )
    origin_ispb = _field(record, 49, 56)
    if not ISPB.match(origin_ispb):
        raise ParseError("INVALID_FIELD", "the origin institution code is malformed")
    return Header(
        file_date=file_date,
        batch_id=batch_id,
        settlement_date=settlement_date,
        origin_ispb=origin_ispb,
    )


def _parse_transfer(record: str, number: int, settlement_date: date) -> Transfer:
    transfer_id = _field(record, 2, 17)
    if not MOVEMENT_ID.match(transfer_id):
        raise ParseError("INVALID_IDENTIFIER", "a transfer identity is malformed")
    amount = _implied_decimal(_field(record, 19, 32), _field(record, 18, 18))
    if amount <= 0:
        raise ParseError("INVALID_FIELD", "a transfer amount is not positive")
    if _field(record, 33, 35) != "BRL":
        raise ParseError("INVALID_FIELD", "a transfer currency is not BRL")

    transfer_date = _date(_field(record, 36, 43))
    if transfer_date != settlement_date:
        raise ParseError(
            "INVALID_TIMESTAMP", "a transfer date differs from the settlement date"
        )
    moment = datetime.combine(
        transfer_date, _time(_field(record, 44, 49)), tzinfo=SAO_PAULO
    )

    for start, end in ((50, 57), (89, 96)):
        if not ISPB.match(_field(record, start, end)):
            raise ParseError("INVALID_FIELD", "an institution code is malformed")
    for start, end in ((58, 61), (97, 100)):
        if not _field(record, start, end).isdigit():
            raise ParseError("INVALID_FIELD", "a branch code is malformed")
    for start, end in ((62, 73), (101, 112)):
        if not _field(record, start, end).isdigit():
            raise ParseError("INVALID_FIELD", "an account number is malformed")

    payer_party_type = _field(record, 88, 88)
    beneficiary_party_type = _field(record, 127, 127)
    purpose_code = _right_trim(_field(record, 128, 137))
    if not PURPOSE_CODE.match(purpose_code):
        raise ParseError("INVALID_IDENTIFIER", "a purpose code is malformed")
    status_code = _field(record, 138, 139)
    if status_code not in {"OK", "RT"}:
        raise ParseError("INVALID_FIELD", "a status code is not OK or RT")

    # The beneficiary name is validated and then discarded: the privacy contract
    # marks it a prohibited output, so it never enters a domain record at all.
    beneficiary_name = _right_trim(_field(record, 140, 162))
    if not SAFE_TEXT.match(beneficiary_name):
        raise ParseError("INVALID_IDENTIFIER", "a beneficiary name is malformed")

    return Transfer(
        physical_record_number=number,
        transfer_id=transfer_id,
        amount=amount,
        moment=moment,
        payer_ispb=_field(record, 50, 57),
        payer_branch=_field(record, 58, 61),
        payer_account=_field(record, 62, 73),
        payer_tax_id=_document(payer_party_type, _field(record, 74, 87)),
        payer_party_type=payer_party_type,
        beneficiary_ispb=_field(record, 89, 96),
        beneficiary_branch=_field(record, 97, 100),
        beneficiary_account=_field(record, 101, 112),
        beneficiary_tax_id=_document(
            beneficiary_party_type, _field(record, 113, 126)
        ),
        beneficiary_party_type=beneficiary_party_type,
        purpose_code=purpose_code,
        status_code=status_code,
    )


def _parse_return(record: str, number: int, transfer: Transfer) -> Return:
    return_id = _field(record, 2, 17)
    original_transfer_id = _field(record, 18, 33)
    if not MOVEMENT_ID.match(return_id) or not MOVEMENT_ID.match(original_transfer_id):
        raise ParseError("INVALID_IDENTIFIER", "a return identity is malformed")
    if original_transfer_id != transfer.transfer_id:
        raise ParseError(
            "RETURN_LINK_MISMATCH", "a return does not name the transfer it follows"
        )
    amount = _implied_decimal(_field(record, 35, 48), _field(record, 34, 34))
    if -amount != transfer.amount:
        raise ParseError(
            "RETURN_LINK_MISMATCH", "a return is not the full transfer amount"
        )
    moment = datetime.combine(
        _date(_field(record, 49, 56)), _time(_field(record, 57, 62)), tzinfo=SAO_PAULO
    )
    if moment <= transfer.moment:
        raise ParseError(
            "INVALID_TIMESTAMP", "a return is not strictly after its transfer"
        )
    reason_code = _field(record, 63, 67)
    if not REASON_CODE.match(reason_code):
        raise ParseError("INVALID_IDENTIFIER", "a return reason code is malformed")
    reason_text = _right_trim(_field(record, 68, 91))
    if not SAFE_TEXT.match(reason_text):
        raise ParseError("INVALID_IDENTIFIER", "a return reason text is malformed")
    return Return(
        physical_record_number=number,
        return_id=return_id,
        original_transfer_id=original_transfer_id,
        amount=amount,
        moment=moment,
        reason_code=reason_code,
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
    if any(not record for record in records):
        raise ParseError("INVALID_TRANSPORT", "blank lines are forbidden")
    if len(records) < 3:
        raise ParseError("INVALID_RECORD_SEQUENCE", "the batch has too few records")

    if records[0][:1] != "H" or len(records[0]) != HEADER_LENGTH:
        raise ParseError("INVALID_RECORD_LENGTH", "the header is malformed")
    if records[-1][:1] != "T" or len(records[-1]) != TRAILER_LENGTH:
        raise ParseError("INVALID_RECORD_LENGTH", "the trailer is malformed")

    header = _parse_header(records[0], filename_date, filename_batch)

    trailer_record = records[-1]
    if _field(trailer_record, 67, 82) != header.batch_id:
        raise ParseError("INVALID_RECORD_SEQUENCE", "the trailer batch is wrong")
    if _date(_field(trailer_record, 2, 9)) != header.file_date:
        raise ParseError("INVALID_RECORD_SEQUENCE", "the trailer date is wrong")
    for start, end in ((10, 15), (16, 21)):
        if not _field(trailer_record, start, end).isdigit():
            raise ParseError("INVALID_FIELD", "a trailer count is not numeric")
    trailer = Trailer(
        declared_transfer_count=int(_field(trailer_record, 10, 15)),
        declared_return_count=int(_field(trailer_record, 16, 21)),
        declared_gross_amount=_implied_decimal(
            _field(trailer_record, 23, 36), _field(trailer_record, 22, 22)
        ),
        declared_return_amount=_implied_decimal(
            _field(trailer_record, 38, 51), _field(trailer_record, 37, 37)
        ),
        declared_net_amount=_implied_decimal(
            _field(trailer_record, 53, 66), _field(trailer_record, 52, 52)
        ),
    )

    transfers: list[Transfer] = []
    returns: list[tuple[Transfer, Return]] = []
    identities: set[str] = set()
    index = 1
    while index < len(records) - 1:
        record = records[index]
        if record[:1] != "D" or len(record) != TRANSFER_LENGTH:
            raise ParseError("INVALID_RECORD_LENGTH", "a body record is not a transfer")
        transfer = _parse_transfer(record, index + 1, header.settlement_date)
        if transfer.transfer_id in identities:
            raise ParseError("DUPLICATE_IDENTIFIER", "a movement identity repeats")
        identities.add(transfer.transfer_id)
        transfers.append(transfer)
        index += 1

        if transfer.status_code == "RT":
            if index >= len(records) - 1:
                raise ParseError(
                    "INVALID_RECORD_SEQUENCE", "a returned transfer has no return"
                )
            follower = records[index]
            if follower[:1] != "R" or len(follower) != RETURN_LENGTH:
                raise ParseError(
                    "INVALID_RECORD_SEQUENCE", "a returned transfer has no return"
                )
            entry = _parse_return(follower, index + 1, transfer)
            if entry.return_id in identities:
                raise ParseError("DUPLICATE_IDENTIFIER", "a movement identity repeats")
            identities.add(entry.return_id)
            returns.append((transfer, entry))
            index += 1
        elif index < len(records) - 1 and records[index][:1] == "R":
            raise ParseError(
                "INVALID_RECORD_SEQUENCE", "a settled transfer is followed by a return"
            )

    if not transfers:
        raise ParseError("INVALID_RECORD_SEQUENCE", "the batch has no transfers")

    gross = sum((item.amount for item in transfers), start=Decimal("0.00"))
    returned = sum((entry.amount for _, entry in returns), start=Decimal("0.00"))
    return ParsedBatch(
        header=header,
        transfers=tuple(transfers),
        returns=tuple(returns),
        trailer=trailer,
        computed_transfer_count=len(transfers),
        computed_return_count=len(returns),
        computed_gross_amount=gross,
        computed_return_amount=returned,
        computed_net_amount=gross + returned,
    )
