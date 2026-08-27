"""Validate Type 01 landing rows. Privacy already died at the parser."""

from __future__ import annotations

import re
from decimal import Decimal

from model import CPF_MASK_PREFIX, TOKEN_PREFIX, LandingRow
from parser import MONEY_QUANTUM

TOKEN_RE = re.compile(r"^tok_[0-9a-f]{24}$")
CPF_MASK_RE = re.compile(r"^\*{7}[0-9]{4}$")
LAST4_RE = re.compile(r"^[0-9]{4}$")
BATCH_RE = re.compile(r"^B[0-9]{15}$")
RAW_PAN_RE = re.compile(r"^\d{16}$")
RAW_CPF_RE = re.compile(r"^\d{11}$")


class SchemaError(ValueError):
    pass


def _forbid_clear_pii(value: str) -> None:
    if RAW_PAN_RE.fullmatch(value) or RAW_CPF_RE.fullmatch(value):
        raise SchemaError("clear PAN or CPF must not appear in landing")


def validate_row(row: LandingRow) -> None:
    if not BATCH_RE.match(row.batch_id):
        raise SchemaError("invalid batch_id")
    if not TOKEN_RE.match(row.card_token) or not row.card_token.startswith(TOKEN_PREFIX):
        raise SchemaError("invalid card_token")
    if not LAST4_RE.match(row.card_last4):
        raise SchemaError("invalid card_last4")
    if not CPF_MASK_RE.match(row.cpf_masked) or not row.cpf_masked.startswith(
        CPF_MASK_PREFIX
    ):
        raise SchemaError("invalid cpf_masked")
    if row.movement_code not in {"P", "R"}:
        raise SchemaError("invalid movement_code")
    if not isinstance(row.amount_brl, Decimal):
        raise SchemaError("amount_brl must be Decimal")
    if row.amount_brl != row.amount_brl.quantize(MONEY_QUANTUM):
        raise SchemaError("amount_brl must be scale 2")
    for field in (
        row.batch_id,
        row.source_file,
        row.transaction_id,
        row.merchant_id,
        row.card_token,
        row.card_last4,
        row.cpf_masked,
        row.transaction_ts,
        row.authorization_code,
        row.nsu,
        row.terminal_id,
    ):
        _forbid_clear_pii(field)


def validate_rows(rows: tuple[LandingRow, ...]) -> tuple[LandingRow, ...]:
    if not rows:
        raise SchemaError("accepted landing requires at least one row")
    ordered = tuple(sorted(rows, key=lambda item: item.source_record_number))
    for row in ordered:
        validate_row(row)
        if row.batch_id != ordered[0].batch_id:
            raise SchemaError("mixed batch_id in one landing file")
        if row.source_file != ordered[0].source_file:
            raise SchemaError("mixed source_file in one landing file")
    return ordered
