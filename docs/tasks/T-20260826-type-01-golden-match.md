---
id: T-20260826-type-01-golden-match
title: Attach golden-match for Type 01 Gold (two questions, no tolerance)
status: ready
format_version: 3
profile: standard
effort: S
budget_iterations: 15
agent: any
parent: docs/seams.md
depends_on:
  - T-20260826-type-01-gold
supersedes: (none)
touches_paths: []
creates_paths:
  - evidence/modern/
source_note: "docs/consensus-lakehouse.md signed 2026-08-26; ADR 0011; seams.md seam 2 Match"
created: 2026-08-26T18:00:00Z
tags: [type-01, golden-match, referee]
owner: Luan Moreno
priority: P1
severity: financial-critical
due_date: (none)
precondition: "docs/consensus-lakehouse.md canonical; Gold gated before attach"
blocked_reason: (none)
security_class: restricted_synthetic_pii
source_action_item: (none)
tracker_ref: (none)
execution_backend: any
signed_off: false
signed_off_by: (none)
signed_off_at: (none)
accepted: false
accepted_by: (none)
accepted_at: (none)
evidence_refs: []
---

# Attach golden-match for Type 01 Gold (two questions, no tolerance)

> **Why:** Seam 2 last leg. Attach the referee. Do not rewrite it.

---

## Goal

Attach `validation/golden-match/golden_match.py` to Type 01 modern
observations (landing + Gold) and to contract plus legacy observation.
Two questions, **never netted**: legacy parity, and business
correctness. Aggregate keys `batch_id` + `currency`. Record keys
`batch_id` + `source_record_number`. No tolerance.
`DF-SOURCE-001` / 173.44 classifies `CONFIRMED_SOURCE_DEFECT` when
modern matches the contract terminal. Do **not** rewrite
`golden_match.py`. Do not write frozen trees. Do not write product
code while `signed_off: false`.

---

## Context

ADR 0011. Referee already on the tree. Golden-match is not the Dark
Factory. Keep 173.44.

---

## Behavior

- **B-1** — GIVEN `valid-minimal` WHEN match runs THEN both questions
  may be yes (net 173.45, MATCHED, `amount_delta` 0.00).
- **B-2** — GIVEN `DF-SOURCE-001` WHEN match runs THEN classification
  is `CONFIRMED_SOURCE_DEFECT`. Trailer stays 173.44. Zero unexplained.
- **B-3** — GIVEN the two questions WHEN a difference exists THEN they
  are not netted into one score. Tolerance is zero.
- **B-4** — GIVEN this leaf THEN `validation/golden-match/golden_match.py`
  is not modified. No writes under `legacy/`, `contracts/`, `gen/`,
  `infra/`.

---

## Success Criteria

```bash
ROOT="$(git rev-parse --show-toplevel)"
SPEC="$ROOT/docs/tasks/T-20260826-type-01-golden-match.md"
ADR="$ROOT/docs/adrs/0011-golden-match-keys-two-questions.md"
REF="$ROOT/validation/golden-match/golden_match.py"
CONSENSUS="$ROOT/docs/consensus-lakehouse.md"

eval_1() {
  test -f "$REF" || return 1
  grep -q 'two separate questions' "$ADR" || grep -q 'Two questions' "$ADR" || return 1
  grep -q 'CONFIRMED_SOURCE_DEFECT' "$SPEC" || return 1
  grep -q '173.44' "$SPEC" || return 1
  grep -q 'No tolerance' "$SPEC" || grep -q 'no tolerance' "$SPEC" || return 1
  grep -q 'Luan Moreno' "$CONSENSUS" || return 1
  grep -q 'signed_off: false' "$SPEC" || return 1
  awk '
    BEGIN { sec="" }
    /^---$/ { n++; next }
    n==1 && $0 ~ /^(touches_paths|creates_paths):/ { sec=$1; next }
    n==1 && sec != "" && $0 ~ /^[^[:space:]-]/ { sec="" }
    n==1 && sec != "" && $0 ~ /^[[:space:]]*-[[:space:]]*(legacy|contracts|gen|infra)\// { bad=1 }
    END { exit bad ? 1 : 0 }
  ' "$SPEC" || return 1
}

eval_2() {
  test -f "$REF" || return 1
  git -C "$ROOT" diff --exit-code -- "$REF" || return 1
  grep -q 'not rewrite' "$SPEC" || return 1
  grep -q 'batch_id' "$SPEC" || return 1
  grep -q 'currency' "$SPEC" || return 1
  grep -q 'source_record_number' "$SPEC" || return 1
}
```

---

## Validation Card

```yaml
success_criteria:
  - id: eval_1
    description: Referee on tree; two questions; CONFIRMED_SOURCE_DEFECT; keep 173.44; freeze fence
    runnable: bash
    check_type: deterministic
    verifies: [B-1, B-2, B-3, B-4]
    terminal: true
    expected_duration_sec: 5
  - id: eval_2
    description: golden_match.py is unmodified; keys are paid grain plus record identity
    runnable: bash
    check_type: deterministic
    verifies: [B-3, B-4]
    terminal: true
    expected_duration_sec: 5

retry_policy:
  max_iterations: 15
  circuit_breaker_no_progress: 3
  on_terminal_failure: park_with_context

agent_contract:
  version: 2
  read: [intent, behavior, contract, guardrails, operations]
  produce: [code, tests]
  required_tools: [git, bash]
  timeout_minutes: 30
  sandbox_type: host
  output_artifacts: []
  mcp_dependencies: []
  emit: [pass, fail, retry_with_reason, parked_with_context]
  backend_metadata: {}
```

---

## Exit Check

```bash
eval_1 && eval_2
```

---

## Rollback Plan

(none — later execution: remove `evidence/modern/` files this leaf
created. Never restore a patched `golden_match.py` as “the referee”.)

---

## Observability Hooks

(none until mesh. Watch classification codes; unexplained difference blocks serve.)

---

## Anti-Patterns

- **Don't rewrite `golden_match.py` to invent slack.**
- **Don't net the two questions.**
- **Don't call this the Dark Factory.**
- **Don't repair 173.44.**
- **Don't hand-edit `signed_off*`.**

---

## Do-Not-Touch

- `legacy/`
- `contracts/`
- `gen/`
- `infra/`
- `validation/golden-match/golden_match.py`

---

## Open Questions

(none)
