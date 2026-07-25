"""Type 02 validation, document privacy, and independent batch controls."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from ...common.privacy import (
    assert_no_restricted_values,
    mask_document,
    tokenize_document,
)
from .model import ParsedBatch, SanitizedRecord

SOURCE_CONTROL_COUNT_MISMATCH = "SOURCE_CONTROL_COUNT_MISMATCH"
SOURCE_CONTROL_CREDIT_MISMATCH = "SOURCE_CONTROL_CREDIT_MISMATCH"
SOURCE_CONTROL_DEBIT_MISMATCH = "SOURCE_CONTROL_DEBIT_MISMATCH"
SOURCE_CONTROL_NET_MISMATCH = "SOURCE_CONTROL_NET_MISMATCH"


class SchemaError(ValueError):
    """The parsed batch cannot become a valid sanitized publication."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True, slots=True)
class BatchControls:
    declared_event_count: int
    computed_event_count: int
    declared_credit_amount: Decimal
    computed_credit_amount: Decimal
    declared_debit_amount: Decimal
    computed_debit_amount: Decimal
    declared_net_amount: Decimal
    computed_net_amount: Decimal

    def as_evidence(self) -> dict[str, object]:
        return {
            "computed_credit_amount": f"{self.computed_credit_amount:.2f}",
            "computed_debit_amount": f"{self.computed_debit_amount:.2f}",
            "computed_event_count": self.computed_event_count,
            "computed_net_amount": f"{self.computed_net_amount:.2f}",
            "declared_credit_amount": f"{self.declared_credit_amount:.2f}",
            "declared_debit_amount": f"{self.declared_debit_amount:.2f}",
            "declared_event_count": self.declared_event_count,
            "declared_net_amount": f"{self.declared_net_amount:.2f}",
        }


@dataclass(frozen=True, slots=True)
class SanitizedBatch:
    batch_id: str
    source_file: str
    records: tuple[SanitizedRecord, ...]
    controls: BatchControls


def controls_of(parsed: ParsedBatch) -> BatchControls:
    return BatchControls(
        declared_event_count=parsed.trailer.declared_event_count,
        computed_event_count=parsed.computed_event_count,
        declared_credit_amount=parsed.trailer.declared_credit_amount,
        computed_credit_amount=parsed.computed_credit_amount,
        declared_debit_amount=parsed.trailer.declared_debit_amount,
        computed_debit_amount=parsed.computed_debit_amount,
        declared_net_amount=parsed.trailer.declared_net_amount,
        computed_net_amount=parsed.computed_net_amount,
    )


def sanitize(parsed: ParsedBatch, *, source_filename: str) -> SanitizedBatch:
    """Validate controls, tokenize and mask documents, and scan the candidate.

    Each control has its own stable code, so a rejection says which control
    disagreed rather than only that something did. The source-owned declaration
    is never corrected.
    """

    controls = controls_of(parsed)
    if controls.declared_event_count != controls.computed_event_count:
        raise SchemaError(SOURCE_CONTROL_COUNT_MISMATCH, "declared event count is wrong")
    if controls.declared_credit_amount != controls.computed_credit_amount:
        raise SchemaError(SOURCE_CONTROL_CREDIT_MISMATCH, "declared credit is wrong")
    if controls.declared_debit_amount != controls.computed_debit_amount:
        raise SchemaError(SOURCE_CONTROL_DEBIT_MISMATCH, "declared debit is wrong")
    if controls.declared_net_amount != controls.computed_net_amount:
        raise SchemaError(SOURCE_CONTROL_NET_MISMATCH, "declared net is wrong")

    records = tuple(
        SanitizedRecord(
            batch_id=parsed.header.batch_id,
            source_file=source_filename,
            source_record_number=event.physical_record_number,
            end_to_end_id=event.end_to_end_id,
            transaction_id=event.transaction_id,
            payer_document_token=tokenize_document(event.payer_document),
            payer_document_masked=mask_document(event.payer_document),
            payee_document_token=tokenize_document(event.payee_document),
            payee_document_masked=mask_document(event.payee_document),
            event_timestamp=event.event_timestamp,
            amount_brl=event.signed_amount,
            direction=event.direction,
            status=event.status,
            return_code=event.return_code,
            description=event.description,
        )
        for event in parsed.events
    )

    restricted = tuple(
        value
        for event in parsed.events
        for value in (event.payer_document, event.payee_document)
    )
    candidate = "\n".join(
        "|".join(
            (
                record.batch_id,
                record.source_file,
                str(record.source_record_number),
                record.end_to_end_id,
                record.transaction_id,
                record.payer_document_token,
                record.payer_document_masked,
                record.payee_document_token,
                record.payee_document_masked,
                record.event_timestamp,
                f"{record.amount_brl:.2f}",
                record.direction,
                record.status,
                record.return_code,
                record.description,
            )
        )
        for record in records
    )
    assert_no_restricted_values(candidate, restricted)

    return SanitizedBatch(
        batch_id=parsed.header.batch_id,
        source_file=source_filename,
        records=records,
        controls=controls,
    )
