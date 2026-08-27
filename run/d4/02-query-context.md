# 02 · Query the Context Layer

- Slide: Execute 02 (Hands-On **slice a · query** · chip `run/d4/` · **02**)
- Slice: **A · Query**
- Who: every seat, through **their** agent + MCP
- Next: Dig Leave · SeamWise, then [`03-remaining-seams.md`](03-remaining-seams.md) on Execute 03–05

Show first: Context Layer. Same nine-pack brain. OntoLayer is observation. `docs/` is papers. `plans/modern.md` is the engagement contract. `contracts/` is the judge.

## Prompt (verbatim)

```text
You are querying the Context Layer for the Orchestrator seat. Do not change any file.

1. Read docs/README.md and docs/CONTEXT.md.
   Where does “paid” live for Type 01? Name the reporting table, the grain, and which procedure writes it.
   Use northwind-ontology MCP catalog_ask, or say to run make ontology-ask.
   Do not grep SQL as the judge.

2. Read plans/modern.md (Milestones 4 and 5, golden-match).
   What is an eval allowed to mean on this plant?
   What must Dagster not do?

3. Name the four rooms of the Context Layer (brain / catalog / papers / judge).
   Where do observations live (evidence/)?

Do not write product code.
Do not invent a grain.
Do not add a tenth NotebookLM source.
```

Staff, if MCP is down:

```bash
make ontology-ask-sql
make ontology-ask
```

## Proof

| Ask | A healthy answer |
|---|---|
| Paid | `reporting.card_settlement_reconciliation` · grain `batch_id + currency` · `reporting.refresh_card_settlement_reconciliation` |
| Eval | Runnable judge. Golden-match: two questions, six codes, no tolerance. “dbt ran” is a log |
| Dagster | Lineage, retries, evidence — **not** the parser |
| Four rooms | Brain (`spec/` / NotebookLM) · OntoLayer · `docs/` · `contracts/`. Observations: `evidence/` |

Without ontology: 0 SQL hits for “paid”. That contrast still holds.

## If fail

Graph down → `make deploy && make ontology` **on this checkout only**. Do not guess joins. Do not treat `plans/modern.md` as an ADR. Do not start generate on mush.
