# Verification map

**33,484 lines of test code across 100 files in six locations** — more test code
than the entire legacy production estate (29,732 lines). This page is the index
to all of it.

> Until the pre-workshop review this file described **Type 01 only**, because
> Type 01 was the first vertical slice and the page was never updated. Anyone
> reading it concluded four fifths of the estate was untested. It now covers all
> five types.

---

## The six locations

Tests do not all live under `tests/`. They live with the thing they prove.

| Location | Lines | Files | Proves |
|---|---:|---:|---|
| `tests/` | 22,438 | 43 | The legacy estate, live and end to end |
| `legacy/processor/src/test/` | 4,616 | 7 | The Java processor, per type |
| `gen/tests/` | 3,757 | 26 | DataGen's bytes, per type |
| `factory/tests/` | 1,761 | 10 | The detector: contract, unit, security, live |
| `validation/oracle/tests/` | 833 | 6 | The independent correctness oracles |
| `modern/dbt/tests/` | 79 | 18 | The lakehouse gates, tagged per type |

Inside `tests/`:

| Directory | Lines | Files | Scope |
|---|---:|---:|---|
| `end-to-end/` | 6,445 | 7 | Live SFTP, Java, PostgreSQL, evidence |
| `contracts/` | 6,204 | 5 | Cross-component contract oracles, one per type |
| `unit/` | 6,001 | 18 | Loaders, workflows, worker, recovery, facade |
| `postgres/` | 2,022 | 5 | Real `COPY`, procedures, rollback |
| `modern/` | 943 | 5 | Modern ingestion and the golden-match referee |
| `security/` | 778 | 2 | Adversarial worker and transport probes |

`security/test_worker_security.py` is the one to read if you read only one file:
15 tests covering symlinked cache artifacts, path traversal in manifests,
declared-size bounds enforced *before* download, a lock that refuses a symbolic
link without touching its target, and
`test_sensitive_exception_text_never_enters_batch_outcome`.

---

## Coverage by type

| Surface | 01 | 02 | 03 | 04 | 05 |
|---|:-:|:-:|:-:|:-:|:-:|
| Contract bytes and layout — `gen/tests/contract/` | ✓ | ✓ | ✓ | ✓ | ✓ |
| Generator encoding — `gen/tests/unit/` | ✓ | ✓ | ✓ | ✓ | ✓ |
| Generator privacy — `gen/tests/security/` | ✓ | ✓ | ✓ | ✓ | ✓ |
| Java conversion and privacy — `legacy/processor/src/test/` | ✓ | ✓ | ✓ | ✓ | ✓ |
| Cross-component contract — `tests/contracts/` | ✓ | ✓ | ✓ | ✓ | ✓ |
| Independent oracle — `validation/oracle/tests/` | ✓ | ✓ | ✓ | ✓ | ✓ |
| Loader boundary — `tests/unit/test_typeNN_loader.py` | ✓ | ✓ | ✓ | ✓ | ✓ |
| Typed workflow — `tests/unit/test_typeNN_workflow.py` | ✓ | ✓ | ✓ | ✓ | ✓ |
| Transactional rollback — `tests/postgres/` | ✓ | ✓ | ✓ | ✓ | ✓ |
| Live acceptance — `tests/end-to-end/run_typeNN_suite.py` | ✓ | ✓ | ✓ | ✓ | ✓ |
| Lakehouse gates — `modern/dbt/tests/` | ✓ | ✓ | ✓ | ✓ | ✓ |

The matrix is complete. Two Type 02 cells were empty until the pre-workshop
review — no test anywhere referenced `Type02WorkflowAdapter`, and Type 02 was
the only type without a dedicated
`test_oracle_callback_failure_rolls_back_the_entire_batch` proof. Both are now
filled:

- `tests/unit/test_type02_workflow.py` — routing, typed Java dispatch, the
  oracle input, evidence allowlisting, and the rule that a wrongly typed
  declaration becomes *absent* rather than a guessed value.
- `tests/postgres/test_type02_loader_rollback.py` — proves the `COPY`, both
  procedures, the reporting row, and all four control-plane records disappear
  when the oracle rejects at the reconciliation boundary.

The rollback test's emptiness assertions were checked against a live database
for vacuity: all seven tables genuinely hold rows for the canonical Type 02
batch and none for the probe. A count that is always zero proves nothing.

Type 02's loader unit test remains the thinnest at 3 tests / 87 lines, against
Type 03's 7 tests / 219 lines. That is the next gap worth closing.

---

## Two acceptance implementations, not one

```text
run_type01_suite.py   590 lines   bespoke
run_type02_suite.py   524 lines   bespoke
run_type03_suite.py     7 lines   → typed_acceptance.main_for_type("03")
run_type04_suite.py     7 lines   → typed_acceptance.main_for_type("04")
run_type05_suite.py     7 lines   → typed_acceptance.main_for_type("05")
```

`typed_acceptance.py` (1,685 lines) is a declarative harness. Its
`TypeAcceptanceSpec` pins scenarios, business and reporting tables, zero-delta
columns, privacy columns **with their regex patterns**, a privacy-consistency
callable, the exact Java field sets for success and rejection, and forbidden
evidence keys. Its registry contains exactly `"03"`, `"04"`, `"05"`.

Types 01 and 02 predate it and keep 1,114 lines of hand-written acceptance code.

All five run under `make test-e2e TYPE=all`, so nothing is unproven. But **the
acceptance contract lives in three places**, and nothing forces the two bespoke
suites to assert what the spec requires. Porting them to the harness is the right
eventual move; it is not a change to make casually, because the bespoke suites
are currently the only proof for the two most-demoed types.

---

## Type 01 is the exception everywhere

Worth knowing before reading any per-type code, because the pattern repeats:

| Area | How Type 01 differs |
|---|---|
| `legacy/postgres/` | Generic table names, no `type01` migration, procedures split into `002` |
| `legacy/runner/` | Defines 11 adapter members; 02–05 override four more evidence hooks |
| `modern/dbt/` | Was the only type with a release gate or conservation test until the review |
| `tests/end-to-end/` | Bespoke suite; 03–05 use the shared harness |
| `gen/` | `type_01` module naming vs `type01` in the legacy runtime |

Nothing here was ever wrong. Each time the estate generalised, Type 01 was left
as it was and the new mechanism started at the next type. That is what a real
legacy estate looks like, and it is the honest answer to "why is migration hard?"

DataGen uses `type_01` to match its `generators/type_01_*` convention; the legacy
runtime uses `type01` to match Java packages and the loader/workflow convention.
Both identify file type `01`. This is a layer-specific naming convention, not two
implementations.

---

## Running them

```bash
make check                  # source, build, Java, and the fast suites
make test-postgres          # rollback-only, against a live database
make test-type01            # the full Type 01 proof on a fresh runtime
make test-e2e TYPE=all      # live acceptance, all five types
make test-worker-e2e        # the autonomous worker on a clean runtime
make test                   # check + test-postgres + worker acceptance
make modern-check           # modern ingestion and golden-match units + mypy
make modern-dbt             # 20 models and 131 data tests
make df-check               # detector contract, unit, and security + mypy
```

Live suites do not erase runtime state, and canonical batch IDs are immutable.
**Clean or isolate the runtime before repeating a live suite** —
`make clean CONFIRM=clean-runtime`, then `make deploy`.

## What must not change

- **A gate that cannot fail is worse than no gate.** Six have been found in this
  repository so far. When adding one, prove it red before accepting it green.
- **`modern/dbt/` type tags.** An untagged test silently never runs in a scoped
  build.
- **Fixture names.** They are resolved by path across four languages.
