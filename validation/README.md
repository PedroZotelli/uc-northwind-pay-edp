# The referees

**3,432 lines across 13 files.** Neither implementation may mark its own work.
This folder holds the two components that decide who is right, and it is
deliberately outside both `legacy/` and `modern/` — a referee that lives in a
player's folder is not a referee.

```text
validation/
├── oracle/                    3,116   the legacy referee
│   ├── canonical.py              40   strict scalar normalization, shared
│   ├── type01_oracle.py         545
│   ├── type02_oracle.py         499
│   ├── type03_oracle.py         524
│   ├── type04_oracle.py         488
│   ├── type05_oracle.py         487
│   └── tests/                   833   one suite per type
│
└── golden-match/                316   the modern referee
    └── golden_match.py
```

The size difference is not an accident, and neither is the fact that it used to
be larger. See "Two referees, one philosophy" below.

---

## `oracle/` — the legacy referee

One oracle per type, each independently recomputing what the contract says the
answer should be, then comparing it with what legacy actually produced. They
read `contracts/types/<slug>/main/` — the approved fixtures — and never read the
Java or the loaders.

Each oracle exposes the same three comparisons, which is what
`legacy/runner/workflow_registry.py` calls through its adapters:

| Function | Compares |
|---|---|
| `compare_sanitized_before_posting` | The sanitized CSV, before anything reaches PostgreSQL |
| `compare_post_db_reconciliation` | The reporting reconciliation, after the procedures ran |
| `compare_rejection` | The terminal refusal of a batch that was correctly refused |

Three outcome labels, and the distinction matters:

- `oracle_matched` — compared against an approved expectation and agreed;
- `internally_reconciled_unscored` — internally consistent, but no approved
  artifact exists to score it against;
- `rejected_unscored` — correctly refused, so there is nothing to score.

An oracle never reports "pass" for something it did not actually compare. That
is the whole reason the middle label exists.

### `canonical.py` — 40 lines that set the rule for the folder

```python
def canonical_money(value: object) -> str | None:
    """Return an exact scale-two money lexeme or reject it.

    Oracles compare observations; they must never repair observations by
    rounding, padding, accepting binary floats, or normalizing negative zero.
    """
```

**This is the governing principle of `validation/`.** A referee that quietly
rounds `173.445` to `173.44` has invented a tolerance, and a tolerance is how an
unexplained cent becomes an accepted cent.

---

## `golden-match/` — the modern referee

`golden_match.py` asks two separate questions of every batch, and keeps them
separate all the way into the evidence packet:

1. **Legacy parity** — did modern reach the same observable outcome as legacy?
2. **Business correctness** — did modern satisfy the approved contract?

A source defect makes those answers differ, which is exactly why they are never
netted out. Every difference is classified as one of six:

| Classification | Explained? |
|---|:-:|
| `CONFIRMED_SOURCE_DEFECT` | ✓ |
| `CONFIRMED_LEGACY_DEFECT` | ✓ |
| `APPROVED_BEHAVIOR_CHANGE` | ✓ |
| `MODERN_DEFECT` | — |
| `CONTRACT_AMBIGUITY` | — |
| `UNRESOLVED` | — |

`Comparison.resolved` requires **no unexplained difference and every check
true**. `modern/serving/service.py` refuses to serve an unresolved batch, so
this property is load-bearing at the API boundary, not just in a report.

There is no tolerance member anywhere in this module, and adding one would
defeat its purpose.

### Accepted and rejected batches are compared differently

| | Accepted | Rejected |
|---|---|---|
| Record level | modern Parquet vs `expected-*-sanitized.csv` | *nothing — there are no rows* |
| Aggregate | modern Gold vs contract **and** vs `reporting.*` | — |
| Terminal | — | modern status/code vs **`control.batches`** and vs the contract |
| Controls | — | declared vs independently computed |

Inventing empty rows so a rejected batch can be "compared like a successful one"
would hide the difference that matters, so it is not done.

---

## Two referees, one philosophy — and where it had drifted

Both referees exist to compare, never to repair. Two defects found in the
pre-workshop review had drifted from that:

**1. The rejected half never contacted legacy.** `modern/pipeline.py` built the
"legacy" terminal observation out of the contract's own expectation:

```python
legacy_final = {"status": expectation.get("expected_status"),      # ← the contract
                "code":   expectation.get("expected_code")}
```

So `legacy_matches_contract_status` and `legacy_matches_contract_code` compared
the contract with itself — **two checks that could not fail** — while the
emitted `Difference` recorded `reference_name="legacy-observation"` for a
legacy observation that was never read.

Fixed: `_legacy_terminal_status()` reads the real `control.batches` row
read-only; `compare_rejection` now takes `Mapping | None` and, when legacy is
deliberately skipped, records `legacy_terminal_comparison_skipped_by_request`
instead of asserting something trivially true. A missing legacy row is a hard
failure, not a silent pass.

**2. The money renderer rounded.** `_money` was
`f"{Decimal(str(value)):.2f}"`, which pads and rounds — and rounds
ROUND_HALF_EVEN, so `173.445` became `173.44` where the contract mandates
HALF_UP and `173.45`. Latent, because every live input is already
`decimal(18, 2)`, but it is precisely the silent tolerance the module's own
docstring denies having. It now refuses a value that is not already exact.

Both were found by reading, not by a failing gate — which is the point. Both are
now covered by `tests/modern/test_golden_match.py`.

---

## Verification

| Referee | Tests |
|---|---|
| `oracle/` | `validation/oracle/tests/` — 833 lines, one suite per type, run by `make check` |
| `golden-match/` | `tests/modern/test_golden_match.py` — run by `make modern-check` |

`golden-match` had **no unit tests at all** until the pre-workshop review: 316
lines with authority over what may be served, exercised only end to end, where a
check that cannot fail is invisible. Two of its tests are regression guards for
the defects above.

The tests live in `tests/modern/` rather than beside the source because
`golden-match` contains a hyphen and therefore cannot be an importable package —
it is put on `sys.path` by `modern/pipeline.py`. The approved tree in
[`../plans/modern.md`](../plans/modern.md) places modern's tests there.

## What must not change

- **Referees never repair.** No rounding, padding, coercion, or tolerance — in
  either half of this folder.
- **The two questions stay separate.** Merging legacy parity with business
  correctness makes a source defect indistinguishable from a modern one.
- **A referee never asserts what it did not observe.** If a channel is skipped,
  say so; do not synthesize it and check it against itself.
- **`resolved` keeps requiring both** no unexplained difference *and* all checks
  true. It gates the serving layer.
