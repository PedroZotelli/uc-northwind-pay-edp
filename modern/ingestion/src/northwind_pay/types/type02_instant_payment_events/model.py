"""Typed Type 02 domain records with exact Decimal money."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Header:
    file_date: date
    batch_id: str


@dataclass(frozen=True, slots=True)
class Event:
    """One instant-payment event, still carrying restricted documents."""

    physical_record_number: int
    end_to_end_id: str
    transaction_id: str
    payer_document_type: str
    payer_document: str
    payee_document_type: str
    payee_document: str
    event_timestamp: str
    amount_brl: Decimal
    direction: str
    status: str
    return_code: str
    description: str

    @property
    def signed_amount(self) -> Decimal:
        """C is positive and D is negative; derived exactly once, here."""

        return self.amount_brl if self.direction == "C" else -self.amount_brl


@dataclass(frozen=True, slots=True)
class Trailer:
    declared_event_count: int
    declared_credit_amount: Decimal
    declared_debit_amount: Decimal
    declared_net_amount: Decimal


@dataclass(frozen=True, slots=True)
class ParsedBatch:
    header: Header
    events: tuple[Event, ...]
    trailer: Trailer
    computed_event_count: int
    computed_credit_amount: Decimal
    computed_debit_amount: Decimal
    computed_net_amount: Decimal


@dataclass(frozen=True, slots=True)
class SanitizedRecord:
    batch_id: str
    source_file: str
    source_record_number: int
    end_to_end_id: str
    transaction_id: str
    payer_document_token: str
    payer_document_masked: str
    payee_document_token: str
    payee_document_masked: str
    event_timestamp: str
    amount_brl: Decimal
    direction: str
    status: str
    return_code: str
    description: str
