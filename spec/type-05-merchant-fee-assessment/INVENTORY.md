# Inventory — what you received

**This folder is declarative only. There is no code in it, and there will not
be.** You receive a specification and proof of behaviour. You do not receive a
translation — if you did, you would be porting, and the referee would be
comparing a copy with its original.

---

## 1 · The specification — `contracts/types/05-merchant-fee-assessment/`

Four files, four questions. This is the whole of what "correct" means.

| File | Lines | Answers |
|---|---:|---|
| `layout.yaml` | 134 | How do I read the bytes? Semicolon delimiter, decimal commas, localized dates, quoting, record grammar, `canonical_rejection_codes` |
| `csv.yaml` | 45 | What do I emit? Sanitized columns, types, patterns, database target, natural key |
| `privacy.yaml` | 62 | What must never leave? Restricted fields, approved transformations, prohibited destinations |
| `reconciliation.yaml` | 111 | How do I know it added up? Controls, procedure order, report relation, tolerances (all zero), success criteria |
| `README.md` | 71 | Why this layout exists and what it exercises |

## 2 · The oracle — `contracts/types/05-merchant-fee-assessment/main/`

Five inputs, and for every one of them the **approved output**. Human-reviewed,
committed, and frozen. This is what will grade your work.

| Scenario | Input | Approved output |
|---|---|---|
| `valid-minimal` | `valid-minimal.csv` | `expected-sanitized.csv` · `expected-reconciliation.yaml` |
| `valid-boundary` | `valid-boundary.csv` | `expected-valid-boundary-sanitized.csv` · `…-reconciliation.yaml` |
| `rounding-half-up` | `rounding-half-up.csv` | `expected-rounding-half-up-sanitized.csv` · `…-reconciliation.yaml` |
| `malformed` | `malformed.csv` | `expected-malformed-rejection.yaml` — must be **refused** |
| **`DF-SOURCE-005`** | `df-source-005.csv` | `expected-df-source-005-finding.yaml` — must be **refused and attributed** |

**`DF-SOURCE-005` is the important one.** The source declares an assessed fee of
`0.99` where its own rows compute `1.00` under HALF_UP. You must reach `1.00`,
**preserve the `0.99` exactly as published**, refuse the batch, and attribute the
defect to the source system. Do not repair it. Repairing it destroys the evidence
that something upstream is broken.

## 3 · Proof the legacy behaves this way

Not a document — a command. Run it before you build anything:

```bash
make run TYPE=05 SCENARIO=valid-minimal     # accepted, reconciles MATCHED
make run TYPE=05 SCENARIO=DF-SOURCE-005     # refused, quarantined
```

The legacy vertical is installed and running: the Java privacy boundary, the
PostgreSQL loader, migrations `007`–`010`, the source generator, the independent
oracle, and the workflow adapter. **You may read any of it. You may not modify
any of it, and you may not port from it** — build from the specification above.

---

## Missing — this is the job

| | Status |
|---|---|
| `modern/ingestion/.../type05_*/` — model, parser, schema, writer, handler | ❌ **not built** |
| `modern/dbt/models/bronze/` — detail + control | ❌ **not built** |
| `modern/dbt/models/silver/` | ❌ **not built** |
| `modern/dbt/models/gold/` — reconciliation at the legacy grain | ❌ **not built** |
| `modern/dbt/tests/assert_type05_*` — release gate, conservation, privacy, HALF_UP | ❌ **not built** |
| `tests/modern/test_modern_type05.py` | ❌ **not built** |
| `"05"` in `pipeline.py` (4 maps), `registration.py`, `service.py` | ❌ **not wired** |
| `05` entries in `modern/dbt/models/*/schema.yml` and `sources.yml` | ❌ **not wired** |

Prove it:

```bash
ls modern/ingestion/src/northwind_pay/types/
→ type01_card_settlement  type02_instant_payment_events
  type03_payment_slip_settlement  type04_ted_transfer_settlement
```

Four. Not five.

## The arithmetic

**~5,800 lines of ground truth already exist. About 1,000 lines are missing.**

That thousand is the work. The other 5,800 is what will grade it.
