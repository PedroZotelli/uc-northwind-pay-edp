# 04 · Pass 5 — generate remaining SWE + DE

- Slide: Execute 03–05 (Hands-On **slice b · generate**) — tile 04 after Task-Spec Show + [`../../presentation/task-spec.html`](../../presentation/task-spec.html)
- Slice: **B · Generate**
- Who: instructor authors the first remaining leaf in public, then every seat
- Next: [`05-register-linear.md`](05-register-linear.md) on the **same board**

Task-Spec kit already ran. Mesh is **not** inside this kit. One leaf, one eval. `signed_off` starts **false**. Empty type packages forbidden.

## Prompt (verbatim)

```text
You are Pass 5 Tasking on NorthWind Pay. Orchestrator seat.
Author remaining SWE + DE leaves under docs/tasks/.
One leaf, one eval. signed_off starts false.

Required (skip a leaf if that artifact already exists and matches the ADR):
- Types 02, 03, 04: ingest (five-file / landing) and lakehouse (dlt → B/S/G → golden-match) as separate leaves
- Type 05: ingest + lakehouse leaves. Evals must cover DF-SOURCE-005 (CONFIRMED_SOURCE_DEFECT) and rounding-half-up (HALF_UP; HALF_EVEN is MODERN_DEFECT)
- Orchestrate: Dagster lineage on closed Type 01 — parsing does not move into the orchestrator

Each leaf must forbid writes to legacy/, contracts/, gen/, infra/.
Each eval is a runnable command, not “the agent said it worked.”
Do not author Type 06.
Do not create empty type folders.
```

```bash
mkdir -p docs/tasks
cvg tasking --draft --json
```

If `cvg` wrote under `cvg/docs/`, move the leaves into `docs/tasks/`. If `cvg` errors, the agent still writes the leaves.

## Proof

Leaves exist for remaining SWE+DE with evals. No empty Type `05` package. `signed_off` is false. Type `06` absent.

## If fail

No eval → tear it up. Empty type-02 folder → delete it. Do not crank unsigned leaves. Do not Loop factory from chat.
