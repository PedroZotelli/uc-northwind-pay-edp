# ADR 0010 — Parser owns privacy and Decimal; dbt does not retokenize

- Status: Accepted (Structure). Binding after lakehouse Consensus.
- Date: 2026-08-26
- Pass: 2 Structure
- Decider: Helena Dias (owner). Unsigned until `docs/consensus-lakehouse.md`.
- Privacy: Priya Shah — privacy finished before any landing row.

## Context

ADR 0006 parked rule allocation between ingestion and dbt (row 6).
Privacy already dies at the parser (ADR 0004). Money is Decimal
(ADR 0003). The five-file package owns Type 01 grammar, privacy,
money, and terminal outcome (ADR 0002).

Second Brain Type 01 inbound / privacy policy: tokenize PAN, keep
last4, mask CPF. The judge is `privacy.yaml`, not a dbt model.
Java is the live-line boundary. The second plant does not import
it. dlt does not own those rules (ADR 0007).

## Decision

**Ingestion (Type 01 parser / five-file package) already did
privacy and Decimal.** Those facts are true of landing before dlt
registers anything.

**dbt does not retokenize.** It does not unmask. It does not
re-decode overpunch. It does not re-parse raw. It does not write
173.45 into a trailer or control to “fix” 173.44 (ADR 0005).

dbt may conform grain, signs, dates, and controls on
already-safe Decimal columns, and it may test Bronze → Silver →
Gold. It may block Gold when privacy-safe contracts fail. It
must not become a second parser or a second privacy boundary.

Clear PAN or CPF in any lakehouse zone is a failed batch, not a
transform to apply later.

## What this is not

A dbt project layout, a list of tests, HMAC key storage, or a
port of Java tokenization into SQL.

## Consequences

- Rule split is altitude, not a stack preference: parser owns
  Type 01 grammar / privacy / money; dlt registers; dbt conforms
  and tests Gold.
- A dbt model that emits `tok_` from a PAN is a failed ADR, not
  an implementation detail.
- Golden-match compares privacy-safe observations. It does not
  ask dbt to repair the source.

## Evidence

- `docs/adrs/0003-decimal-never-float.md`, `0004-privacy-dies-at-the-parser.md`
- `docs/adrs/0006-later-nights-parked.md` — row 6, Day 3
- `contracts/types/01-card-settlement/privacy.yaml` — the judge
- `plans/modern.md` — transform prohibited values **before**
  Parquet; “Give dlt one explicit role”
- Second Brain packs 01 and 03 — privacy at parse; **do not
  invent a dbt model that tokenizes**
- `docs/seams.md` — Constructor must not write the Type 01 parser
