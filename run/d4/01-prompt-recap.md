# 01 · Prompt — Recap Gold

- Slide: Recap · Gold, Recap · papers (talk; **no** Hands-On badge)
- Slice: **Recap**
- Who: every seat, through **their** agent
- Next: Stage talks, Craft Shows, Floor Context Layer Show, then [`02-query-context.md`](02-query-context.md) on Execute 02

Do not recut Tuesday’s ingest sign or Wednesday’s lakehouse sign. Map: [`docs/README.md`](../../docs/README.md). Contract: [`plans/modern.md`](../../plans/modern.md).

## Prompt (verbatim)

```text
Do not change any file.
Read docs/README.md, docs/consensus.md, docs/seams.md, and docs/adrs/0006-later-nights-parked.md.
List docs/adrs/, docs/tasks/, and modern/ (terminal, not Git).
If docs/consensus-lakehouse.md exists, read it.

From the files, not from memory:
1. Who signed ingest → landing? Must we keep 173.44?
2. Does a lakehouse sign exist? What did ADR 0006 park for tonight (rows 8–9)?
3. Is Type 01 Gold on disk (landing Parquet, lakehouse, golden-match packet)? If missing, say so.
4. How many Task-Specs exist? Any for Types 02–05?
5. Which seam is tonight (orchestrate + remaining types)? Which signs must we not recut?

Do not make run unless evidence/B202607230000001/reconciliation.json is missing.
Do not write any file.
Do not generate Types 02–05 yet.
```

## Proof

1. **Luan Moreno, Agentic Lead** · **173.44** kept.
2. Lakehouse sign **or named gap**. **0006 rows 8–9** = Dagster / serve = tonight.
3. Gold **present or named as a gap**. `main` may have none — that is allowed.
4. Parser leaf exists. Types `02`–`05` **not** tasked yet.
5. Seam **3** + remaining type lanes tonight. Do not recut ingest or lakehouse Consensus.

## If fail

Gold missing → **do not run 03–09**. Name the gap; Stage still runs. Missing MATCHED packet → [`../d1/05-boot.md`](../d1/05-boot.md). Do not share Compose port **2222**.
