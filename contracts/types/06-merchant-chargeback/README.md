# 06 - Merchant Chargeback Adjustment

Status: approved for Type 06 factory kit

Synthetic chargeback adjustments. Independent calculation is
`original × rate ÷ 100` rounded **HALF_UP** to scale 2.

`valid-minimal` row `67,00` at `1,500` percent is exactly `1.005` before
scale-2 rounding: contract **1.01**. The live Java plant may MATCHED a
different cent. That disagreement is a **legacy-plant** defect, not a
source lie. Do not patch Java.

## Detection

- Filename: `^NW_MERCHANT_CHARGEBACK_[0-9]{8}_B[0-9]{15}\.csv$`
- Header type code: `MER_CHGBK06`
- Encoding: UTF-8 NFC, semicolon, quoted description

## Canonical outcomes

| Scenario | Batch | Expected (contract) |
|---|---|---|
| `valid-minimal` | `B202607230000501` | MATCHED chargeback **1.01** |
| `valid-boundary` | `B200002290000502` | accepted |
| `malformed` | `B202607230000503` | `INVALID_CSV_QUOTING` |
| `legacy-miss` | `B202607230000504` | contract MATCHED **1.01** (same HALF_UP steel thread) |
