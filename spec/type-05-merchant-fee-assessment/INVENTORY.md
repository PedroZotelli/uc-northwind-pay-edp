# The pack — what you received

Everything below is **in this folder**. Open it, diff it, run against it. No
implementation code was delivered: you get the specification, real inputs, the
outputs the current system produces, one complete execution, and the shape of
what you must hand back.

```
spec/type-05-merchant-fee-assessment/
├── WORK-ORDER.md            the task, the guardrails, done-when
├── INVENTORY.md             this file
├── 01-specification/        the four contract YAMLs + the type README
├── 02-raw-in/               5 raw source files, exactly as the source emits them
├── 03-sanitized-out/        what the Java privacy boundary produces from them
├── 04-reconciliation/       the approved totals for each accepted batch
├── 05-rejections/           the approved refusals — including the source defect
├── 06-legacy-execution/     ONE REAL RUN. 13 artifacts, produced 2026-07-25
└── 07-deliverable-shape/    what a finished modernization looks like
```

---

## 01 · Specification

| File | Answers |
|---|---|
| `layout.yaml` | How do I read the bytes? Semicolon delimiter, decimal commas, localized dates, quoting, record grammar, `canonical_rejection_codes` |
| `csv.yaml` | What do I emit? Column list, types, patterns, database target, natural key |
| `privacy.yaml` | What must never leave? Restricted fields and their approved transformation |
| `reconciliation.yaml` | How do I know it added up? Controls, procedure order, report relation, tolerances (**all zero**) |
| `README.md` | Why this layout exists and what it exercises |

## 02 · Raw in — what the source sends

`valid-minimal.csv` · `valid-boundary.csv` · `rounding-half-up.csv` ·
`malformed.csv` · **`df-source-005.csv`**

Semicolon-delimited, decimal commas, UTF-8. Real restricted identifiers in the
tax-id column — this is production-shaped synthetic data, treat it as sensitive.

## 03 · Sanitized out — what the Java produces

The privacy boundary's output for each accepted batch. **This is the interface
you must reproduce.** Tax identifiers masked, amounts at contract scale, columns
in contract order.

Compare `02-raw-in/valid-minimal.csv` against
`03-sanitized-out/valid-minimal.sanitized.csv` side by side. Every
transformation between those two files is specified in `01-specification/`.
Nothing there is discretionary.

## 04 · Reconciliation — the approved totals

Per accepted batch: source count, staged count, applied count, gross, assessed
fee, calculated fee, the deltas, and `status: MATCHED`. Byte-exact. These are
what your Gold layer must reproduce.

## 05 · Rejections — the approved refusals

| File | Meaning |
|---|---|
| `malformed.rejection.yaml` | A grammar violation. Refused with a canonical code |
| **`df-source-005.finding.yaml`** | **The source lied.** It declares an assessed fee its own rows contradict |

`df-source-005` is the fixture that matters. The source declares `0.99`; the
rows compute `1.00` under HALF_UP. You must reach `1.00`, **preserve the `0.99`
exactly as published**, refuse the batch, and attribute the defect to the source
system. **Do not repair it.** Repairing it destroys the evidence that something
upstream is broken.

## 06 · Legacy execution — one real run

Batch `B202607230000401`, `valid-minimal`, executed 2026-07-25. Thirteen
artifacts, not logs:

| Artifact | Shows |
|---|---|
| `source-manifest.json` | What the source declared |
| `raw-publication.json` · `raw-intake.json` | Transport, hashes, zone transitions |
| `java-run.json` | What the Java computed vs what was declared |
| `sanitized-csv.sha256` · `raw-file.sha256` | Byte identity of both sides |
| `postgres-load.json` · `procedure-run.json` | The load and the governed procedures |
| `postgres-diagnostic.json` | An **independent** SQL recomputation of the controls |
| `reconciliation.json` | The reporting result |
| `expected-diff.json` | The oracle's verdict |
| `final-status.json` | The terminal outcome |

Reproduce it yourself:

```bash
make run TYPE=05 SCENARIO=valid-minimal     # accepted, MATCHED
make run TYPE=05 SCENARIO=DF-SOURCE-005     # refused, quarantined
```

## 07 · Deliverable shape — what you hand back

Taken from a type that **is** already modernized, so there is no ambiguity about
the target:

| File | |
|---|---|
| `EXAMPLE-golden-match.json` | The referee's verdict. `resolved: true`, `unexplained_count: 0` |
| `EXAMPLE-final-status.json` | The terminal outcome of a modern run |
| `EXAMPLE-difference-adjudication-source-defect.json` | How a source defect is classified rather than netted out |

Your Type 05 run must produce the same shapes:

```json
{ "batch_id": "B202607230000401", "outcome_class": "accepted",
  "resolved": true, "unexplained_count": 0, "differences": [] }
```

and for the defect batch, a difference classified `CONFIRMED_SOURCE_DEFECT` —
never `MODERN_DEFECT`, never absent.

---

## Missing — this is the job

| | Status |
|---|---|
| `modern/ingestion/.../type05_*/` — model, parser, schema, writer, handler | ❌ **not built** |
| `modern/dbt/models/{bronze,silver,gold}/` for this type | ❌ **not built** |
| `modern/dbt/tests/assert_type05_*` — release gate, conservation, privacy, HALF_UP | ❌ **not built** |
| `tests/modern/test_modern_type05.py` | ❌ **not built** |
| `"05"` in `pipeline.py`, `registration.py`, `service.py`, dbt schemas | ❌ **not wired** |

```bash
ls modern/ingestion/src/northwind_pay/types/
→ type01  type02  type03  type04       # four. not five.
```

## The arithmetic

**~5,800 lines of ground truth exist. About 1,000 lines are missing.**

That thousand is the work. The other 5,800 is what will grade it.
