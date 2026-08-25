# Day 2 — follow-along

Staff execute folder. Scope: [`agenda/d2.md`](../../agenda/d2.md). Deck: [`presentation/d2-translator.html`](../../presentation/d2-translator.html) — file exists; **not** signed off as follow-along yet. Drive from this folder until the HUD is rebuilt. Beat `Slide:` lines are the **six boards** below, not Execute numbers on that HTML.

**One Night.** No morning / afternoon. Stage is keyboards down. Show, then the Hands-On board, send the room into the numbered beats, **look up** at the proof. Do not flip a slide per prompt. Do not skip a Show.

House stack (unchanged): Oh My Pi → OpenRouter → a workspace (CMUX, ORCA, Super Engineering, or BYO) → DeepSeek. We grade gates, not the vendor.

**Story:** Yesterday we understood (0–1). Tonight we restated that brief, grasped the Java *plant as concepts*, bound the Agent Harness, signed Consensus, then wrote Type `01` landing. Lakehouse waits.

- [ ] **End-to-End**
  1. *First Write & Independence*
  2. *Bind the Agent Harness*
  3. *Query Second Brain*
  4. *Query OntoLayer & the Specs*
  5. *Attach Seamwise & Task-Spec*
  6. *Converge Pass 2–8 on ingest → landing*

| Slice | Beats | Public beat | Look up when |
|---|---|---|---|
| **A · Yesterday** | [`01`](01-matched.md)–[`03`](03-review-intent.md) | Recap Day 1 · review Pass 0–1 | MATCHED still; BRD + tech-spec restated |
| **B · Picture** | [`04`](04-first-write.md) | 1 · First write | Two plants drawn; first write = Parquet |
| **C · Grasp** | [`05`](05-brain-java.md)–[`06`](06-specs-graph.md) | 3 + 4 · Brain & specs | Java concepts cited; what we build / do not |
| **D · Fence** | [`07`](07-bind-harness.md) | 2 · Bind the Agent Harness | Touch `legacy/processor/` → **fail closed** |
| **E · Kits** | [`08`](08-kits.md) | 5 · Seamwise + Task-Spec | Lanes at 3, leaves at 5, named |
| **F · Barrier** | [`09`](09-structure.md)–[`11`](11-consensus.md) | 6a · Pass 2–4 | Owner **signs**. No sign → skip G |
| **G · Landing** | [`12`](12-tasking.md)–[`15`](15-malformed.md) | 6b · Pass 5–8 | Parquet on valid; **zero** Parquet on refuse |
| **Close** | [`16`](16-research.md) | Research | Grain, first write, golden-match two questions |

If `11` ends unsigned, **do not run 12–15**. Bind (`07`) is on **before** any `modern/` write. Do not port Java. Do not rebuild the Second Brain — **nine packs, no tenth source**. Type `06` is not in the notebook. Specs and OntoLayer are the repo / MCP, not a new upload.

## How to run this Night (same mold as Day 1)

Day 1 used **six Hands-On boards**, not one slide per prompt. Do the same. The eight slice names below are the *story*. The six boards are what you put on the projector.

| Board | Beats | Show first | Hands-On | Clock |
|---|---|---|---|---|
| 1 · Recap | 01–03 | Yesterday’s receipts + Pass 0–1 | Restate BRD + tech-spec | Tight. This is look, not the Night |
| 2 · Picture + grasp | 04–06 | First write; Java as concepts | Brain J1–J5; specs + `ontology-ask` | Grasp, then move |
| 3 · Fence | 07 | Agent Harness vs Bind | Touch `legacy/processor/` | **Stop the Night if it writes** |
| 4 · Kits + barrier | 08–11 | Seamwise / Task-Spec / spine 2–4 | ADRs, seams, **owner signs** | No sign → skip board 5 |
| 5 · Landing | 12–15 | One leaf, one eval | Loop + two refuses | **This is the SWE proof** |
| 6 · Research | 16 | — | Three queries | Then walk |

Public checklist order is **capabilities**, not the clock. Clock is the table above: recap → picture → Bind → sign → build → Research.

**SWE “did it right” is only board 5**, after the sign:

| Smoke | Right | Wrong |
|---|---|---|
| `valid-minimal` | Parquet + readiness; replay identical | A CSV on SFTP; a Java import |
| `DF-SOURCE-001` | 173.44 kept, 173.45 computed, **zero** Parquet | Trailer patched; Parquet on the lie |
| malformed | Stable code, quarantine, no publication | A crash as the only result |
| Bind still on | Frozen folders untouched | `legacy/` edited “to go green” |

