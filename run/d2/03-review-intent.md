# 03 · Review Pass 1 — the tech-spec

- Slide: Board 1 · Recap — look, do not pick a lakehouse
- Slice: **A · Yesterday**
- Who: every seat, through **their** agent
- Next: [`04-first-write.md`](04-first-write.md)

Intent already answered the brief. Tonight we **restate** it. An unsigned tech-spec is not a license to code — that is why we Bind and sign later tonight.

## Prompt (verbatim)

```text
Read docs/README.md then docs/tech-spec-type-01-card-settlement.md.
Do not change any file.

Restate, from the file:
1. The brief, restated — one page.
2. Requirements — keep the lie, refuse a mismatch, Type 01 steel thread.
3. Truth roles — inbound spec/, judge contracts/, frozen plant, observation evidence/.
4. What the second plant must not do — first write is not SFTP; do not import Java.
5. Open questions — which ones are still open for ADRs tonight?

It must not have picked DuckDB, dbt, a lakehouse, or any stack as a decision.
If it did, name that as a smell. Do not start Pass 2 to paper over it.
```

## Proof

The room can restate the spec with the file closed. First write is later (tonight). No Java import. No SFTP as modern input. Open questions are owned, not silently defaulted.

## If fail

Missing file → stop and reopen Day 1 Intent. Do not invent the brief in the parser.
