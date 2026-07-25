# Work order — Type 05, Merchant Fee Assessment

**Received:** 2026-07-25 · **Requested by:** partner integration
**Target:** the modern platform, end to end
**Autonomy:** L3 — unattended, guardrails below

---

## What arrived

A new payment file type. Percentage fees assessed per merchant, semicolon CSV
with decimal commas, HALF_UP rounding. The kit in this folder is the
**specification and the ground truth**: five scenarios, and for every one of
them the approved output.

```
spec/type-05-merchant-fee-assessment/
├── WORK-ORDER.md          this file
├── INVENTORY.md           a guided tour of everything below
├── 01-specification/      the four contract YAMLs
├── 02-raw-in/             5 raw source files
├── 03-sanitized-out/      what the Java privacy boundary produces
├── 04-reconciliation/     the approved totals
├── 05-rejections/         the approved refusals, incl. the source defect
├── 06-legacy-execution/   one real run, 13 artifacts
└── 07-deliverable-shape/  what a finished modernization looks like
```

**No implementation code is delivered.** You get the specification, real inputs,
the outputs the current system produces, one complete execution, and the shape
of the deliverable. You do not get a translation — if you did, you would be
porting, and the referee would be comparing a copy with its original.

Already deployed by the platform team, ahead of this request:

- **the contract and its oracle** — `contracts/types/05-merchant-fee-assessment/`
- schema — migrations `007`–`010`, applied and checksummed
- `legacy/postgres/type05_loader.py`
- `legacy/processor/.../type05/` — the Java privacy boundary
- `gen/src/generators/type_05_*.py`
- `validation/oracle/type05_oracle.py`
- `Type05WorkflowAdapter` in the runner

## ⚠️ Acceptance criterion #1 — the money

Everything else is secondary to this. The `DF-SOURCE-005` batch carries a
declared assessed fee its own detail rows contradict:

| | Required |
|---|---|
| Your parser must compute | **`1.00`** — the true HALF_UP value |
| The source's declaration | **`0.99`, preserved byte-exact. Never repaired.** |
| golden-match classification | **`CONFIRMED_SOURCE_DEFECT`** — never `MODERN_DEFECT`, never absent |
| Terminal outcome | refused, quarantined, zero rows written |
| `assessment_calculation_delta`, accepted batches | exactly **`0.00`** |
| `unexplained_count` | **`0`** |

**Do not repair the source's number.** A system that silently corrects its input
has destroyed the evidence that something upstream is broken. Compute the truth,
preserve the lie, refuse the batch, name who lied.

> ⚠️ **Python's default rounding is `ROUND_HALF_EVEN`. This contract mandates
> `HALF_UP`.** Both `round()` and `f"{value:.2f}"` will quietly give you banker's
> rounding — `0.125` becomes `0.12`, not `0.13`. Use
> `Decimal.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)`.
>
> Get this wrong and every structural test still passes: the tokens are
> well-formed, the row counts match, the types are right. Only byte-for-byte
> comparison against the approved output catches a one-cent error.

## Your task

1. **Read the pack.** `INVENTORY.md` walks all seven folders. Start by diffing
   `02-raw-in/valid-minimal.csv` against
   `03-sanitized-out/valid-minimal.sanitized.csv` — every transformation between
   them is specified in `01-specification/` and none of it is discretionary.
2. **Prove the legacy side runs.** `make run TYPE=05 SCENARIO=valid-minimal`
   must succeed and `DF-SOURCE-005` must be refused. Confirm the ground truth
   before you trust anything you build against it.
3. **Build the modern vertical.** Ingestion → canonical Parquet → dlt → DuckDB
   → dbt Bronze/Silver/Gold → golden-match → evidence. Types `01`–`04` are your
   pattern; follow their conventions rather than inventing new ones.

**Build from the specification, not from the legacy code.** You may read
`legacy/` to understand behaviour. Porting it reproduces its defects and then
calls the result parity.

## Frozen — read, never write

`legacy/` · `contracts/` (other types) · `gen/` · `infra/` · applied migrations

Never edit an expected value, fixture, or oracle to turn a red gate green. If a
gate cannot pass without changing frozen truth, **stop and say so.**

## Forbidden

**Do not read git history for a previous modern implementation of this type.**
Build from the contract. If you look, say that you looked.

## Halt immediately on

- a restricted value reaching any sanitized output, log, or evidence file
- any write to a frozen path
- a gate that cannot pass without changing frozen truth
- Docker unavailable

## Done when

```bash
make run TYPE=05 SCENARIO=valid-minimal     # legacy accepts
make run TYPE=05 SCENARIO=DF-SOURCE-005     # legacy refuses
make modern-run TYPE=05                     # golden-match resolves
make modern-dbt                             # every model and data test green
make modern-check                           # units + strict mypy
make test-e2e TYPE=all                      # 01-05, nothing regressed
```

and the evidence shows:

| Batch | Expected |
|---|---|
| `B202607230000401` `valid-minimal` | succeeded · `resolved: true` · `unexplained_count: 0` |
| `B202607230000404` `rounding-half-up` | succeeded · HALF_UP proven at the cent |
| `B202607230000405` `DF-SOURCE-005` | refused · `CONFIRMED_SOURCE_DEFECT` |

The last row is the one that matters. The source declares an assessed fee of
`0.99` where its own rows compute `1.00`. Both stacks must reach `1.00`,
**preserve the `0.99` exactly as published**, refuse the batch, and attribute
the defect to the source system.

## Report

Commit in small gate-passing increments. When you finish, write down what you
had to work out — a convention you inferred, a gate that proved nothing, a place
the old type list was hardcoded. The sixth type should be cheaper than this one.
