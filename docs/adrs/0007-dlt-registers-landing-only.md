# ADR 0007 — dlt registers landing only

- Status: Accepted (Structure). Binding after lakehouse Consensus.
- Date: 2026-08-26
- Pass: 2 Structure
- Decider: Helena Dias (owner). Unsigned until `docs/consensus-lakehouse.md`.

## Context

ADR 0006 parked the exact dlt loading or registration role (row 3)
for Day 3. Ingest → landing is already signed. Constructor consumes
**published** `modern/landing/` Parquet and must not re-parse raw
(`docs/seams.md` seam 2).

Second Brain pack 01 / the 2026-06-09 sync sketch a second reader
then Parquet then Bronze / Silver / Gold. That sketch is **mail**.
It does not name dlt. `plans/modern.md` Milestone 2 does: load or
register Parquet through one approved dlt boundary. The writer
already owns the Parquet bytes (ADR 0001, ADR 0002).

## Decision

**dlt registers landing only.**

It consumes immutable sanitized Parquet (and its readiness
manifest) already published under `modern/landing/`. It does
**not** read SFTP `raw/incoming`. It does **not** re-parse Type 01
bytes. It does **not** own money, privacy, or grammar. Those stay
with the five-file package (ADR 0002–0004).

One role. It does not duplicate the writer. Landing stays
immutable after publication. A refused or source-lie batch that
emits **zero** Parquet (ADR 0005) gives dlt nothing to register
for that batch. dlt must not invent Gold, a net, or a token.

## What this is not

A dlt pipeline design, a choice of loader vs attach API, a
re-parse of `.dat` inside the lakehouse, or a second privacy
boundary. Dagster is not this decision (ADR 0006 row 8).

## Consequences

- Seam 2 first leg is **register landing**, not parse.
- dbt reads registered landing (or the lakehouse tables that
  follow). It does not call the Type 01 parser.
- Evidence for a refused lie does not invent a dlt load artifact.

## Evidence

- `docs/adrs/0006-later-nights-parked.md` — row 3, Day 3
- `docs/seams.md` — seam 2 consumes landing; does not re-parse raw
- `plans/modern.md` — “dlt registers landing; does not re-parse”;
  “does not own money, privacy, or grammar”; Milestone 2
- Second Brain pack 01 / `spec/estate/meetings/2026-06-09-file-decomposition.md`
  — second reader of the same raw bytes; **abstain on the word dlt**
- `docs/tech-spec-type-01-card-settlement.md` W-2 — stack was not
  an Intent decision; this ADR is Structure after ingest Consensus
