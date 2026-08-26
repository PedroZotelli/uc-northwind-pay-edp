# Docs — Converge paper trail

This folder is where Converge **writes**. It is not inbound
([`spec/`](../spec/README.md)), not the judge ([`contracts/`](../contracts/README.md)),
and not the method manuals ([`presentation/`](../presentation/README.md)).

This repo’s Converge home for the **room** is **`docs/`**, not `cvg/docs/`.
If `cvg` emits under `cvg/docs/` or `cvg/swimlanes/`, copy the artifact
into the path below. `cvg init` (Thursday, or host) creates `cvg/` for
the referee — it does **not** replace this folder. Do not copy another
project’s lane names (`assurance` / `foundation` / `models`). This plant’s
seams are **ingest → landing**, **dlt → Gold**, **orchestrate + serve**.

Do not upload these files into NotebookLM. The brain is inbound only
([`brain/notebooklm/`](../brain/notebooklm/README.md)).

---

## Story of the week (what papers close)

| Night | Seat | What this folder holds | Product (not this folder) |
|---|---|---|---|
| **1** | Archaeologist | BRD + tech-spec (Pass 0–1) | none |
| **2** | Translator (SWE) | Landing ADRs 0001–0005, **0006 parked**, `seams.md`, ingest **sign**, one parser leaf | parser may exist under `modern/ingestion/`; Parquet **not** required Tuesday |
| **3** | Constructor (DE + analytics) | Unpark 0006 → ADRs 0007+; seam 2 legs; **`consensus-lakehouse.md`**; Type 01 lakehouse leaves | Type 01 **landing → Gold + golden-match**. Mesh **seed**. Types `02`–`05` **not** tasked |
| **4** | Orchestrator | Remaining SWE + DE leaves (`02`–`04`, Type `05`, orchestrate) | Loop cranks the queue. Linear is the board. Type `05` unattended |
| **5** | Dark Factory | Type `06` papers when that drop arrives | Classify. Do not patch `legacy/` |

**Two nights, two seats, one type** (Tue–Wed). Thursday **generates** the
rest and cranks it. Do not dump Types `02`–`05` on Wednesday.

Clocks: [`run/d2/`](../run/d2/README.md) · [`run/d3/`](../run/d3/README.md).
Scope: [`agenda/d3.md`](../agenda/d3.md) · [`agenda/d4.md`](../agenda/d4.md).

---

## On disk now (Day 3 Constructor worktree)

```text
docs/
  README.md                              this map
  brd-type-01-card-settlement.md         Pass 0 Capture     Day 1 · exists
  tech-spec-type-01-card-settlement.md    Pass 1 Intent      Day 1 · exists
  CONTEXT.md                             glossary           Day 2 + lakehouse terms
  adrs/0001-first-write-is-landing-parquet.md
  adrs/0002-type-01-five-file-package.md
  adrs/0003-decimal-never-float.md
  adrs/0004-privacy-dies-at-the-parser.md
  adrs/0005-source-lie-kept-zero-parquet.md
  adrs/0006-later-nights-parked.md        park **record** (rows 3–7 unparked as 0007–0011; 8–9 Day 4)
  adrs/0007-dlt-registers-landing-only.md
  adrs/0008-ducklake-duckdb-is-local.md
  adrs/0009-medallion-grains-and-keys.md
  adrs/0010-rule-split-parser-vs-dbt.md
  adrs/0011-golden-match-keys-two-questions.md
  seams.md                               seam 2 legs: register → medallion → match
  consensus.md                           ingest → landing **signed** 2026-08-25 (do not recut)
  consensus-lakehouse.md                 dlt → Gold **signed** 2026-08-26
  tasks/T-20260825-type-01-landing-parser.md
  tasks/T-20260826-type-01-*.md           emit, dlt, bronze, silver, gold, golden-match
```

Keep **173.44**. Ingest sign stays canonical. Types `02`–`05` not tasked.

---

## Pass → file

| Pass | Name | File | Night |
|---|---|---|---|
| 0 | Capture | [`brd-type-01-card-settlement.md`](brd-type-01-card-settlement.md) | Day 1 wrote it. Later nights **look** ([`run/d2/02-prompt-papers.md`](../run/d2/02-prompt-papers.md), [`run/d3/01-prompt-recap.md`](../run/d3/01-prompt-recap.md)) |
| 1 | Intent | [`tech-spec-type-01-card-settlement.md`](tech-spec-type-01-card-settlement.md) | Same |
| 2 | Structure | `adrs/` + `CONTEXT.md` | Day 2 landing 0001–0005 + park 0006 ([`run/d2/08-structure.md`](../run/d2/08-structure.md)). Day 3 unparks rows 3–7 as 0007+ ([`run/d3/06-structure.md`](../run/d3/06-structure.md)). Do not recut 0001–0005 |
| 3 | Decompose | [`seams.md`](seams.md) | Day 2 named three seams; tasked seam 1 ([`run/d2/09-decompose.md`](../run/d2/09-decompose.md)). Day 3 writes **seam 2 legs** (register → medallion → match) ([`run/d3/07-decompose.md`](../run/d3/07-decompose.md)). Day 4 cuts remaining type lanes + orchestrate |
| 4 | Consensus | [`consensus.md`](consensus.md) · `consensus-lakehouse.md` | Day 2 ingest sign ([`run/d2/10-consensus.md`](../run/d2/10-consensus.md)). Day 3 lakehouse sign ([`run/d3/08-consensus.md`](../run/d3/08-consensus.md)). No lakehouse sign → **skip Gold** (`run/d3` 09–12 dark) |
| 5 | Tasking | `tasks/` | Day 2: one parser leaf ([`run/d2/11-taskspec.md`](../run/d2/11-taskspec.md)). Day 3: Type 01 remainder + lakehouse leaves ([`run/d3/09-taskspec.md`](../run/d3/09-taskspec.md)). Day 4: remaining SWE + DE (`02`–`04`, Type `05`, orchestrate) |
| 6 | Register | opt-in / `cvg/` | Day 3 Mesh is **seed** (local Gold). Factory Register is Day 4 |
| 7 | Bind | harness, not a doc | Shown Day 2 fail-closed; **still on** Day 3 ([`run/d3/README.md`](../run/d3/README.md)) |
| 8 | Loop | product, not this folder | Type 01 Gold is Day 3 product ([`run/d3/10-landing.md`](../run/d3/10-landing.md)–[`12-golden-match.md`](../run/d3/12-golden-match.md)). Factory 6–8 + Linear = Day 4 |

