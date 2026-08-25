# 09 · Pass 2 — Structure (ADRs)

- Slide: Board 4 · Barrier — Pass 2 ADRs into `docs/adrs/`
- Slice: **F · Barrier**
- Who: instructor drafts the first ADR in public, then every seat
- Next: [`10-decompose.md`](10-decompose.md)

What is true, never how. Facts from the Second Brain, OntoLayer, and the Day 1 tech-spec. The graph is evidence. It is not the ADR.

Close the ten questions in `plans/modern.md` or **park** each with an owner. A question without a sentence is not closed.

## Prompt (verbatim)

```text
You are Pass 2 Structure on NorthWind Pay. Human-led. No product code.

Read docs/README.md and docs/tech-spec-type-01-card-settlement.md.
You may query the Second Brain and OntoLayer for facts.
Write ADRs under docs/adrs/ as NNNN-short-name.md.
Write domain terms to docs/CONTEXT.md.
This repo’s Converge home is docs/, not cvg/docs/.
Draft ADRs that answer, as facts + constraints, not build steps:

Example shape: “dlt registers landing; it does not re-parse.”
(That ADR is for Day 3 — write tonight’s landing facts, not the lakehouse.)

Tonight’s landing ADRs must cover:
- First write is modern/landing/ Parquet, not SFTP
- Type 01 five-file package is the unit
- Decimal, never float
- Privacy dies at the parser
- Source lie keeps 173.44; refuse; zero Parquet

Do not pick a lakehouse.
Do not write modern/ code.
Do not import Java.
```

Then gate if `cvg` sits:

```bash
mkdir -p docs/adrs
cvg structure --draft --json
```

If `cvg` wrote under `cvg/docs/`, move the ADRs and `CONTEXT.md` into `docs/`.

## Proof

Files exist under [`docs/adrs/`](../../docs/README.md) and `docs/CONTEXT.md`. The room can restate them with the files closed. No “how we implement the parser” in an ADR.

## If fail

A stack choice dressed as an ADR → tear it out. Park it. Do not proceed to Decompose on mush.
