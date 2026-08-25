# 10 · Pass 3 — Decompose (Seamwise)

- Slide: Board 4 · Barrier — Pass 3 seams into `docs/seams.md`
- Slice: **F · Barrier**
- Who: instructor cuts in public, room copies
- Next: [`11-consensus.md`](11-consensus.md)

Seamwise attaches here. One lane tonight. Do not invent a fourth estate. Do not start Task-Specs.

## Do

Name the three seams. Own each arrow. Steel thread = Type `01`.

| Seam | Owner | Built |
|---|---|---|
| Ingest → landing | Translator · **tonight** | raw SFTP → five-file → `modern/landing/` |
| dlt → Gold | Constructor · Day 3 | register-only dlt → DuckLake → dbt |
| Orchestrate + serve | Orchestrator · Day 4 | Dagster, read-only Gold |

Event-driven tonight = this ingest seam (sense, claim, emit). Not a broker.

## Prompt (verbatim)

```text
You are Pass 3 Decompose on NorthWind Pay.
Cut seams for the week. Steel thread is Type 01 ingest → landing.
Write the seam list to docs/seams.md (see docs/README.md).
Name: seam, swimlane, leg. One owner per handoff.
Do not write Task-Specs.
Do not write product code.
Do not change frozen folders.
```

## Proof

`docs/seams.md` exists. Three seams on the board. Type `01` is the only lane that will be tasked tonight. Days 3–4 are named, not built.

## If fail

They cut “Java vs Python” as a seam → stop. The seam is the **handoff**, not the language.