Pass 6 Register is opt-in — not a board. Pass 7 Bind was already proven on board 3; keep it on during the Loop.

Time: if recap + grasp eat the Night, you did not translate. Cut talk, keep 07, 11, 12–15.

Converge papers live in [`docs/`](../../docs/README.md) — **this repo’s home, not `cvg/docs/`**. Day 1 already wrote Capture + Intent. Tonight Structure → Consensus → Tasking write the rest **there**. Landing writes `modern/landing/`. `evidence/` is gitignored — open it in the **terminal**.

```text
docs/
  brd-type-01-card-settlement.md         Pass 0  look (02)
  tech-spec-type-01-card-settlement.md    Pass 1  look (03)
  CONTEXT.md + adrs/NNNN-*.md            Pass 2  write (09)
  seams.md                               Pass 3  write (10)
  consensus.md                           Pass 4  sign (11)  — no sign, skip G
  tasks/                                 Pass 5  write (12)
modern/landing/                          Pass 8  smoke (13–15)
```

## Dry-run E2E (after you sign this folder)

A **new git worktree** is the right isolation. Do not prove the Night in the teaching checkout — `modern/` and Night 2 ADRs from a dry-run must not pollute the clock.

Sign **this folder**, not the Translator HTML. Then:

1. **Commit the clock** on `main` (or a signed branch). `run/d2/` is untracked until you do. A worktree from `origin/main` @ `fa62afd` does **not** have these 16 beats, `docs/README.md`, or the Day 1 BRD/tech-spec.
2. **Do not commit** dry-run `modern/`, `docs/adrs/`, `docs/consensus.md`, or `docs/tasks/` unless you mean that product to ship. The worktree is disposable.
3. **Worktree from that commit**, not from dirty `main`:

```bash
git worktree add ../nw-d2-e2e <signed-commit>
cd ../nw-d2-e2e
cp .env.example .env   # bump SFTP_PORT / POSTGRES ports if the teaching stack is still up
# or: stop the teaching stack first — compose name is northwind-pay-legacy, port 2222
make init && make deploy
make run TYPE=01 SCENARIO=valid-minimal
# then walk run/d2/01 → 16 in order
```

4. **Reuse the Day 1 notebook.** Do not rebuild it. Specs + graph are the repo / MCP. Bind still needs a real harness (fail closed on `legacy/processor/`).
5. **SWE proof is only 13–15**, after the sign. Those smokes are the **modern** handler against `spec/type-01-card-settlement/samples/{valid-minimal,df-source-001,malformed}.dat`. They are **not** `make run` (Java).

Walk 01–16. If recap + grasp eat the Night, you did not translate. Cut talk, keep 07, 11, 12–15.

## Beats (one file each)

| # | File | Slice | What they do |
|---|---|---|---|
| 01 | [`01-matched.md`](01-matched.md) | A | `make status` · Type `01` still MATCHED |
| 02 | [`02-review-capture.md`](02-review-capture.md) | A | Restate Pass 0 BRD · six headings |
| 03 | [`03-review-intent.md`](03-review-intent.md) | A | Restate Pass 1 tech-spec · no stack |
| 04 | [`04-first-write.md`](04-first-write.md) | B | Draw independence · first write = Parquet |
| 05 | [`05-brain-java.md`](05-brain-java.md) | C | Query the brain · Java **concepts**, cite a page |
| 06 | [`06-specs-graph.md`](06-specs-graph.md) | C | Specs + OntoLayer · what we build / how |
| 07 | [`07-bind-harness.md`](07-bind-harness.md) | D | Bind the Agent Harness · fail closed |
| 08 | [`08-kits.md`](08-kits.md) | E | Seamwise at 3 · Task-Spec at 5 |
| 09 | [`09-structure.md`](09-structure.md) | F | Pass 2 · ADRs · what is true, never how |
| 10 | [`10-decompose.md`](10-decompose.md) | F | Pass 3 · ingest → landing · Type `01` |
| 11 | [`11-consensus.md`](11-consensus.md) | F | Pass 4 · owner signs · the barrier |
| 12 | [`12-tasking.md`](12-tasking.md) | G | Pass 5 · one leaf, one eval |
| 13 | [`13-loop-valid.md`](13-loop-valid.md) | G | Pass 8 · `valid-minimal` → Parquet + replay |
| 14 | [`14-df-source.md`](14-df-source.md) | G | `DF-SOURCE-001` · 173.44 kept · zero Parquet |
| 15 | [`15-malformed.md`](15-malformed.md) | G | Malformed · quarantine · no publication |
| 16 | [`16-research.md`](16-research.md) | Close | Query Day 3 in · then walk |
