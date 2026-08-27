---
id: T-20260826-type-01-bronze
title: Type 01 Bronze is source-aligned landing records
status: ready
format_version: 3
profile: standard
effort: S
budget_iterations: 15
agent: any
parent: docs/seams.md
depends_on:
  - T-20260826-type-01-dlt-register
supersedes: (none)
touches_paths: []
creates_paths:
  - modern/dbt/models/bronze/
source_note: "docs/consensus-lakehouse.md signed 2026-08-26; ADR 0009 Bronze; seams.md seam 2 Medallion"
created: 2026-08-26T18:00:00Z
tags: [type-01, bronze, medallion, grain]
owner: Luan Moreno
priority: P1
severity: financial-critical
due_date: (none)
precondition: "docs/consensus-lakehouse.md canonical; dlt register gated before product write"
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

# Type 01 Bronze is source-aligned landing records

> **Why:** Medallion first grain. Minimal reinterpretation. Not a re-parse.

---

## Goal

Author and later execute Type 01 **Bronze** over registered landing.
Grain: one row per landing record. Keys: `batch_id` +
`source_record_number`. Already-Decimal, already privacy-safe.
Zero Parquet batches produce no Bronze. Do not retokenize. Do not
write frozen trees. Do not write product code while `signed_off: false`.

---

## Context

ADR 0009. Local DuckLake / DuckDB (ADR 0008). dbt does not retokenize
(ADR 0010). Staging is not Bronze.

---

## Behavior

- **B-1** — GIVEN registered landing WHEN Bronze is built THEN grain
  keys are `batch_id` + `source_record_number`.
- **B-2** — GIVEN Bronze WHEN inspected THEN it does not re-parse raw
  and does not emit clear PAN/CPF.
- **B-3** — GIVEN `B202607230000004` / 173.44 WHEN Bronze is built
  THEN that batch has no Bronze rows.
- **B-4** — no writes under `legacy/`, `contracts/`, `gen/`, `infra/`.

---

## Success Criteria

```bash
ROOT="$(git rev-parse --show-toplevel)"
SPEC="$ROOT/docs/tasks/T-20260826-type-01-bronze.md"
ADR="$ROOT/docs/adrs/0009-bronze-silver-gold-grains.md"
BRONZE="$ROOT/modern/dbt/models/bronze"

eval_1() {
  grep -q 'batch_id' "$ADR" || return 1
  grep -q 'source_record_number' "$ADR" || return 1
  grep -q 'Source-aligned' "$ADR" || grep -q 'source-aligned' "$ADR" || return 1
  grep -q 'source_record_number' "$SPEC" || return 1
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
  if [[ ! -d "$BRONZE" ]] || ! find "$BRONZE" -type f ! -path '*/.*' | grep -q .; then
    grep -q 'signed_off: false' "$SPEC" || return 1
    return 0
  fi
  find "$BRONZE" -type f | grep -q . || return 1
  find "$BRONZE" -type f -print0 | xargs -0 grep -l 'source_record_number' | grep -q . || return 1
  ! find "$BRONZE" -type f -print0 | xargs -0 grep -lE 'from[[:space:]]+legacy|import[[:space:]]+java|raw/incoming' | grep -q . || return 1
}
```

---

## Validation Card

```yaml
success_criteria:
  - id: eval_1
    description: Bronze grain is batch_id + source_record_number (ADR 0009)
    runnable: bash
    check_type: deterministic
    verifies: [B-1, B-4]
    terminal: true
    expected_duration_sec: 5
  - id: eval_2
    description: Absent Bronze allowed only while unsigned; present Bronze names the grain and does not parse raw
    runnable: bash
    check_type: deterministic
    verifies: [B-1, B-2, B-4]
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

(none — later execution: remove `modern/dbt/models/bronze/` files this leaf created.)

---

## Observability Hooks

(none until mesh.)

---

## Anti-Patterns

- **Don't invent joins onto Postgres.**
- **Don't retokenize.**
- **Don't treat Bronze as a new seam.**
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
