# Agenda — five-day scope

These briefs are the week map. They are **scope**, not hour-by-hour
run-of-show. The night you execute lives in [`run/`](../run/README.md)
(staff + the two designers). Do not invent extra story when the slides
are built.

The public bootcamp page is the autonomy curve. This folder is how that
curve lands on **this** repo.

| Day | Seat | File | Rings | Converge | Gate |
|---|---|---|---|---|---|
| 1 | Archaeologist (SA + AI) | [`d1.md`](d1.md) | Prompt + context | **0–1** Capture → Intent | The system starts to understand the legacy (Second Brain + OntoLayer + tech-spec) |
| 2 | Translator (SWE) | [`d2.md`](d2.md) | Harness | **2–4** then **5–8** on ingest → landing | Type `01` translates safely, isolated. Consensus is the barrier before the first write |
| 3 | Constructor (DE + analytics) | [`d3.md`](d3.md) | Harness + loop seed | 5–8 on dlt → Gold | Pipeline builds Bronze → Gold with you validating |
| 4 | Orchestrator | [`d4.md`](d4.md) | Loop + eval | 7–8. Type `05` unattended | Loop runs; small `HALF_UP` pill |
| 5 | Dark Factory | [`d5.md`](d5.md) | Orchestration | Full 0–8 on sealed Type `06` | Never-seen type onboarded live. Large pill: `CONFIRMED_LEGACY_DEFECT` |

**The week starts at Day 1.** You arrive as an AI-native engineer from scratch.
You do not inherit a brain, a graph, or last run's ADRs.

| Night | What closes |
|---|---|
| 1 | Plant **MATCHED**. Second Brain fed (whole drop, types `01`–`05`). OntoLayer via MCP. Capture + Intent. Research queries for Day 2. **No product code.** |
| 2 | ADRs, seams, **Consensus signed**, then Type `01` landing Parquet |
| 3 | dlt → Gold. Golden-match attached |
| 4 | Unattended Type `05`. Bind + Loop |
| 5 | Sealed Type `06`. Full spine. Classify, do not patch |

Every day uses the same swing: **Stage → Craft → Floor → Debrief**.
Day 1 also has **Dig** (read, brain, graph, spine) between Floor and Debrief.

Every day closes with three parts: **role skills** (the seat), **deliverables**
(what you hold), and **Research** (what you query for tomorrow). See each
`dN.md` → `## Research`.

The inbound drop is [`spec/`](../spec/README.md). The engagement map is
[`plans/`](../plans/README.md). The operator surface is the root
[`README.md`](../README.md). Type `06` is **not** in `spec/` until Friday
morning.

The human Second Brain for the week is
[`brain/notebooklm/`](../brain/notebooklm/README.md) — nine packs, types
`01`–`05`. Days 2–4 **query that notebook**. They do not rebuild it. Type
`06` is a new source on Friday, not in the zip.

Public page lists Day 1 Converge as *P1 Intent · P2 Structure*. This week
**keeps Capture + Intent on Day 1** so follow-along can finish Second Brain
and OntoLayer. **Structure (ADRs) is the first act of Day 2**, then Decompose
and Consensus, then the first modern write. The page gate still holds: by
Tuesday night the legacy is specified, structured, and translated.

## Decks

| Day | Deck |
|---|---|
| 1 | [`presentation/d1-archaeologist.html`](../presentation/d1-archaeologist.html) — live. 44 slides. Staff: [`run/d1/`](../run/d1/README.md) |
| 2 | [`presentation/d2-translator.html`](../presentation/d2-translator.html) — file exists; not signed off as follow-along yet |
| 3–5 | not built yet. Build from this folder. |

## What is frozen vs what the week writes

| Already on the tree | Written during the week |
|---|---|
| Legacy plant, five contracts, DataGen, oracles | Second Brain (Day 1, queried all week) + OntoLayer, Converge artifacts, `modern/` for Types `01`–`05` |
| Inbound packs `01`–`05` under `spec/` | ADRs, seams, Task-Specs (Day 2+) |
| `validation/golden-match/golden_match.py` | Modern observations attached to that referee |
| This folder (scope) | Hour-by-hour in [`run/`](../run/README.md); Day 1 PPT is closed |

Do not pre-seed Converge. Do not copy last run's ADRs out of git history.
Do not repair a source declaration. Do not edit frozen `legacy/` to go green.
