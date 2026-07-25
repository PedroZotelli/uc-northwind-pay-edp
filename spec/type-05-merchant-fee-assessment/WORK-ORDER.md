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
├── INVENTORY.md           what arrived and where each piece belongs
└── tests/                 the kit's own proof suite, awaiting installation
```

Already deployed by the platform team, ahead of this request:

- **the contract and its oracle** — `contracts/types/05-merchant-fee-assessment/`
- schema — migrations `007`–`010`, applied and checksummed
- `legacy/postgres/type05_loader.py`
- `legacy/processor/.../type05/` — the Java privacy boundary
- `gen/src/generators/type_05_*.py`
- `validation/oracle/type05_oracle.py`
- `Type05WorkflowAdapter` in the runner

## Your task

1. **Install the kit's proof suite.** Four test files in `tests/` here belong in
   the estate's suites — `INVENTORY.md` says where.
2. **Prove the legacy side runs.** `make run TYPE=05 SCENARIO=valid-minimal`
   must succeed and `DF-SOURCE-005` must be refused. Confirm the ground truth
   before you trust anything you build against it.
3. **Build the modern vertical.** Ingestion → canonical Parquet → dlt → DuckDB
   → dbt Bronze/Silver/Gold → golden-match → evidence. Types `01`–`04` are your
   pattern; follow their conventions rather than inventing new ones.

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
