---
id: T-20260826-type-01-dlt-register
title: dlt registers Type 01 landing Parquet only (no re-parse)
status: ready
format_version: 3
profile: standard
effort: S
budget_iterations: 15
agent: any
parent: docs/seams.md
depends_on:
  - T-20260826-type-01-landing-emit
supersedes: (none)
touches_paths: []
creates_paths:
  - modern/lakehouse/dlt/
source_note: "docs/consensus-lakehouse.md signed 2026-08-26; ADR 0007; seams.md seam 2 Register"
created: 2026-08-26T18:00:00Z
tags: [type-01, dlt, register, lakehouse]
owner: Luan Moreno
priority: P1
severity: financial-critical
due_date: (none)
precondition: "docs/consensus-lakehouse.md canonical; landing emit gated before product write"
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

# dlt registers Type 01 landing Parquet only (no re-parse)

> **Why:** Seam 2 first leg. dlt is a register, not a parser.

---

## Goal

Author and later execute one **dlt register-only** path that consumes
immutable `modern/landing/` Parquet (and readiness manifest) already
published. It does **not** read SFTP raw, re-parse Type 01 bytes, own
money, privacy, or grammar, or invent a net. Zero Parquet batches are
not registered. Do not write `legacy/`, `contracts/`, `gen/`, or
`infra/`. Do not write product code while `signed_off: false`.

---

## Context

ADR 0007. Constructor swimlane. Parser/emit own grammar, Decimal, and
privacy. Local DuckLake comes after this leaf. Keep 173.44.

---

## Behavior

- **B-1** — GIVEN published landing Parquet WHEN dlt runs THEN it
  registers that landing only (ADR 0007).
- **B-2** — GIVEN raw `.dat` bytes WHEN dlt runs THEN it does not parse
  them, does not tokenize PAN/CPF, and does not decode overpunch.
- **B-3** — GIVEN zero Parquet for `B202607230000004` WHEN dlt runs
  THEN it registers nothing for that batch and does not invent Gold.
- **B-4** — GIVEN this leaf WHEN any file is written THEN the path is
  not under `legacy/`, `contracts/`, `gen/`, or `infra/`.

---

## Success Criteria

```bash
ROOT="$(git rev-parse --show-toplevel)"
SPEC="$ROOT/docs/tasks/T-20260826-type-01-dlt-register.md"
ADR="$ROOT/docs/adrs/0007-dlt-registers-landing-only.md"
CONSENSUS="$ROOT/docs/consensus-lakehouse.md"
DLT="$ROOT/modern/lakehouse/dlt"

eval_1() {
  grep -q 'registers landing only' "$ADR" || return 1
  grep -q 're-parse' "$ADR" || return 1
  grep -q 'no re-parse' "$SPEC" || return 1
  grep -q 'modern/landing/' "$SPEC" || return 1
  grep -q 'does not own money' "$SPEC" || grep -q 'own money' "$SPEC" || return 1
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
  if [[ ! -d "$DLT" ]] || ! find "$DLT" -type f ! -path '*/.*' | grep -q .; then
    grep -q 'signed_off: false' "$SPEC" || return 1
    return 0
  fi
  ! find "$DLT" -type f -name '*.py' -print0 | xargs -0 grep -lE 'raw/incoming|CRD_SETTLE01|overpunch' | grep -q . || return 1
  ! find "$DLT" -type f -print0 | xargs -0 grep -lE 'from[[:space:]]+legacy|import[[:space:]]+java|legacy\.processor' | grep -q . || return 1
  find "$DLT" -type f | grep -q . || return 1
}
```

---

## Validation Card

```yaml
success_criteria:
  - id: eval_1
    description: Register-only role, no re-parse, freeze fence, unsigned until gated
    runnable: bash
    check_type: deterministic
    verifies: [B-1, B-2, B-3, B-4]
    terminal: true
    expected_duration_sec: 5
  - id: eval_2
    description: Absent dlt path allowed only while unsigned; present dlt does not parse raw or import Java
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

(none — append-only spec. Later execution: remove `modern/lakehouse/dlt/` files this leaf created.)

---

## Observability Hooks

(none until mesh. Evidence may record a dlt register receipt; refused batches must not invent one.)

---

## Anti-Patterns

- **Don't re-parse raw.** Landing is the input.
- **Don't tokenize in dlt.** Privacy died at the parser.
- **Don't compute a net from `.dat`.** dlt does not own money.
- **Don't copy Postgres into dlt.** Observation only.
- **Don't author Dagster.**
- **Don't hand-edit `signed_off*`.**

---

## Do-Not-Touch

- `legacy/`
- `contracts/`
- `gen/`
- `infra/`
- `legacy/processor/src`
- Type 01 `parser.py` (Translator)
- `validation/golden-match/golden_match.py`

---

## Open Questions

(none — register-vs-load API is implementation inside this role; the role itself is closed.)