`cvg` may error (Task-Spec 3.9 vs Converge 3.8). The **agent still writes
here**. Do not debug the CLI in front of the room. A dated signature in
`consensus.md` / `consensus-lakehouse.md` still counts.

---

## ADR index (Day 2)

| ADR | Status | Closes |
|---|---|---|
| [`0001-first-write-is-landing-parquet.md`](adrs/0001-first-write-is-landing-parquet.md) | Closed | First write is `modern/landing/` Parquet, not SFTP |
| [`0002-type-01-five-file-package.md`](adrs/0002-type-01-five-file-package.md) | Closed | `model → parser → schema → writer → handler` |
| [`0003-decimal-never-float.md`](adrs/0003-decimal-never-float.md) | Closed | Exact Decimal |
| [`0004-privacy-dies-at-the-parser.md`](adrs/0004-privacy-dies-at-the-parser.md) | Closed | PAN token + last4, CPF mask — before Gold |
| [`0005-source-lie-kept-zero-parquet.md`](adrs/0005-source-lie-kept-zero-parquet.md) | Closed | Keep **173.44**. Refuse. Zero Parquet |
| [`0006-later-nights-parked.md`](adrs/0006-later-nights-parked.md) | **Parked** (record) | Rows **3–7** unparked as 0007–0011. Rows **8–9** Day 4 (Dagster, serve). Row 10 CI = no |
| [`0007-dlt-registers-landing-only.md`](adrs/0007-dlt-registers-landing-only.md) | Closed (lakehouse sign) | dlt registers landing. No re-parse, money, or privacy |
| [`0008-ducklake-duckdb-is-local.md`](adrs/0008-ducklake-duckdb-is-local.md) | Closed (lakehouse sign) | Local DuckLake / DuckDB. Not a warehouse copy |
| [`0009-medallion-grains-and-keys.md`](adrs/0009-medallion-grains-and-keys.md) | Closed (lakehouse sign) | Bronze / Silver grain `batch_id`+`source_record_number`; Gold `batch_id`+`currency` |
| [`0010-rule-split-parser-vs-dbt.md`](adrs/0010-rule-split-parser-vs-dbt.md) | Closed (lakehouse sign) | Parser owns privacy + Decimal; dbt asserts, does not retokenize |
| [`0011-golden-match-keys-two-questions.md`](adrs/0011-golden-match-keys-two-questions.md) | Closed (lakehouse sign) | Paid keys; two questions; six codes; do not rewrite the referee |

0006 stays as the park record. Day 3 added **new** ADRs; it did not rewrite 0001–0005.

---

## Method manuals (not this folder)

| Manual | What it is |
|---|---|
| [`presentation/cvg-aut-systems-spine-steps.html`](../presentation/cvg-aut-systems-spine-steps.html) | Converge spine — nine passes, one human barrier |
| [`presentation/asd-agentic-loop.html`](../presentation/asd-agentic-loop.html) | ASD — the Agentic Loop |
| [`presentation/boot-uc-northwind-pay-edp-oss.html`](../presentation/boot-uc-northwind-pay-edp-oss.html) | Bootcamp reference |
| [`presentation/seamwise.html`](../presentation/seamwise.html) | SeamWise kit — Leave · SeamWise on Nights 2 and 3, return to the numbered beat |
| [`presentation/d3-constructor.html`](../presentation/d3-constructor.html) | Night 3 HUD — not a paper |

Plans steer the plant: [`plans/`](../plans/README.md). This folder is
the week’s **signed papers**.

---

## What this folder is not

- Not contracts, fixtures, or expected outputs.
- Not a second copy of [`plans/legacy.md`](../plans/legacy.md) or [`plans/modern.md`](../plans/modern.md).
- Not the HTML manuals or Night decks.
- Not `modern/`. Landing Parquet and Gold are **product** after the relevant sign.
- Not `cvg/swimlanes/`. That tree is the referee workspace (Day 4 host: `cvg init`), projected from [`seams.md`](seams.md).
- Not the Second Brain. Do not paste BRD, ADRs, or Consensus into NotebookLM.

Do not pre-seed Day 3 lakehouse papers. Do not copy last run’s ADRs out of
git history. Do not repair **173.44**.
