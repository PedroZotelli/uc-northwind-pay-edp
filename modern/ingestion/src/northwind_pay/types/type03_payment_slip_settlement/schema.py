"""Type 03 validation, tokenization, masking, and independent batch controls."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from ...common.privacy import (
    assert_no_restricted_values,
    mask_document,
    tokenize_with_prefix,
)
from .model import ParsedBatch, SanitizedRecord

SOURCE_CONTROL_LOT_COUNT_MISMATCH = "SOURCE_CONTROL_LOT_COUNT_MISMATCH"
SOURCE_CONTROL_PHYSICAL_COUNT_MISMATCH = "SOURCE_CONTROL_PHYSICAL_COUNT_MISMATCH"
SOURCE_CONTROL_LOGICAL_COUNT_MISMATCH = "SOURCE_CONTROL_LOGICAL_COUNT_MISMATCH"
SOURCE_CONTROL_FACE_MISMATCH = "SOURCE_CONTROL_FACE_MISMATCH"
SOURCE_CONTROL_DISCOUNT_MISMATCH = "SOURCE_CONTROL_DISCOUNT_MISMATCH"
SOURCE_CONTROL_FEE_MISMATCH = "SOURCE_CONTROL_FEE_MISMATCH"
SOURCE_CONTROL_NET_MISMATCH = "SOURCE_CONTROL_NET_MISMATCH"


class SchemaError(ValueError):
    """The parsed batch cannot become a valid sanitized publication."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True, slots=True)
class BatchControls:
    declared_lot_count: int
    computed_lot_count: int
    declared_physical_record_count: int
    computed_physical_record_count: int
    declared_logical_count: int
    computed_logical_count: int
    declared_face_amount: Decimal
    computed_face_amount: Decimal
    declared_discount_amount: Decimal
    computed_discount_amount: Decimal
    declared_fee_amount: Decimal
    computed_fee_amount: Decimal
    declared_net_amount: Decimal
    computed_net_amount: Decimal
    computed_orphan_segment_count: int

    def as_evidence(self) -> dict[str, object]:
        return {
            "computed_discount_amount": f"{self.computed_discount_amount:.2f}",
            "computed_face_amount": f"{self.computed_face_amount:.2f}",
            "computed_fee_amount": f"{self.computed_fee_amount:.2f}",
            "computed_logical_count": self.computed_logical_count,
            "computed_lot_count": self.computed_lot_count,
            "computed_net_amount": f"{self.computed_net_amount:.2f}",
            "computed_orphan_segment_count": self.computed_orphan_segment_count,
            "computed_physical_record_count": self.computed_physical_record_count,
            "declared_discount_amount": f"{self.declared_discount_amount:.2f}",
            "declared_face_amount": f"{self.declared_face_amount:.2f}",
            "declared_fee_amount": f"{self.declared_fee_amount:.2f}",
            "declared_logical_count": self.declared_logical_count,
            "declared_lot_count": self.declared_lot_count,
            "declared_net_amount": f"{self.declared_net_amount:.2f}",
            "declared_physical_record_count": self.declared_physical_record_count,
        }


@dataclass(frozen=True, slots=True)
class SanitizedBatch:
    batch_id: str
    source_file: str
    records: tuple[SanitizedRecord, ...]
    controls: BatchControls


def controls_of(parsed: ParsedBatch) -> BatchControls:
    return BatchControls(
        declared_lot_count=parsed.trailer.declared_lot_count,
        computed_lot_count=parsed.computed_lot_count,
        declared_physical_record_count=parsed.trailer.declared_physical_record_count,
        computed_physical_record_count=parsed.computed_physical_record_count,
        declared_logical_count=parsed.trailer.declared_logical_count,
        computed_logical_count=parsed.computed_logical_count,
        declared_face_amount=parsed.declared_face_amount,
        computed_face_amount=parsed.computed_face_amount,
        declared_discount_amount=parsed.declared_discount_amount,
        computed_discount_amount=parsed.computed_discount_amount,
        declared_fee_amount=parsed.declared_fee_amount,
        computed_fee_amount=parsed.computed_fee_amount,
        declared_net_amount=parsed.trailer.declared_net_amount,
        computed_net_amount=parsed.computed_net_amount,
        computed_orphan_segment_count=parsed.computed_orphan_segment_count,
    )


