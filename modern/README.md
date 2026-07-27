# The modern platform

The **independent second implementation**. It reads the same contracts as
legacy, processes the same bytes, and must reach the same observable outcome —
without ever reading legacy's code.

**6,834 lines across 88 files.** Legacy is 29,622. That ratio is the point: the
difference is not cleverness, it is the absence of accumulated compensation.

```text
modern/
├── pipeline.py                    598   the seven stages, as plain functions
├── requirements.txt                23   pinned; deliberately not shared with legacy
│
├── ingestion/                    4,459   65% of the platform
│   ├── pyproject.toml
│   └── src/northwind_pay/
│       ├── common/                      money · privacy · documents · parquet
│       ├── intake/admission.py    100   the admission gate
│       ├── evidence.py             96   one packet per batch
│       └── types/
│           ├── type01_card_settlement/
│           ├── type02_instant_payment_events/
│           ├── type03_payment_slip_settlement/
│           └── type04_ted_transfer_settlement/
│
├── lakehouse/dlt/registration.py  148   landing Parquet → DuckDB catalog
│
├── dbt/                          1,054
│   ├── macros/                          release_gate · conserves_totals
│   ├── models/bronze/   8 sql            4 detail + 4 control
│   ├── models/silver/   4 sql
│   ├── models/gold/     4 sql
│   └── tests/          14 sql            singular assertions, tagged per type
│
├── dagster/…dagster.py            229   4 assets × 4 partitions + 3 checks
│
└── serving/                        245
    ├── service.py                 137   the two serving rules, enforced once
    ├── api/app.py                  50   FastAPI — routing only
    └── mcp/tools.py                58   MCP — routing only
```

Created at runtime and gitignored: `landing/`, `lakehouse/ducklake/`, `.venv/`.

---

## The one rule that defines this folder

> **Modern reads the contract. Modern never reads the Java.**

Reading the legacy implementation would be copying the answer and calling it a
proof: every defect in the old code would be reproduced faithfully and then
declared "parity". Independence is what makes a disagreement *informative* —
it is the reason five source defects were caught rather than absorbed.

Modern's inputs are `contracts/types/**` and raw bytes. Nothing else.

---

## `pipeline.py` — the spine

```bash
modern/pipeline.py --type 01 [--skip-legacy-comparison]
```

| Stage | Function | What it produces |
|---|---|---|
| 1–3 | `ingest` | Admit, parse, validate, publish canonical Parquet |
| 4 | `register` | The dlt registration boundary |
| 5 | `build_models` | dbt Bronze, Silver, Gold with their quality gates |
| 6 | `compare` | Golden-match against contract truth and legacy observation |
| 7 | `write_evidence` | One immutable, privacy-safe packet per batch |

Every stage is a plain function. `dagster/` calls **these same functions** —
it reimplements nothing. That is what makes *"direct and orchestrated execution
produce the same result"* a property of the code rather than a claim.

`--skip-legacy-comparison` exists because of a real defect found during the
autonomous run: golden-match once reported legacy parity **without contacting
legacy**, because `psycopg` was missing and a bare `except` swallowed it.
Skipping legacy is now explicit or the run fails. Never pass this flag on an
authoritative acceptance.

The same class of defect recurred on the rejected-batch path and was fixed in
the pre-workshop review — see
[`validation/README.md`](../validation/README.md), "Two referees, one
philosophy". Both halves now read a live `control.batches` / `reporting.*`
observation or refuse.

`pipeline.py` loads `.env` at import through `_load_dotenv()`, mirroring
`legacy/runner/config.py`. Without it `NWP_TOKENIZATION_KEY` is absent and
**every valid batch quarantines with `PRIVACY_VIOLATION`** — a failure that
reads like a privacy defect and is a missing environment file.

---

## `ingestion/` — five files per type, every type

| File | Owns |
|---|---|
| `model.py` | The typed record. Exact `Decimal`; no float touches money, ever |
| `parser.py` | Bytes → records. The largest file per type (247–351 lines) |
| `schema.py` | Contract validation and the canonical rejection codes |
| `writer.py` | Deterministic canonical Parquet |
| `handler.py` | The type's single entry point |

Package names match the contract slugs in `contracts/types/registry.yaml`
exactly. That is load-bearing, not cosmetic: it is how a reader confirms an
implementation exists for a registered type without running anything.

`common/` holds what must be decided once and only once — `money.py` (exact
arithmetic, HALF_UP), `privacy.py` (HMAC tokenization, masking, the output
scan), `documents.py` (Mod-11 CPF/CNPJ), `parquet.py` (byte-stable writes).

**Compare with legacy.** `legacy/runner/workflow_registry.py` puts all five
types in one 1,963-line file behind an ABC. Modern gives each type a package
with an identical file rhythm. Both are type-agnostic at the orchestration
layer; only one is browsable.

---

## `dbt/` — three layers and two gates

| Layer | Rule |
|---|---|
| **Bronze** | Typed and source-aligned. Never re-parses — ingestion already decided every value |
| **Silver** | Conforms and classifies. **Changes no monetary value** |
| **Gold** | Governed reconciliation at the *legacy* reporting grain, so golden-match compares like with like |

Every model and test carries a `type_NN` tag. `pipeline.py` scopes a
single-type run with `--select tag:type_NN`, so tagging is not decoration —
**an untagged or mistagged test silently never runs.**

