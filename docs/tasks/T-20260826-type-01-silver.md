---
id: T-20260826-type-01-silver
title: Type 01 Silver is conformed grain on landing identity
status: ready
format_version: 3
profile: standard
effort: S
budget_iterations: 15
agent: any
parent: docs/seams.md
depends_on:
  - T-20260826-type-01-bronze
supersedes: (none)
touches_paths: []
creates_paths:
  - modern/dbt/models/silver/
source_note: "docs/consensus-lakehouse.md signed 2026-08-26; ADR 0009 Silver; seams.md seam 2 Medallion"
created: 2026-08-26T18:00:00Z
tags: [type-01, silver, medallion, grain]
owner: Luan Moreno
priority: P1
severity: financial-critical
due_date: (none)
precondition: "docs/consensus-lakehouse.md canonical; Bronze gated before product write"
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

# Type 01 Silver is conformed grain on landing identity

> **Why:** Medallion second grain. Conformed entities, signs, dates.
> Paid batch grain is `batch_id` + `currency`. Not a re-parse.

---

## Goal

Author and later execute Type 01 **Silver**. Record identity remains
`batch_id` + `source_record_number`. Batch-level business / paid grain
is `batch_id` + `currency`. Do not retokenize. Do not copy staging as
paid. Do not write frozen trees. Do not write product code while
`signed_off: false`.

---

## Context

ADR 0009. OntoLayer paid grain is `batch_id` + `currency` on
`reporting.card_settlement_reconciliation` — observation, not a
Silver source table.

---

## Behavior

- **B-1** — GIVEN Bronze WHEN Silver is built THEN record keys stay
  `batch_id` + `source_record_number` and paid grain is `batch_id` +
  `currency`.
- **B-2** — GIVEN Silver WHEN inspected THEN it does not re-parse raw
  and does not retokenize PAN/CPF.
- **B-3** — GIVEN the source lie WHEN Silver is built THEN
  `B202607230000004` has no Silver rows.
- **B-4** — no writes under `legacy/`, `contracts/`, `gen/`, `infra/`.

---

## Success Criteria

```bash
ROOT="$(git rev-parse --show-toplevel)"
SPEC="$ROOT/docs/tasks/T-20260826-type-01-silver.md"
ADR="$ROOT/docs/adrs/0009-bronze-silver-gold-grains.md"
SILVER="$ROOT/modern/dbt/models/silver"

eval_1() {
  grep -q 'Conformed' "$ADR" || grep -q 'conformed' "$ADR" || return 1
  grep -q 'source_record_number' "$SPEC" || return 1
  grep -q 'currency' "$SPEC" || return 1
  grep -q 'batch_id' "$SPEC" || return 1
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
  if [[ ! -d "$SILVER" ]] || ! find "$SILVER" -type f ! -path '*/.*' | grep -q .; then
    grep -q 'signed_off: false' "$SPEC" || return 1
    return 0
  fi
  find "$SILVER" -type f -print0 | xargs -0 grep -l 'source_record_number' | grep -q . || return 1
  find "$SILVER" -type f -print0 | xargs -0 grep -l 'currency' | grep -q . || return 1
  ! find "$SILVER" -type f -print0 | xargs -0 grep -lE 'from[[:space:]]+legacy|import[[:space:]]+java|raw/incoming' | grep -q . || return 1
}
```

---

## Validation Card

```yaml
success_criteria:
  - id: eval_1
    description: Silver grain is record identity plus paid batch_id+currency
    runnable: bash
    check_type: deterministic
    verifies: [B-1, B-4]
    terminal: true
    expected_duration_sec: 5
  - id: eval_2
    description: Absent Silver allowed only while unsigned; present Silver names both grains
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

(none — later execution: remove `modern/dbt/models/silver/` files this leaf created.)

---

## Observability Hooks

(none until mesh.)

---

## Anti-Patterns

- **Don't treat staging as paid.**
- **Don't retokenize.**
- **Don't invent extra join keys.**
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
