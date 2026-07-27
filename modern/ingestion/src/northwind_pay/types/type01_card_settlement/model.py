"""Typed Type 01 domain records with exact Decimal money."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Header:
    file_date: date
    batch_id: str
    file_type_code: str
    layout_version: str


@dataclass(frozen=True, slots=True)
class Detail:
    """One card settlement movement, still carrying restricted values.

    Instances of this record never leave the parser boundary. The schema layer
    converts them into sanitized records before anything is published.
    """

    physical_record_number: int
    transaction_id: str
    merchant_id: str
    pan: str
    cpf: str
    transaction_date: date
    transaction_time: time
    amount_brl: Decimal
    currency: str
    movement_code: str
    authorization_code: str
    nsu: str
    terminal_id: str


@dataclass(frozen=True, slots=True)
class Trailer:
    file_date: date
    declared_detail_count: int
    declared_net_amount: Decimal
    batch_id: str


@dataclass(frozen=True, slots=True)
class ParsedBatch:
    """A fully parsed batch plus the controls computed independently from it."""

    header: Header
    details: tuple[Detail, ...]
    trailer: Trailer
    computed_detail_count: int
    computed_net_amount: Decimal


@dataclass(frozen=True, slots=True)
class SanitizedRecord:
    """One privacy-safe record, shaped exactly like the sanitized CSV contract."""

    batch_id: str
    source_file: str
    source_record_number: int
    transaction_id: str
    merchant_id: str
    card_token: str
    card_last4: str
    cpf_masked: str
    transaction_ts: str
    amount_brl: Decimal
    movement_code: str
    authorization_code: str
    nsu: str
    terminal_id: str
