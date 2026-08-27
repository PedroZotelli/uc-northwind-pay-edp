---
id: T-20260826-type-01-landing-emit
title: Emit Type 01 landing Parquet for valid-minimal; zero Parquet for 173.44
status: ready
format_version: 3
profile: standard
effort: S
budget_iterations: 15
agent: any
parent: docs/seams.md
depends_on:
  - T-20260825-type-01-landing-parser
supersedes: (none)
touches_paths: []
creates_paths:
  - modern/ingestion/src/northwind_pay/types/01-card-settlement/model.py
  - modern/ingestion/src/northwind_pay/types/01-card-settlement/schema.py
  - modern/ingestion/src/northwind_pay/types/01-card-settlement/writer.py
  - modern/ingestion/src/northwind_pay/types/01-card-settlement/handler.py
source_note: "docs/consensus-lakehouse.md signed 2026-08-26; ADR 0001/0005; seams.md seam 1 emit + seam 2 consumes landing"
created: 2026-08-26T18:00:00Z
tags: [type-01, landing, emit, parquet]
owner: Luan Moreno
priority: P1
severity: financial-critical
due_date: (none)
precondition: "docs/consensus-lakehouse.md records canonical lakehouse sign; parser leaf exists; do not execute product code until this leaf is gated"
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

# Emit Type 01 landing Parquet for valid-minimal; zero Parquet for 173.44

> **Why:** Seam 2 consumes published landing. Parquet is missing on disk.
> This leaf is the Type 01 **emit** remainder (schema / writer / handler),
> not dlt and not Gold.

---

## Goal

Author and later execute Type 01 **model, schema, writer, and handler**
so `valid-minimal` (batch `B202607230000001`, net **173.45**) publishes
atomic sanitized Parquet plus readiness manifest under `modern/landing/`,
and `df-source-001` / batch `B202607230000004` / trailer **173.44** emits
**zero** Parquet. First write is landing, not SFTP. Do not write
`legacy/`, `contracts/`, `gen/`, or `infra/`. Do not write `modern/`
product code while `signed_off: false`.

---

## Context

Steel thread remainder: Type 01 landing must exist before dlt registers
(`docs/seams.md` seam 1 Emit, seam 2 consumes). Lakehouse Consensus
signed 2026-08-26. Ingest Consensus 2026-08-25 unchanged. Keep 173.44.
Parser already exists under `modern/ingestion/.../parser.py`. Do not
import Java.

---

## Behavior

- **B-1** — GIVEN `valid-minimal` WHEN emit succeeds THEN atomic Parquet
  and a readiness manifest exist under `modern/landing/` for batch
  `B202607230000001`. Destination is not SFTP `csv/outgoing`.
- **B-2** — GIVEN `df-source-001` / trailer **173.44** vs rows **173.45**
  WHEN emit runs THEN **zero** Parquet and no landing rows for
  `B202607230000004`. Finding stays `SOURCE_CONTROL_TOTAL_MISMATCH`.
- **B-3** — GIVEN landing money columns WHEN Parquet is published THEN
  values are Decimal scale 2, never float, and PAN/CPF are already
  tokenized/masked (parser owns privacy).
- **B-4** — GIVEN this leaf WHEN any file is written THEN the path is
  not under `legacy/`, `contracts/`, `gen/`, or `infra/`.

---

## Success Criteria

