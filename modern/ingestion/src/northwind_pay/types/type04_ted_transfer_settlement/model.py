"""Typed Type 04 domain records with exact Decimal money."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Header:
    file_date: date
    batch_id: str
    settlement_date: date
    origin_ispb: str


@dataclass(frozen=True, slots=True)
class Transfer:
    """One outbound transfer, still carrying restricted party data."""

    physical_record_number: int
    transfer_id: str
    amount: Decimal
    moment: datetime
    payer_ispb: str
    payer_branch: str
    payer_account: str
    payer_tax_id: str
    payer_party_type: str
    beneficiary_ispb: str
    beneficiary_branch: str
    beneficiary_account: str
    beneficiary_tax_id: str
    beneficiary_party_type: str
    purpose_code: str
    status_code: str


@dataclass(frozen=True, slots=True)
class Return:
    """One full return, linked to the transfer it immediately follows."""

    physical_record_number: int
    return_id: str
    original_transfer_id: str
    amount: Decimal
    moment: datetime
    reason_code: str


@dataclass(frozen=True, slots=True)
class Trailer:
    declared_transfer_count: int
    declared_return_count: int
    declared_gross_amount: Decimal
    declared_return_amount: Decimal
    declared_net_amount: Decimal


@dataclass(frozen=True, slots=True)
class ParsedBatch:
    header: Header
    transfers: tuple[Transfer, ...]
    returns: tuple[tuple[Transfer, Return], ...]
    trailer: Trailer
    computed_transfer_count: int
    computed_return_count: int
    computed_gross_amount: Decimal
    computed_return_amount: Decimal
    computed_net_amount: Decimal


@dataclass(frozen=True, slots=True)
class SanitizedRecord:
    batch_id: str
    source_file: str
    source_record_number: int
    movement_id: str
    original_transfer_id: str
    movement_kind: str
    movement_ts: str
    amount_brl: Decimal
    payer_account_token: str
    payer_tax_id_masked: str
    beneficiary_account_token: str
    beneficiary_tax_id_masked: str
    beneficiary_ispb: str
    purpose_code: str
    status_code: str
    return_reason_code: str
