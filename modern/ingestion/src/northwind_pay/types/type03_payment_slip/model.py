"""Typed Type 03 domain records with exact Decimal money."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class LogicalRow:
    """One settlement, assembled from an adjacent A and B segment pair."""

    record_number_a: int
    record_number_b: int
    lot_number: str
    sequence: str
    settlement_id: str
    payment_reference: str
    face_amount: Decimal
    due_date: date
    payment_date: date
    discount: Decimal
    fee: Decimal
    status_code: str
    bank_reference: str
    tax_id_type: str
    beneficiary_tax_id: str
    beneficiary_name: str
    bank_code: str
    branch_number: str
    account_number: str
    account_check_digit: str
    client_reference: str

    @property
    def net_amount(self) -> Decimal:
        """Face minus discount plus fee, in exact decimal arithmetic."""

        return self.face_amount - self.discount + self.fee


@dataclass(frozen=True, slots=True)
class Trailer:
    declared_lot_count: int
    declared_physical_record_count: int
    declared_logical_count: int
    declared_net_amount: Decimal


@dataclass(frozen=True, slots=True)
class ParsedBatch:
    batch_id: str
    rows: tuple[LogicalRow, ...]
    trailer: Trailer
    declared_face_amount: Decimal
    declared_discount_amount: Decimal
    declared_fee_amount: Decimal
    computed_lot_count: int
    computed_physical_record_count: int
    computed_logical_count: int
    computed_face_amount: Decimal
    computed_discount_amount: Decimal
    computed_fee_amount: Decimal
    computed_net_amount: Decimal
    computed_orphan_segment_count: int


@dataclass(frozen=True, slots=True)
class SanitizedRecord:
    batch_id: str
    source_file: str
    source_record_number_a: int
    source_record_number_b: int
    lot_number: str
    sequence: str
    settlement_id: str
    payment_reference_token: str
    payment_reference_last4: str
    beneficiary_token: str
    beneficiary_tax_id_type: str
    beneficiary_tax_id_masked: str
    bank_account_token: str
    bank_account_last4: str
    due_date: str
    payment_date: str
    face_amount_brl: Decimal
    discount_brl: Decimal
    fee_brl: Decimal
    net_amount_brl: Decimal
    status: str
    bank_reference: str
    client_reference: str
