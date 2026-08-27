"""Type 01 landing records — Decimal money, privacy-safe fields only."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

from parser import MONEY_QUANTUM, SanitizedDetail

SAO_PAULO = ZoneInfo("America/Sao_Paulo")
TOKEN_PREFIX = "tok_"
CPF_MASK_PREFIX = "*******"


@dataclass(frozen=True)
class LandingRow:
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

    def as_mapping(self) -> dict[str, object]:
        return {
            "batch_id": self.batch_id,
            "source_file": self.source_file,
            "source_record_number": self.source_record_number,
            "transaction_id": self.transaction_id,
            "merchant_id": self.merchant_id,
            "card_token": self.card_token,
            "card_last4": self.card_last4,
            "cpf_masked": self.cpf_masked,
            "transaction_ts": self.transaction_ts,
            "amount_brl": self.amount_brl.quantize(MONEY_QUANTUM),
            "movement_code": self.movement_code,
            "authorization_code": self.authorization_code,
            "nsu": self.nsu,
            "terminal_id": self.terminal_id,
        }


def compose_transaction_ts(transaction_date: str, transaction_time: str) -> str:
    stamp = datetime(
        int(transaction_date[0:4]),
        int(transaction_date[4:6]),
        int(transaction_date[6:8]),
        int(transaction_time[0:2]),
        int(transaction_time[2:4]),
        int(transaction_time[4:6]),
        tzinfo=SAO_PAULO,
    )
    return stamp.isoformat()


def landing_row_from_detail(detail: SanitizedDetail, source_file: str) -> LandingRow:
    return LandingRow(
        batch_id=detail.batch_id,
        source_file=source_file,
        source_record_number=detail.source_record_number,
        transaction_id=detail.transaction_id,
        merchant_id=detail.merchant_id,
        card_token=detail.card_token,
        card_last4=detail.card_last4,
        cpf_masked=detail.cpf_masked,
        transaction_ts=compose_transaction_ts(
            detail.transaction_date, detail.transaction_time
        ),
        amount_brl=detail.amount_brl.quantize(MONEY_QUANTUM),
        movement_code=detail.movement_code,
        authorization_code=detail.authorization_code,
        nsu=detail.nsu,
        terminal_id=detail.terminal_id,
    )
