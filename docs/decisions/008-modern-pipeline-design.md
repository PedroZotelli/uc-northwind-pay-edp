# 008 — Modern pipeline design: the ten decisions M0 defers

- Date: 2026-07-24
- Phase: 3, Milestone M0
- Status: accepted

## Context

`plans/modern.md` lists ten decisions as "pending before modern coding" and
defers them to a future design turn. The autonomous mandate makes that turn
this one. M0's gate is that every handoff has one owner, one input contract, and
one accepted output.

The binding constraint throughout: modern must be an **independent second
implementation**. It may not call the Java processor, import its parsing logic,
reuse the stored procedures, or read legacy CSV or PostgreSQL as input. Legacy
observations are comparison evidence only. Anything that makes modern easier by
borrowing from legacy destroys the thing golden-match is supposed to measure.

## Decisions

### 1. Python version, packaging, validation

Python 3.12 in `modern/.venv`, driven by a pinned `modern/requirements.txt`,
imported through `PYTHONPATH=modern/ingestion/src`. No build backend.

The environment is deliberately **separate from `legacy/runner/.venv`**. Sharing
one resolver would let a legacy pin constrain modern, or worse, let a modern
package land in the interpreter that runs the frozen oracle. Two environments
cost one extra `pip install` and buy genuine independence.

Validation is hand-written over `dataclasses` with `Decimal` money, not a
coercing library. Pydantic is present but confined to the serving layer, where
its job is request/response shape rather than financial semantics. A library
that silently coerces `"173.44"` to a float is precisely the failure this
system exists to detect.

### 2. Canonical Parquet

| Property | Value |
|---|---|
| Engine | `pyarrow` 25.0.0 |
| Money | `decimal128(18, 2)`, never float |
| Compression | ZSTD level 3 |
| Row groups | One per batch |
| Dictionary encoding | Off |
| Statistics | Off |
| Format version | 2.6 |
| Row order | `source_record_number` ascending |
| Partitioning | None inside the file; one file per batch on disk |
| Metadata | Contract identity, batch, raw SHA-256, writer version |

Statistics and dictionary encoding are disabled because both embed
data-dependent structures that can vary across runs; with them off the file is a
pure function of the rows and the schema, so the SHA-256 of the Parquet file is
itself a determinism check. Partitioning is per-file rather than Hive-style
because a batch is the unit of atomicity, replay, and quarantine everywhere else
in this system, and matching that makes the landing zone immutable per batch.

### 3. The dlt role

**Registration, never transformation.** dlt loads already-canonical landing
Parquet into DuckDB Bronze-input tables and owns load identity and state. It
does not parse, does not derive a value, and does not re-shape a column. The
writer owns Parquet; dlt owns "this file became these rows, under this load id".

`plans/modern.md` requires exactly one owner per handoff, and the tempting
alternative — letting dlt infer schema from raw and do the typing — would give
Parquet and dlt overlapping ownership of the same decision.

### 4. DuckLake and DuckDB

The lakehouse is `modern/lakehouse/ducklake/northwind_modern.duckdb` with four
schemas: `landing` (views over the immutable Parquet tree), `bronze`, `silver`,
`gold`. DuckDB is the catalog; the DuckLake role is the immutable per-batch
Parquet tree plus the catalog that registers it. The database file is disposable
runtime state and is rebuilt from landing, so the Parquet tree — not the
database — is the durable artifact.

### 5. Bronze, Silver, Gold grains and keys

| Model | Grain | Key | Owner |
|---|---|---|---|
| `bronze_card_settlement` | one sanitized detail record | `(batch_id, source_record_number)` | dbt, source-aligned |
| `silver_card_settlement` | one conformed movement | `(batch_id, source_record_number)` | dbt, conformed |
| `gold_card_settlement_reconciliation` | one batch and currency | `(batch_id, currency)` | dbt, governed |

The Gold grain deliberately equals the legacy `reporting.*_reconciliation`
grain. Golden-match then compares like with like instead of comparing an
aggregate to a reshaped aggregate, which is where parity comparisons usually go
wrong.