def sanitize(parsed: ParsedBatch, *, source_filename: str) -> SanitizedBatch:
    """Validate controls, tokenize and mask, and scan the complete candidate."""

    controls = controls_of(parsed)
    for declared, computed, code in (
        (
            controls.declared_lot_count,
            controls.computed_lot_count,
            SOURCE_CONTROL_LOT_COUNT_MISMATCH,
        ),
        (
            controls.declared_physical_record_count,
            controls.computed_physical_record_count,
            SOURCE_CONTROL_PHYSICAL_COUNT_MISMATCH,
        ),
        (
            controls.declared_logical_count,
            controls.computed_logical_count,
            SOURCE_CONTROL_LOGICAL_COUNT_MISMATCH,
        ),
        (
            controls.declared_face_amount,
            controls.computed_face_amount,
            SOURCE_CONTROL_FACE_MISMATCH,
        ),
        (
            controls.declared_discount_amount,
            controls.computed_discount_amount,
            SOURCE_CONTROL_DISCOUNT_MISMATCH,
        ),
        (
            controls.declared_fee_amount,
            controls.computed_fee_amount,
            SOURCE_CONTROL_FEE_MISMATCH,
        ),
        (
            controls.declared_net_amount,
            controls.computed_net_amount,
            SOURCE_CONTROL_NET_MISMATCH,
        ),
    ):
        if declared != computed:
            raise SchemaError(code, "a declared source control is wrong")

    records = tuple(
        SanitizedRecord(
            batch_id=parsed.batch_id,
            source_file=source_filename,
            source_record_number_a=row.record_number_a,
            source_record_number_b=row.record_number_b,
            lot_number=row.lot_number,
            sequence=row.sequence,
            settlement_id=row.settlement_id,
            payment_reference_token=tokenize_with_prefix(
                row.payment_reference,
                prefix="payref",
                key_variable="NWP_PAYMENT_REFERENCE_KEY",
            ),
            payment_reference_last4=row.payment_reference[-4:],
            beneficiary_token=tokenize_with_prefix(
                row.beneficiary_name,
                prefix="party",
                key_variable="NWP_PARTY_TOKEN_KEY",
            ),
            beneficiary_tax_id_type="CPF" if row.tax_id_type == "1" else "CNPJ",
            beneficiary_tax_id_masked=mask_document(row.beneficiary_tax_id),
            bank_account_token=tokenize_with_prefix(
                (
                    f"{row.bank_code}:{row.branch_number}:"
                    f"{row.account_number}:{row.account_check_digit}"
                ),
                prefix="acct",
                key_variable="NWP_ACCOUNT_TOKEN_KEY",
            ),
            bank_account_last4=row.account_number[-4:],
            due_date=row.due_date.isoformat(),
            payment_date=row.payment_date.isoformat(),
            face_amount_brl=row.face_amount,
            discount_brl=row.discount,
            fee_brl=row.fee,
            net_amount_brl=row.net_amount,
            status=row.status_code,
            bank_reference=row.bank_reference,
            client_reference=row.client_reference,
        )
        for row in parsed.rows
    )

    restricted = tuple(
        value
        for row in parsed.rows
        for value in (
            row.payment_reference,
            row.beneficiary_tax_id,
            row.beneficiary_name,
            row.account_number,
        )
    )
    candidate = "\n".join(
        ",".join(
            (
                record.settlement_id,
                record.payment_reference_token,
                record.beneficiary_token,
                record.beneficiary_tax_id_masked,
                record.bank_account_token,
                record.bank_reference,
                record.client_reference,
                f"{record.net_amount_brl:.2f}",
            )
        )
        for record in records
    )
    assert_no_restricted_values(candidate, restricted)

    return SanitizedBatch(
        batch_id=parsed.batch_id,
        source_file=source_filename,
        records=records,
        controls=controls,
    )
