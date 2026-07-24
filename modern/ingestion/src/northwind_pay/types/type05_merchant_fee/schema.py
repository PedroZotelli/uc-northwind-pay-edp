"""Type 05 validation, masking, and independent batch controls."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Mapping

from ...common.documents import mask_cnpj
from ...common.privacy import assert_no_restricted_values
from .model import ParsedBatch, SanitizedRecord

SOURCE_CONTROL_ASSESSED_FEE_MISMATCH = "SOURCE_CONTROL_ASSESSED_FEE_MISMATCH"
SOURCE_CONTROL_ROW_COUNT_MISMATCH = "SOURCE_CONTROL_ROW_COUNT_MISMATCH"
SOURCE_CONTROL_GROSS_MISMATCH = "SOURCE_CONTROL_GROSS_MISMATCH"


class SchemaError(ValueError):
    """The parsed batch cannot become a valid sanitized publication."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True, slots=True)
class BatchControls:
    declared_row_count: int
    computed_row_count: int
    declared_gross_amount: Decimal
    computed_gross_amount: Decimal
    declared_assessed_fee: Decimal
    computed_assessed_fee: Decimal
    declared_calculated_fee: Decimal
    computed_calculated_fee: Decimal

    def as_evidence(self) -> dict[str, object]:
        return {
            "computed_assessed_fee": f"{self.computed_assessed_fee:.2f}",
            "computed_calculated_fee": f"{self.computed_calculated_fee:.2f}",
            "computed_gross_amount": f"{self.computed_gross_amount:.2f}",
            "computed_row_count": self.computed_row_count,
            "declared_assessed_fee": f"{self.declared_assessed_fee:.2f}",
            "declared_calculated_fee": f"{self.declared_calculated_fee:.2f}",
            "declared_gross_amount": f"{self.declared_gross_amount:.2f}",
            "declared_row_count": self.declared_row_count,
        }


@dataclass(frozen=True, slots=True)
class SanitizedBatch:
    batch_id: str
    source_file: str
    records: tuple[SanitizedRecord, ...]
    controls: BatchControls


def controls_of(parsed: ParsedBatch, declared: Mapping[str, Any]) -> BatchControls:
    """Pair the source-owned declaration with independently computed totals."""

    return BatchControls(
        declared_row_count=int(str(declared["row_count"])),
        computed_row_count=parsed.computed_row_count,
        declared_gross_amount=Decimal(str(declared["gross_amount"])),
        computed_gross_amount=parsed.computed_gross_amount,
        declared_assessed_fee=Decimal(str(declared["assessed_fee"])),
        computed_assessed_fee=parsed.computed_assessed_fee,
        declared_calculated_fee=Decimal(str(declared["calculated_fee"])),
        computed_calculated_fee=parsed.computed_calculated_fee,
    )


def sanitize(
    parsed: ParsedBatch,
    *,
    source_filename: str,
    declared: Mapping[str, Any],
) -> SanitizedBatch:
    """Validate controls, mask, and scan the complete candidate output.

    The source-owned declaration is never corrected. A disagreement is a
    terminal source defect and the batch produces no sanitized output.
    """

    controls = controls_of(parsed, declared)
    if controls.declared_row_count != controls.computed_row_count:
        raise SchemaError(
            SOURCE_CONTROL_ROW_COUNT_MISMATCH, "declared row count is wrong"
        )
    if controls.declared_gross_amount != controls.computed_gross_amount:
        raise SchemaError(
            SOURCE_CONTROL_GROSS_MISMATCH, "declared gross amount is wrong"
        )
    if controls.declared_assessed_fee != controls.computed_assessed_fee:
        raise SchemaError(
            SOURCE_CONTROL_ASSESSED_FEE_MISMATCH,
            "declared assessed fee does not match the independently parsed rows",
        )

    records = tuple(
        SanitizedRecord(
            batch_id=row.batch_id,
            source_file=source_filename,
            source_record_number=row.physical_record_number,
            assessment_id=row.assessment_id,
            merchant_id=row.merchant_id,
            merchant_tax_id_masked=mask_cnpj(row.merchant_tax_id),
            fee_code=row.fee_code,
            description=row.description,
            gross_amount_brl=row.gross_amount,
            rate_percent=row.rate_percent,
            assessed_fee_brl=row.assessed_fee,
            calculated_fee_brl=row.calculated_fee,
            assessment_date=row.assessment_date.isoformat(),
            rounding_mode="HALF_UP",
        )
        for row in parsed.rows
    )

    # Scan every byte of the candidate output for every raw CNPJ, as the
    # privacy contract requires, before anything can be published.
    candidate = "\n".join(
        ";".join(
            (
                record.batch_id,
                record.source_file,
                str(record.source_record_number),
                record.assessment_id,
                record.merchant_id,
                record.merchant_tax_id_masked,
                record.fee_code,
                record.description,
                f"{record.gross_amount_brl:.2f}",
                f"{record.rate_percent:.3f}",
                f"{record.assessed_fee_brl:.2f}",
                f"{record.calculated_fee_brl:.2f}",
                record.assessment_date,
                record.rounding_mode,
            )
        )
        for record in records
    )
    assert_no_restricted_values(
        candidate, tuple(row.merchant_tax_id for row in parsed.rows)
    )

    return SanitizedBatch(
        batch_id=parsed.batch_id,
        source_file=source_filename,
        records=records,
        controls=controls,
    )