### 6. Rule allocation between ingestion and dbt

Ingestion owns transport, encoding, positions, grammar, overpunch, exact money,
privacy transformation, and independent batch controls. dbt owns aggregation,
conformance, reconciliation, and quality. **dbt never re-parses and ingestion
never aggregates across batches.** The boundary is the Parquet file: everything
upstream is about reading bytes correctly, everything downstream is about
combining already-correct records.

### 7. Golden-match keys

Two levels, both compared against two references:

- **Record level**, keyed `(batch_id, source_record_number)` — modern sanitized
  records against the contract's `expected-sanitized.csv` and against the legacy
  sanitized CSV observation.
- **Aggregate level**, keyed `(batch_id, currency)` — modern Gold against the
  contract's `expected-reconciliation.yaml` and against legacy
  `reporting.*_reconciliation`.

Rejected batches are compared on terminal status, stable code, zero Parquet,
zero Gold, zero business mutation, and peer continuation — not on rows, because
there are none and inventing empty rows to compare would hide the difference
that matters.

Every difference is classified as exactly one of `CONFIRMED_SOURCE_DEFECT`,
`CONFIRMED_LEGACY_DEFECT`, `MODERN_DEFECT`, `APPROVED_BEHAVIOR_CHANGE`,
`CONTRACT_AMBIGUITY`, or `UNRESOLVED`. There is no tolerance member: the release
gate permits no unexplained financial difference and a configurable tolerance is
how one gets introduced quietly.

### 8. Dagster model

One asset per deterministic stage — landing Parquet, dlt registration, dbt
Bronze/Silver/Gold, golden-match, evidence — partitioned by batch identity with
a dynamic partition per canonical batch. Retries only on genuinely transient
boundaries; a contract, privacy, or golden-match failure is terminal and never
retried, because retrying a deterministic failure just burns the same result
again. Asset checks carry the privacy scan and the golden-match verdict, so a
red check blocks Gold rather than annotating it.

Parsing and business logic stay entirely outside orchestration code: Dagster
calls the same handler functions the CLI calls, which is what makes "direct and
orchestrated execution produce the same result" testable rather than aspirational.

### 9. Serving

FastAPI, read-only, over an approved Gold snapshot: `/health`,
`/batches/{batch_id}/status`, `/batches/{batch_id}/reconciliation`,
`/batches/{batch_id}/golden-match`. MCP exposes the same three narrow tools —
batch status, reconciliation, difference explanation — by calling the identical
service functions.

No arbitrary SQL, no restricted zone access, and no serving of a batch whose
golden-match is unresolved. The last rule is enforced in the service layer, not
in the caller, so an unresolved batch cannot be served by any route.

### 10. CI and deployment boundary

Out of scope, explicitly. Local clean-environment reproduction is proven by
`make modern-rebuild`; no CI pipeline, container image, or deployment target is
selected, and no Terraform is written. Claiming CI readiness from local proof is
one of the things `plans/modern.md` forbids.

## Alternatives considered

- **One shared virtual environment.** Rejected: it couples the frozen oracle's
  dependency set to the new implementation's.
- **dlt owning ingestion end to end.** Rejected: it would make dlt a second
  parser and duplicate ownership of typing and privacy.
- **Hive-partitioned landing.** Rejected: the batch is the atomic unit
  everywhere else; per-file-per-batch keeps immutability and replay simple.
- **A tolerance threshold on financial comparison.** Rejected outright.
- **Reusing the legacy Java processor through a subprocess** to produce modern
  Parquet. Rejected: it would make golden-match compare a system with itself.
- **Pydantic models for the financial domain.** Rejected for coercion risk;
  retained only at the serving edge.

## Consequences

- Modern and legacy can disagree, and when they do the difference is real
  signal rather than an artifact of shared code.
- The Parquet SHA-256 becomes a determinism gate for free.
- Two environments must be maintained. `make modern-init` creates the modern
  one; nothing in `make init` changes.
- Gold cannot be served until golden-match resolves, which means a broken
  comparison degrades availability rather than correctness. That is the intended
  trade.
