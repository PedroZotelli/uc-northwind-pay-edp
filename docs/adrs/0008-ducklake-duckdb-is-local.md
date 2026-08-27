# ADR 0008 — DuckLake and DuckDB are local

- Status: Accepted (Structure). Binding after lakehouse Consensus.
- Date: 2026-08-26
- Pass: 2 Structure
- Decider: Helena Dias (owner). Unsigned until `docs/consensus-lakehouse.md`.

## Context

ADR 0006 parked DuckLake storage and catalog placement (row 4) for
Day 3. Intent W-2 forbade picking a warehouse at Pass 1. The
2026-06-09 medallion sketch is mail, not a cloud vendor.

`plans/modern.md` Milestone 2: configure DuckLake and DuckDB
**locally**. Legacy PostgreSQL is an observation environment only,
never a modern source database. A copy of the live warehouse is
not the second plant.

## Decision

Type 01 Gold is rebuilt in a **local** DuckLake catalog with a
**local** DuckDB engine, beside the repo, not as a cloud warehouse
and not as a clone of `northwind_legacy`.

Storage and catalog stay on the Constructor machine / working
tree lakehouse zone. The live plant’s Postgres remains frozen
observation (paid grain retrieved from OntoLayer, not copied as
the modern store).

The gate is a clean local environment that can rebuild the
approved Gold result. That is not a production warehouse claim.

## What this is not

A cloud vendor, a Terraform target, a copy of reporting tables
into DuckDB, or a serving API. FastAPI and MCP stay parked (ADR
0006 row 9). CI stays **no** (row 10).

## Consequences

- Bronze / Silver / Gold for Type 01 are local lakehouse facts.
- Golden-match attaches local Gold and landing to `contracts/`
  and to legacy observation. It does not require a remote catalog.
- Day 4 may serve **approved** Gold; it does not move this catalog
  to the cloud tonight.

## Evidence

- `docs/adrs/0006-later-nights-parked.md` — row 4, Day 3
- `plans/modern.md` — Milestone 2 “Configure DuckLake and DuckDB
  locally”; shared boundary “Legacy PostgreSQL — observation
  environment only”
- `docs/tech-spec-type-01-card-settlement.md` W-2 — no warehouse
  named at Intent
- Second Brain pack 01 — Helena is not sending a lakehouse model;
  rebuild beside Java. **Abstain** on DuckDB as an inbound decision
