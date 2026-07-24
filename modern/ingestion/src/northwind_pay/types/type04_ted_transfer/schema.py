"""Type 04 validation, account privacy, and independent batch controls."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from ...common.privacy import (
    assert_no_restricted_values,
    mask_document,
    tokenize_account,
)
from .model import ParsedBatch, SanitizedRecord

SOURCE_CONTROL_TRANSFER_COUNT_MISMATCH = "SOURCE_CONTROL_TRANSFER_COUNT_MISMATCH"
SOURCE_CONTROL_RETURN_COUNT_MISMATCH = "SOURCE_CONTROL_RETURN_COUNT_MISMATCH"
SOURCE_CONTROL_GROSS_MISMATCH = "SOURCE_CONTROL_GROSS_MISMATCH"
SOURCE_CONTROL_RETURNED_MISMATCH = "SOURCE_CONTROL_RETURNED_MISMATCH"
SOURCE_CONTROL_NET_MISMATCH = "SOURCE_CONTROL_NET_MISMATCH"


class SchemaError(ValueError):
    """The parsed batch cannot become a valid sanitized publication."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True, slots=True)
class BatchControls:
    declared_transfer_count: int
    computed_transfer_count: int
    declared_return_count: int
    computed_return_count: int
    declared_gross_amount: Decimal
    computed_gross_amount: Decimal
    declared_return_amount: Decimal
    computed_return_amount: Decimal
    declared_net_amount: Decimal
    computed_net_amount: Decimal

    def as_evidence(self) -> dict[str, object]:
        return {
            "computed_gross_amount": f"{self.computed_gross_amount:.2f}",
            "computed_net_amount": f"{self.computed_net_amount:.2f}",
            "computed_return_amount": f"{self.computed_return_amount:.2f}",
            "computed_return_count": self.computed_return_count,
            "computed_transfer_count": self.computed_transfer_count,
            "declared_gross_amount": f"{self.declared_gross_amount:.2f}",
            "declared_net_amount": f"{self.declared_net_amount:.2f}",
            "declared_return_amount": f"{self.declared_return_amount:.2f}",
            "declared_return_count": self.declared_return_count,
            "declared_transfer_count": self.declared_transfer_count,
        }


@dataclass(frozen=True, slots=True)
class SanitizedBatch:
    batch_id: str
    source_file: str
    records: tuple[SanitizedRecord, ...]
    controls: BatchControls


def controls_of(parsed: ParsedBatch) -> BatchControls:
    return BatchControls(
        declared_transfer_count=parsed.trailer.declared_transfer_count,
        computed_transfer_count=parsed.computed_transfer_count,
        declared_return_count=parsed.trailer.declared_return_count,
        computed_return_count=parsed.computed_return_count,
        declared_gross_amount=parsed.trailer.declared_gross_amount,
        computed_gross_amount=parsed.computed_gross_amount,
        declared_return_amount=parsed.trailer.declared_return_amount,
        computed_return_amount=parsed.computed_return_amount,
        declared_net_amount=parsed.trailer.declared_net_amount,
        computed_net_amount=parsed.computed_net_amount,
    )


def sanitize(parsed: ParsedBatch, *, source_filename: str) -> SanitizedBatch:
    """Validate controls, tokenize accounts, and emit movements in source order.

    A return inherits its account, tax-mask, institution, purpose, and status
    context from the transfer it immediately follows, which is why the pairing
    is preserved through parsing rather than rebuilt by a join here.
    """

    controls = controls_of(parsed)
    for declared, computed, code in (
        (
            controls.declared_transfer_count,
            controls.computed_transfer_count,
            SOURCE_CONTROL_TRANSFER_COUNT_MISMATCH,
        ),
        (
            controls.declared_return_count,
            controls.computed_return_count,
            SOURCE_CONTROL_RETURN_COUNT_MISMATCH,
        ),
        (
            controls.declared_gross_amount,
            controls.computed_gross_amount,
            SOURCE_CONTROL_GROSS_MISMATCH,
        ),
        (
            controls.declared_return_amount,
            controls.computed_return_amount,
            SOURCE_CONTROL_RETURNED_MISMATCH,
        ),
        (
            controls.declared_net_amount,
            controls.computed_net_amount,
            SOURCE_CONTROL_NET_MISMATCH,
        ),
    ):
        if declared != computed:
            raise SchemaError(code, "a declared source control is wrong")

    returns_by_transfer = {
        transfer.transfer_id: entry for transfer, entry in parsed.returns
    }
    records: list[SanitizedRecord] = []
    for transfer in parsed.transfers:
        payer_token = tokenize_account(
            transfer.payer_ispb, transfer.payer_branch, transfer.payer_account
        )
        beneficiary_token = tokenize_account(
            transfer.beneficiary_ispb,
            transfer.beneficiary_branch,
            transfer.beneficiary_account,
        )
        payer_mask = mask_document(transfer.payer_tax_id)
        beneficiary_mask = mask_document(transfer.beneficiary_tax_id)
        records.append(
            SanitizedRecord(
                batch_id=parsed.header.batch_id,
                source_file=source_filename,
                source_record_number=transfer.physical_record_number,
                movement_id=transfer.transfer_id,
                original_transfer_id="",
                movement_kind="TRANSFER",
                movement_ts=transfer.moment.isoformat(),
                amount_brl=transfer.amount,
                payer_account_token=payer_token,
                payer_tax_id_masked=payer_mask,
                beneficiary_account_token=beneficiary_token,
                beneficiary_tax_id_masked=beneficiary_mask,
                beneficiary_ispb=transfer.beneficiary_ispb,
                purpose_code=transfer.purpose_code,
                status_code=transfer.status_code,
                return_reason_code="",
            )
        )
        entry = returns_by_transfer.get(transfer.transfer_id)
        if entry is None:
            continue
        records.append(
            SanitizedRecord(
                batch_id=parsed.header.batch_id,
                source_file=source_filename,
                source_record_number=entry.physical_record_number,
                movement_id=entry.return_id,
                original_transfer_id=entry.original_transfer_id,
                movement_kind="RETURN",
                movement_ts=entry.moment.isoformat(),
                amount_brl=entry.amount,
                payer_account_token=payer_token,
                payer_tax_id_masked=payer_mask,
                beneficiary_account_token=beneficiary_token,
                beneficiary_tax_id_masked=beneficiary_mask,
                beneficiary_ispb=transfer.beneficiary_ispb,
                purpose_code=transfer.purpose_code,
                status_code=transfer.status_code,
                return_reason_code=entry.reason_code,
            )
        )

    restricted = tuple(
        value
        for transfer in parsed.transfers
        for value in (
            transfer.payer_account,
            transfer.beneficiary_account,
            transfer.payer_tax_id,
            transfer.beneficiary_tax_id,
        )
    )
    candidate = "\n".join(
        ",".join(
            (
                record.movement_id,
                record.original_transfer_id,
                record.movement_kind,
                record.movement_ts,
                f"{record.amount_brl:.2f}",
                record.payer_account_token,
                record.payer_tax_id_masked,
                record.beneficiary_account_token,
                record.beneficiary_tax_id_masked,
                record.beneficiary_ispb,
                record.purpose_code,
                record.status_code,
                record.return_reason_code,
            )
        )
        for record in records
    )
    assert_no_restricted_values(candidate, restricted)

    return SanitizedBatch(
        batch_id=parsed.header.batch_id,
        source_file=source_filename,
        records=tuple(records),
        controls=controls,
    )
