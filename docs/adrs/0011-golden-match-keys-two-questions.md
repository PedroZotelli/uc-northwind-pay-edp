# ADR 0011 — Golden-match keys; two questions never netted

- Status: Accepted (Structure). Binding after lakehouse Consensus.
- Date: 2026-08-26
- Pass: 2 Structure
- Decider: Helena Dias (owner). Unsigned until `docs/consensus-lakehouse.md`.

## Context

ADR 0006 parked record and aggregate keys for golden-match (row
7). The referee module already lives at
`validation/golden-match/golden_match.py`. The week attaches
modern observations; it does not rewrite the module to invent
slack.

Every comparison asks **two separate questions**
(`plans/modern.md`):

1. **Legacy parity** — did modern reach the same observable
   outcome as legacy?
2. **Business correctness** — did modern satisfy the approved
   contract and independently reviewed expectation?

A source defect can make those answers differ. They are never
netted into one score. Golden-match is **not** the Dark Factory.

Paid grain (OntoLayer): `batch_id` + `currency` on
`reporting.card_settlement_reconciliation`. Contract
reconciliation grain is the same. Record replay identity is
`batch_id` + `source_record_number`.

## Decision

Type 01 golden-match keys tonight:

| Kind | Keys | Attaches |
|---|---|---|
| **Aggregate / paid** | `batch_id` + `currency` | Gold vs contract reconciliation vs legacy paid observation |
| **Record** | `batch_id` + `source_record_number` | Landing / Bronze rows vs contract sanitized expectations |

The two questions stay separate. Classification is exactly one
of: `CONFIRMED_SOURCE_DEFECT`, `CONFIRMED_LEGACY_DEFECT`,
`MODERN_DEFECT`, `APPROVED_BEHAVIOR_CHANGE`,
`CONTRACT_AMBIGUITY`, `UNRESOLVED`. No unexplained financial
difference. Tolerances remain zero.

`df-source-001` / trailer **173.44** vs rows **173.45** is a
source lie: keep the declaration, refuse, zero Parquet, zero
Gold. That is `CONFIRMED_SOURCE_DEFECT` when modern matches the
contract terminal — not a license to rewrite 173.44, and not
proof of a Dark Factory.

Happy path `valid-minimal`: net **173.45**, two records,
MATCHED, `amount_delta` **0.00**. Both questions may be yes.

## What this is not

A rewrite of `golden_match.py`, a Dark Factory detector, a
tolerance band, or a netted “close enough” score. Record keys
beyond the contract replay identity are not invented here.

## Consequences

- Seam 2 last leg is golden-match attached to **contract** and to
  **legacy observation**, using these keys.
- Unresolved difference blocks Gold from being served (Day 4).
- Constructor does not change the referee to go green.

## Evidence

- `docs/adrs/0006-later-nights-parked.md` — row 7, Day 3
- `plans/modern.md` — two questions; six codes; Milestone 3;
  golden-match is not the Dark Factory
- `validation/golden-match/golden_match.py` — referee already on
  the tree
- `contracts/types/01-card-settlement/reconciliation.yaml` —
  grain `batch_id`+`currency`; replay
  `batch_id`+`source_record_number`
- OntoLayer / `ontology/scripts/ask.py` — paid grain
  `batch_id`+`currency`; staging is not paid
- `docs/adrs/0005-source-lie-kept-zero-parquet.md` — keep 173.44
