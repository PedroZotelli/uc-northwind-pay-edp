# Seams — Type 01 dlt → Gold

Pass 3 Decompose. Seamwise names: **seam**, **swimlane**, **leg**.
One owner per handoff. Papers live in `docs/`, not `cvg/docs/`.

The seam is a **handoff**, not a language. **Java vs Python is not a
seam.** Both plants read the same SFTP raw bytes; they do not own each
other. Bronze / Silver / Gold are **legs** on seam 2, not new seams.

## Steel thread

**Type 01 dlt → Gold.** This is the only lane for leaves tonight
(Pass 5). Seam 1 (ingest → landing) is **signed Tuesday** — do not
recut. Seam 3 waits for Day 4. Types `02`–`05` are not tonight’s
Task-Specs.

Landing facts already closed (ADRs 0001–0005): first write is
`modern/landing/` Parquet, not SFTP; five-file package; Decimal;
privacy dies at the parser; source lie keeps 173.44 and emits zero
Parquet.

Lakehouse facts (ADRs 0007–0011): dlt registers landing only;
DuckLake / DuckDB are local; Bronze / Silver / Gold grains; parser
owns privacy + Decimal; golden-match keys and two questions never
netted.

## Vocabulary

| Name | Meaning here |
|---|---|
| **Seam** | The cut: what is consumed, what is produced, who may write |
| **Swimlane** | Exactly one owning seat. Coordinates the write surface. Others read through the contract |
| **Leg** | Ordered, observable capability on that lane. Proof is a terminal, not a promise |

Two owners on one seam, or a seam with no owner, is refused.

## Seam list

### 1. Ingest → landing

| | |
|---|---|
| **Seam** | Type 01 raw intake → sanitized landing |
| **Swimlane** | Translator (SWE) — Night 2 |
| **When** | Night 2. Ingest Consensus signed 2026-08-25. Do not recut |
| **Consumes** | Same SFTP `raw/incoming` bytes, checksum, manifest last. `contracts/types/01-card-settlement/` |
| **Produces** | Accepted: atomic Parquet + readiness manifest in `modern/landing/`. Refused / source lie: **zero Parquet**, stable finding |
| **Write surface** | Type 01 five-file package (`model → parser → schema → writer → handler`) and `modern/landing/` |
| **Must not write** | `legacy/`, `contracts/`, `gen/`, `infra/`, SFTP `csv/outgoing`, lakehouse, Gold |
| **Reads through contract** | Legacy CSV, Postgres paid grain, Java — observation only. Never inputs |

**Legs** (ordered):

1. **Sense** — identity, checksum, manifest-last, replay. Same raw the live line already reads.
2. **Claim** — Type 01 parse, Decimal money, privacy at the parser, independent controls.
3. **Emit** — landing Parquet for `valid-minimal` (net 173.45, MATCHED shape); quarantine with zero Parquet for `df-source-001` (keep 173.44) and malformed.

Tuesday’s leaf attaches here. Do not recut.

### 2. dlt → Gold

| | |
|---|---|
| **Seam** | Immutable landing → governed Gold |
| **Swimlane** | Constructor (DE + analytics) — Night 3 |
| **When** | Tonight. Unparked in ADRs 0007–0011. Product write after lakehouse Consensus |
| **Consumes** | `modern/landing/` Parquet already published. Does **not** re-parse raw |
| **Produces** | Bronze → Silver → Gold; golden-match attached to contract and to legacy observation |
| **Write surface** | dlt register, local DuckLake / DuckDB, dbt Bronze → Silver → Gold, golden-match attachment. Constructor owns it |
| **Must not write** | Raw files, the Type 01 parser, frozen plant, landing bytes, Dagster, FastAPI |

**Legs** (ordered). Tonight’s leaves attach here only, after lakehouse sign.

1. **Register** — dlt registers `modern/landing/` Parquet (ADR 0007).
   No re-parse. Does not own money, privacy, or grammar. Zero Parquet
   (ADR 0005) → nothing to register for that batch.

2. **Medallion** — Bronze → Silver → Gold on local DuckLake / DuckDB
   (ADRs 0008–0010). Grains from tonight’s ADRs:
   - **Bronze** — source-aligned landing records. Keys: `batch_id` +
     `source_record_number`.
   - **Silver** — conformed grain. Record identity remains
     `batch_id` + `source_record_number`. Paid / batch grain:
     `batch_id` + `currency`.
   - **Gold** — governed reports and controls. Keys: `batch_id` +
     `currency`. May later be served; unresolved Gold is not
     servable. Staging is not Gold.
   dbt does not retokenize, unmask, or re-decode overpunch.

3. **Match** — attach `validation/golden-match/golden_match.py`
   (ADR 0011). Two questions, never netted: legacy parity, and
   business correctness. Aggregate keys `batch_id` + `currency`;
   record keys `batch_id` + `source_record_number`. No tolerance.
   Do not rewrite the referee. `df-source-001` keeps **173.44**.

### 3. Orchestrate + serve

| | |
|---|---|
| **Seam** | Gold + Type 01 landing → unattended run and read-only serve |
| **Swimlane** | Orchestrator — Night 4 |
| **When** | Day 4. Parked in ADR 0006 |
| **Consumes** | Approved Gold; Type 05 contract when that night opens. Not restricted raw |
| **Produces** | Dagster lineage / replay; Type 05 unattended including `HALF_UP`; read-only serve of approved Gold only |
| **Write surface** | Dagster, serving — **unparked on Day 4** |
| **Must not write** | Parser, landing contract, frozen `legacy/`, unresolved Gold |

**Legs** (named, not run tonight): orchestrate replay → Type 05 pill → serve approved Gold. FastAPI/MCP and CI stay parked (default CI = no).

## Refused cuts

- Java vs Python
- CSV-as-input to modern
- SFTP as modern destination
- Type 06 (not in this drop)
- Types `02`–`05` as tonight’s lanes
- Bronze, Silver, or Gold as **separate seams** (they are legs on seam 2)

## Handoff rule

Each seam has one owner. Translator does not write Gold. Constructor
does not rewrite landing. Orchestrator does not parse Type 01. Pass 5
writes Type 01 lakehouse leaves on **seam 2** after lakehouse
Consensus (`docs/consensus-lakehouse.md`). No lakehouse sign → skip
Gold. Do not recut seam 1. Do not task Types `02`–`05`.
