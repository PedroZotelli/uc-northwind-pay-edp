# Agenda — five-day scope

These briefs are the week map. They are **scope**, not hour-by-hour
run-of-show. Refine after Day 1 is closed (PPT + follow-along at 100%).
Do not invent extra story when the slides are built.

| Day | Seat | File | Converge |
|---|---|---|---|
| 1 | Onboard + Archaeologist | [`d1.md`](d1.md) | Show the spine, then Pass 0–4. **No product code.** Consensus is the barrier. |
| 2 | Translator (SWE) | [`d2.md`](d2.md) | Pass 5–8 on ingest → landing |
| 3 | Constructor (DE + analytics) | [`d3.md`](d3.md) | Pass 5–8 on dlt → Gold |
| 4 | Orchestrator | [`d4.md`](d4.md) | Pass 7–8. Type `05` unattended. Small `HALF_UP` pill. |
| 5 | Dark Factory | [`d5.md`](d5.md) | Full 0–8 on sealed Type `06`. Large pill: `CONFIRMED_LEGACY_DEFECT`. |

**The week starts at Day 1.** Onboard and Archaeologist used to be two days; they are
one. Day 1 carries two seats in sequence:

| Half | Seat | Persona | What it closes |
|---|---|---|---|
| First | Setup | *the Operator* | the plant runs on your machine — Type `01` **MATCHED**, net `173.45` |
| Second | Solutions Architect & AI Engineer | *the Archaeologist* | `spec/` unpacked, ADRs written, seams cut, **Consensus signed** |

Every day uses the same swing: **Stage → Craft → Floor → Debrief**.

The inbound drop is [`spec/`](../spec/README.md). The engagement map is
[`plans/`](../plans/README.md). The operator surface is the root
[`README.md`](../README.md). Type `06` is **not** in `spec/` until Friday
morning.

## Decks

| Day | Deck |
|---|---|
| 1 | [`presentation/d1-archaeologist.html`](../presentation/d1-archaeologist.html) — 37 slides, four blocks |
| 2–5 | not built yet |

## What is frozen vs what the week writes

| Already on the tree | Written during the week |
|---|---|
| Legacy plant, five contracts, DataGen, oracles | `modern/` for Types `01`–`05` |
| Inbound packs `01`–`05` under `spec/` | Converge artifacts (ADRs, seams, Task-Specs) |
| `validation/golden-match/golden_match.py` | Modern observations attached to that referee |
| This folder (scope) | Hour-by-hour and PPTs, after Day 1 is closed |

Do not pre-seed Converge. Do not copy last run's ADRs out of git history.
Do not repair a source declaration. Do not edit frozen `legacy/` to go green.
