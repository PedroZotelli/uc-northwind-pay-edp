# 08 · Attach Seamwise + Task-Spec

- Slide: Board 4 · Kits — Seamwise + Task-Spec, named not coded
- Slice: **E · Kits**
- Who: every seat, through **their** agent
- Next: [`09-structure.md`](09-structure.md)

Converge is already on the path from Day 1. Tonight the other two kits **attach**. They still do not write product code.

## Prompt (verbatim)

```text
Read README.md and docs/README.md. You may read presentation/cvg-aut-systems-spine-steps.html.

Answer from the repo:
1. What is Seamwise? At which Converge pass does it attach tonight?
2. What is the one lane we cut tonight (ingest → landing)? What waits until Day 3?
3. What is Task-Spec? At which pass does it attach?
4. What does “no eval, no build” mean?
5. What is Bind vs the Agent Harness?
6. Where do Converge papers live tonight (docs/ tree — BRD, tech-spec, adrs/, seams, consensus, tasks/)?

Do not change any file.
Do not start Pass 2 yet.
Do not ask OntoLayer these questions.
```

## Proof

| Ask | A healthy answer |
|---|---|
| Seamwise | Lanes. Attaches at **Decompose (Pass 3)**. Tonight: ingest → landing |
| Not tonight | dlt → Gold (Day 3). Dagster (Day 4) |
| Task-Spec | Leaves. Attaches at **Tasking (Pass 5)**. One leaf, one eval |
| Bind | Rails **on** the Agent Harness. Enforcement stays in the harness |
| Papers | [`docs/`](../../docs/README.md) — BRD, tech-spec, `adrs/`, `seams.md`, `consensus.md`, `tasks/` |

## If fail

They say “Task-Spec is Pass 2” → correct from the table. They point at `docs/cvg-aut-systems-spine-steps.html` → that manual is in `presentation/`. Papers are [`docs/README.md`](../../docs/README.md). Do not install a second Converge.