Two gates are defined once in `macros/` and applied by every implemented type:

- **`release_gate(relation, delta_columns)`** — Gold may not publish an
  unexplained financial difference. `status` must be `MATCHED` and every named
  delta must be zero.
- **`conserves_totals(bronze, silver, amount_columns)`** — Silver must not
  change a row count or a monetary total. Compared with `IS DISTINCT FROM`, so
  a batch present on only one side fails instead of comparing `NULL`.

Current suite: **18 singular tests, 3–4 per type**, plus generic tests from the
`schema.yml` files. `make modern-dbt` runs everything: 20 models, 131 data
tests.

### Constant columns in Gold — read this before writing a test

Each Gold model carries **more delta columns than it computes.** Several are
literal `0` or `cast(0.00 as decimal(18, 2))`, and several `source_*` columns
are aliases of their `staged_*` counterparts — self-equal by construction.

They exist so the grain matches the legacy report exactly. They are **not
comparisons.** A test asserting one of them is zero passes without testing
anything.

The real deltas, and the only ones the release gate checks:

| Type | Real count delta | Real amount delta(s) |
|---|---|---|
| `01` | `count_delta` | `amount_delta` |
| `02` | `count_delta` | `net_amount_delta` |
| `03` | `count_delta` | `net_amount_delta` |
| `04` | **`transfer_count_delta`** | `net_amount_delta` |
| `05` | *(not built)* | *(not built)* — the contract specifies `count_delta` and `assessed_fee_delta`, `assessment_calculation_delta` |

Type `05` has no Gold model here. Its contract is deployed and its oracle is
docked in [`spec/`](../spec/type-05-merchant-fee-assessment/INVENTORY.md); the
vertical itself is the work order.

Note Type 04 does not have a `count_delta`. Each model's header comment lists
its own constants by name.

*Why this matters:* a green check that cannot fail is the exact failure mode
this whole repository exists to detect. Four such gates were found and closed
during the autonomous run; a fifth — the release gate covering only Type 01 —
was found during the pre-workshop review and closed by the macros above. Both
macros were verified falsifiable by mutation before being accepted.

---

## `dagster/` — orchestration owns no logic

Four assets (`landing_parquet` → `lakehouse_registration` → `dbt_models` →
`golden_match_report`), partitioned by type, plus three asset checks.

Two details worth knowing:

- The module **deliberately omits `from __future__ import annotations`.**
  Dagster resolves the `context` annotation at decoration time.
- The asset checks read **published evidence**, not the in-memory asset value.
  A partitioned asset input arrives as a mapping keyed by partition once more
  than one partition exists — and reading the artifacts is the stronger
  statement anyway: it asserts what was actually written.

Retries are configured for transient boundaries only. A contract, privacy, or
golden-match failure is deterministic; retrying it burns the same result again
and hides the signal.

---

## `serving/` — two rules, enforced once

`api/` and `mcp/` total 108 lines because they only route. Both call
`service.py`, which enforces:

1. **Only approved Gold is readable.** `GOLD_RELATIONS` is a closed map — there
   is no path to landing, Bronze, Silver, or any restricted zone, and no
   arbitrary SQL.
2. **An unresolved golden-match cannot be served at all** (HTTP 409). A broken
   comparison degrades *availability* rather than *correctness*.

---

## Running it

```bash
make modern-init                  # create modern/.venv from pinned requirements
make modern-run TYPE=01           # one type, end to end, closing golden-match
make modern-dbt                   # all models and tests, unscoped
make modern-check                 # 87 unit tests + strict mypy over 40 files
make modern-dagster TYPE=01       # the same stages, orchestrated
make modern-api                   # read-only API on 127.0.0.1:8099
make modern-rebuild TYPE=01       # wipe the lakehouse, rebuild from landing Parquet
```

`modern-rebuild` is safe by design: landing Parquet is immutable, so the
lakehouse is always reproducible from it.

---

## Two conventions that look like inconsistencies and are not

**Not every directory is a package.** `serving/` has `__init__.py` files
because it *is* imported as a package. `dagster/` and `lakehouse/dlt/` have
none because `pipeline.py` inserts them on `sys.path` and imports
`registration` as a top-level module. Adding `__init__.py` there would imply a
package structure that nothing uses.

**Modern's tests and referee live outside `modern/`.** `tests/modern/` and
`validation/golden-match/` are placed there by the approved tree in
[`plans/modern.md`](../plans/modern.md). The referee in particular should not
live inside a player's folder.

---

## Not here, on purpose

- **`observability/`** — named in the planned tree, scheduled for Milestone 6
  alongside authorization, audit, PII scans, and clean-environment CI. There is
  no empty directory standing in for it: `plans/modern.md` states that the tree
  "names trust boundaries; it does not authorize empty scaffolding."
- **Types `06`–`10`** — deferred until their contracts, legacy observations,
  and explicit scope approval exist.
- **Deployment targets and IaC** — out of scope per
  [DR-008](../docs/decisions/008-modern-pipeline-design.md#10-ci-and-deployment-boundary).

## What must not change

- **The independence rule.** No import, reference, or copy from `legacy/`.
- **The `type_NN` tags.** An untagged test does not run in a scoped build.
- **Zero tolerances.** There is no tolerance member anywhere in golden-match,
  and adding one is how an unexplained cent becomes an accepted cent.
- **`float` anywhere near money.** `common/money.py` is the only arithmetic.
