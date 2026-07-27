"""Type 01 validation, privacy transformation, and independent batch controls.

This is the boundary where restricted values stop. It converts parsed details
into sanitized records, verifies the source-declared controls against the
independently computed ones, and scans the complete candidate output before
anything can be published.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from ...common.money import render
from ...common.privacy import assert_no_restricted_values, mask_cpf, pan_last4, tokenize_pan
from .model import ParsedBatch, SanitizedRecord

# The CSV contract fixes the display timezone for Type 01 at America/Sao_Paulo.
# It has had no DST transition since 2019 and the contract's approved examples
# are all -03:00, so the offset is applied as a fixed contract constant rather
# than through a platform timezone database whose contents can change.
SAO_PAULO = timezone(timedelta(hours=-3))

SOURCE_CONTROL_TOTAL_MISMATCH = "SOURCE_CONTROL_TOTAL_MISMATCH"


class SchemaError(ValueError):
    """The parsed batch cannot become a valid sanitized publication."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True, slots=True)
class BatchControls:
    """Declared and independently computed controls, kept side by side."""

    declared_detail_count: int
    computed_detail_count: int
    declared_net_amount: Decimal
    computed_net_amount: Decimal

    @property
    def matched(self) -> bool:
        return (
            self.declared_detail_count == self.computed_detail_count
            and self.declared_net_amount == self.computed_net_amount
        )

    def as_evidence(self) -> dict[str, object]:
        return {
            "computed_detail_count": self.computed_detail_count,
            "computed_net_amount": render(self.computed_net_amount),
            "declared_detail_count": self.declared_detail_count,
            "declared_net_amount": render(self.declared_net_amount),
        }


@dataclass(frozen=True, slots=True)
class SanitizedBatch:
    """A complete, privacy-safe batch ready for deterministic publication."""

    batch_id: str
    source_file: str
    records: tuple[SanitizedRecord, ...]
    controls: BatchControls


def controls_of(parsed: ParsedBatch) -> BatchControls:
    return BatchControls(
        declared_detail_count=parsed.trailer.declared_detail_count,
        computed_detail_count=parsed.computed_detail_count,
        declared_net_amount=parsed.trailer.declared_net_amount,
        computed_net_amount=parsed.computed_net_amount,
    )


def sanitize(parsed: ParsedBatch, *, source_filename: str) -> SanitizedBatch:
    """Validate controls, transform privacy fields, and scan the candidate.

    The source-declared control is never corrected to match the computed one.
    A disagreement is a terminal source defect and the batch produces no
    sanitized output at all.
    """

    controls = controls_of(parsed)
    if not controls.matched:
        raise SchemaError(
            SOURCE_CONTROL_TOTAL_MISMATCH,
            "declared source controls do not match independently parsed details",
        )

    records: list[SanitizedRecord] = []
    for detail in parsed.details:
        moment = datetime.combine(
            detail.transaction_date, detail.transaction_time, tzinfo=SAO_PAULO
        )
        records.append(
            SanitizedRecord(
                batch_id=parsed.header.batch_id,
                source_file=source_filename,
                source_record_number=detail.physical_record_number,
                transaction_id=detail.transaction_id,
                merchant_id=detail.merchant_id,
                card_token=tokenize_pan(detail.pan),
                card_last4=pan_last4(detail.pan),
                cpf_masked=mask_cpf(detail.cpf),
                transaction_ts=moment.isoformat(),
                amount_brl=detail.amount_brl,
                movement_code=detail.movement_code,
                authorization_code=detail.authorization_code,
                nsu=detail.nsu,
                terminal_id=detail.terminal_id,
            )
        )

    # Scan the complete candidate output, not each field in isolation, so a
    # restricted value cannot survive by arriving through an unexpected column.
    restricted = tuple(
        value for detail in parsed.details for value in (detail.pan, detail.cpf)
    )
    candidate = "\n".join(
        ",".join(
            (
                record.batch_id,
                record.source_file,
                str(record.source_record_number),
                record.transaction_id,
                record.merchant_id,
                record.card_token,
                record.card_last4,
                record.cpf_masked,
                record.transaction_ts,
                render(record.amount_brl),
                record.movement_code,
                record.authorization_code,
                record.nsu,
                record.terminal_id,
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
