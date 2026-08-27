# ADR 0009 — Bronze, Silver, and Gold grains (Type 01)

- Status: Accepted (Structure). Binding after lakehouse Consensus.
- Date: 2026-08-26
- Pass: 2 Structure
- Decider: Helena Dias (owner). Unsigned until `docs/consensus-lakehouse.md`.

## Context

ADR 0006 parked Bronze, Silver, and Gold grains and keys (row 5).
`plans/modern.md` names the zones and requires one documented
grain and owner each. The 2026-06-09 “Bronze / Silver / Gold”
line is mail — not a grain.

OntoLayer / `make ontology-ask` (catalog, not SQL against live
money): Type 01 **paid** is observed on
`reporting.card_settlement_reconciliation`. Grain: `batch_id` +
`currency` (one row per batch per currency). Writer:
`reporting.refresh_card_settlement_reconciliation`. Staging is
not paid.

The contract grain for Type 01 reconciliation is the same keys
(`contracts/types/01-card-settlement/reconciliation.yaml`). Record
replay identity is `batch_id` + `source_record_number`. Those are
not guessed joins.

## Decision

Type 01 medallion grains tonight:

| Zone | Meaning | Grain / keys |
|---|---|---|
| **Bronze** | Source-aligned records from immutable landing. Minimal reinterpretation. Already-Decimal, already privacy-safe columns as published. | One row per landing record. Keys: `batch_id` + `source_record_number`. |
| **Silver** | Conformed entities, signs, dates, and business grain. | Record identity remains `batch_id` + `source_record_number`. Batch-level business / paid grain is `batch_id` + `currency`. |
| **Gold** | Governed reports, controls, and reconciliations. **May later be served** (Day 4). Unresolved Gold is not servable. | One row per batch per currency: `batch_id` + `currency`. Same observation shape as paid: counts, nets, deltas, status. |

Constructor owns these grains. Translator does not rewrite them.
dlt does not invent them (ADR 0007).

Refused / source-lie batches (zero Parquet) produce **no** Bronze,
Silver, or Gold for that batch. Peers continue.

Do not treat `staging.card_settlement` as Gold or as paid. Do not
put Rafael’s unused dump columns into Gold because a meeting
asked; that question stays mail.

## What this is not

dbt model filenames, a star schema, a join graph onto Postgres,
or a FastAPI schema. Serving is parked. This ADR records **what
is true** of the grains, not how to code dbt.

## Consequences

- Seam 2 medallion leg is these three grains, in this order.
- Gold is the Type 01 product that golden-match attaches (ADR
  0011). Day 4 may serve only an **approved** Gold snapshot.
- Block Gold when upstream identity, schema, or quality fails.

## Evidence

- `docs/adrs/0006-later-nights-parked.md` — row 5, Day 3
- `plans/modern.md` — Modern data zones; “one documented grain
  and owner each”; Milestone 2
- `contracts/types/01-card-settlement/reconciliation.yaml` —
  `grain.keys: batch_id, currency`; replay
  `idempotent_by_batch_id_and_source_record_number`
- `contracts/types/01-card-settlement/csv.yaml` — `batch_id`,
  `source_record_number` on the sanitized row
- OntoLayer / `ontology/scripts/ask.py` — paid table, grain
  `batch_id`+`currency`, not staging
- Second Brain pack 01 — Bronze/Silver/Gold nouns in a meeting
  sketch; **not a grain**
