"""Typed Type 05 domain records with exact Decimal money."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Assessment:
    """One fee assessment, still carrying the restricted tax identifier."""

    physical_record_number: int
    assessment_id: str
    batch_id: str
    merchant_id: str
    merchant_tax_id: str
    fee_code: str
    description: str
    gross_amount: Decimal
    rate_percent: Decimal
    assessed_fee: Decimal
    calculated_fee: Decimal
    assessment_date: date


@dataclass(frozen=True, slots=True)
class ParsedBatch:
    batch_id: str
    rows: tuple[Assessment, ...]
    computed_row_count: int
    computed_gross_amount: Decimal
    computed_assessed_fee: Decimal
    computed_calculated_fee: Decimal


@dataclass(frozen=True, slots=True)
class SanitizedRecord:
    """One privacy-safe row, shaped exactly like the sanitized CSV contract."""

    batch_id: str
    source_file: str
    source_record_number: int
    assessment_id: str
    merchant_id: str
    merchant_tax_id_masked: str
    fee_code: str
    description: str
    gross_amount_brl: Decimal
    rate_percent: Decimal
    assessed_fee_brl: Decimal
    calculated_fee_brl: Decimal
    assessment_date: str
    rounding_mode: str