```bash
ROOT="$(git rev-parse --show-toplevel)"
SPEC="$ROOT/docs/tasks/T-20260826-type-01-landing-emit.md"
CONSENSUS="$ROOT/docs/consensus-lakehouse.md"
INGEST="$ROOT/docs/consensus.md"
LANDING="$ROOT/modern/landing"
WRITER="$ROOT/modern/ingestion/src/northwind_pay/types/01-card-settlement/writer.py"
HANDLER="$ROOT/modern/ingestion/src/northwind_pay/types/01-card-settlement/handler.py"

eval_1() {
  grep -q 'modern/landing/' "$SPEC" || return 1
  grep -q 'B202607230000001' "$SPEC" || return 1
  grep -q '173.45' "$SPEC" || return 1
  grep -q 'not SFTP' "$SPEC" || return 1
  grep -q 'Luan Moreno' "$CONSENSUS" || return 1
  grep -q 'canonical' "$CONSENSUS" || return 1
  grep -q 'canonical' "$INGEST" || return 1
  grep -q 'signed_off: false' "$SPEC" || return 1
}

eval_2() {
  grep -q '173.44' "$SPEC" || return 1
  grep -q 'zero Parquet' "$SPEC" || return 1
  grep -q 'B202607230000004' "$SPEC" || return 1
  grep -q 'SOURCE_CONTROL_TOTAL_MISMATCH' "$SPEC" || return 1
  awk '
    BEGIN { sec="" }
    /^---$/ { n++; next }
    n==1 && $0 ~ /^(touches_paths|creates_paths):/ { sec=$1; next }
    n==1 && sec != "" && $0 ~ /^[^[:space:]-]/ { sec="" }
    n==1 && sec != "" && $0 ~ /^[[:space:]]*-[[:space:]]*(legacy|contracts|gen|infra)\// { bad=1 }
    END { exit bad ? 1 : 0 }
  ' "$SPEC" || return 1
}

eval_3() {
  if [[ ! -f "$WRITER" || ! -f "$HANDLER" ]]; then
    grep -q 'signed_off: false' "$SPEC" || return 1
    return 0
  fi
  grep -qE 'modern/landing|landing' "$WRITER" "$HANDLER" || return 1
  ! grep -qE 'from[[:space:]]+legacy|import[[:space:]]+java|legacy\.processor' "$WRITER" "$HANDLER" || return 1
  ! grep -qE 'float\(|np\.float|dtype=float' "$WRITER" "$HANDLER" || return 1
  if [[ -d "$LANDING" ]]; then
    find "$LANDING" -name '*B202607230000004*' | grep -q . && return 1
    find "$LANDING" \( -name '*.parquet' -o -name '*B202607230000001*' \) | grep -q . || return 1
  fi
  return 0
}
```

---

## Validation Card

```yaml
success_criteria:
  - id: eval_1
    description: Leaf names landing Parquet for valid-minimal; lakehouse sign present; signed_off false
    runnable: bash
    check_type: deterministic
    verifies: [B-1]
    terminal: true
    expected_duration_sec: 5
  - id: eval_2
    description: Keep 173.44 zero Parquet; no frozen write paths
    runnable: bash
    check_type: deterministic
    verifies: [B-2, B-4]
    terminal: true
    expected_duration_sec: 5
  - id: eval_3
    description: Absent writer/handler allowed only while unsigned; present emit is Decimal, no Java, no lie Parquet
    runnable: bash
    check_type: deterministic
    verifies: [B-1, B-2, B-3, B-4]
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
eval_1 && eval_2 && eval_3
```

---

## Rollback Plan

(none — append-only spec. Later execution: revert `modern/ingestion/.../{model,schema,writer,handler}.py` and any `modern/landing/` files this leaf created. Never revert frozen trees.)

---

## Observability Hooks

(none until mesh. Watch landing parquet SHA-256; refuse `SOURCE_CONTROL_TOTAL_MISMATCH` with zero Parquet.)

---

## Anti-Patterns

- **Don't write Parquet to SFTP.** First modern write is `modern/landing/`.
- **Don't repair 173.44.** Keep the declaration. Zero Parquet.
- **Don't import Java.** Parser already owns privacy + Decimal.
- **Don't register dlt in this leaf.** That is the next leaf.
- **Don't write product code while `signed_off` is false.**
- **Don't hand-edit `signed_off*`.** Only `taskspec gate --stamp`.

---

## Do-Not-Touch

- `legacy/`
- `contracts/`
- `gen/`
- `infra/`
- `legacy/processor/src`
- `validation/golden-match/golden_match.py`

---

## Open Questions

(none — Python packaging remains parked in ADR 0006 rows 1–2 and must not be smuggled in.)
