# Move 4 — Floor · `d2-translator-java2py.html`

Copy this prompt to the builder. One move. **Append** Floor after **Craft**.
Do not restyle chrome. Do not author Dig–Debrief. Do not rebuild the
Second Brain (that was Day 1).

Quality bar: the **live** [`../d2-translator-java2py.html`](../d2-translator-java2py.html)
(glass papers, SWE tiles, Recap `.req`). Visual bible:
[`d2-visuals.md`](d2-visuals.md). Tonight: **query** until Pass 2–4 has
evidence. Do not clone Day 1 “empty notebook / unzip nine files,” and do
not flatten into two grey columns.

Target: [`../d2-translator-java2py.html`](../d2-translator-java2py.html).
Scope: [`../../agenda/d2.md`](../../agenda/d2.md) Floor HUD 15–18.

**Demo (signed).** Slice **C · Query**. Craft fail-closed (beat 04) already
ran. Next in staff is Floor Show **16–17**, then they type.

| HUD | Kind | Staff |
|---|---|---|
| 15 | Floor divider | none |
| 16 | Show · Second Brain | then [`05-query-brain.md`](../../run/d2/05-query-brain.md) |
| 17 | Show · OntoLayer + specs | then [`06-query-graph.md`](../../run/d2/06-query-graph.md) |
| **18** | Hands-On **B** | **05–06** (one board, two columns) |

Show **first**. Do not skip to the board. Same notebook. No tenth file.
If a slide disagrees with a staff file, **the staff file wins**.

**Order:** Craft (Harness + Hands-On A) **must already be in the file**.
If the last slide is still Stage “Ingest seam”, stop and run Move 3 first.

HUD integers in the plan (15–18) assume Stage is HUD 02–10. If Stage
gained a Q&A slide, numbers shift; identify by `data-act-name`, not by
a frozen index. Script still counts `section.slide`.

---

## Goal

Insert **four** `<section class="slide">` `data-act="FLOOR"` after the
last CRAFT slide.

| Planned HUD | data-act-name | Kind |
|---|---|---|
| 15 | Floor | divider |
| 16 | Second Brain | Show |
| 17 | OntoLayer + specs | Show |
| 18 | Execute B | Hands-On **B** |

Hands-On badge **only** on Execute B. Show 16 and 17 must exist — do not
skip to the board.

After this pass: query is for **Converge 2–4**, not a tour. Nine sources.
No tenth file.

---

## Chrome

Do not copy CSS. Do not rewrite `<script>`. Reuse `.hs-head` `.hs-chip`
`.hs-board` `.req` `.slice-lookup` `.callout` `.hands-on` `.act-num`
`.lede` `.h2` `.mac` `.d5r-split` `.tag` `.wkrail`. Atmosphere + glass:
[`d2-visuals.md`](d2-visuals.md).

Images: `../assets/notebooklm-icon.webp`, `../assets/postgres.svg` as
**quiet marks** on glass, not heroes. No `legacy/` source as visual truth.
Plant stills: `df-gates-opt.jpg` / `df-legacy-opt.jpg` behind overlays.

## Visual (this move)

| HUD | Clone live `data-act-name` | Pattern |
|---|---|---|
| 15 Floor | `Stage` | divider, **green** aurora, `act-num` **03** |
| 16 Second Brain | `SWE Role` tiles | J1–J5 as numbered glass (not a prompt dump, not unzip UI). Optional quiet NotebookLM mark. |
| 17 OntoLayer + specs | `Recap · papers` | dual glass: specs vs graph. Watermarks optional. Gold callout for paid table + grain. Without→with as two states, not a terminal dump. |
| 18 Execute B | Recap `.req` + `.hs-head` | two columns, chip **05–06**, look-up green/red. `span.hands-on`. |

---

## Slide-by-slide

### Divider — Floor

```text
data-act="FLOOR" data-act-name="Floor" data-accent="green"
```

Clone live **Stage** divider (`data-act-name="Stage"`). Green aurora.

- Tag: `Move 3 of 5 · Floor · query`
- `act-num` **03**
- H2: `Ask until 2–4 has evidence.`
- Lede: Two instruments, one job. Brain = concepts. OntoLayer + specs =
  grain, keys, what we will build. **Do not rebuild the notebook.**
- Right: three beats — Show Brain · Show graph+specs · Hands-On B.

### Show — Second Brain

```text
data-act-name="Second Brain" data-accent="cyan"
```

**Query, not ingest.** Day 1 already fed nine packs.

Must say:

- Same notebook as last Night. Types 01–05. No Type 06.
- Cite a page or abstain. Fluent with no source is a failure.
- Do not Add sources. Do not upload tech-spec, ADRs, Java, `modern/`, `.dat`.

Job tonight: J1–J5 in [`05-query-brain.md`](../../run/d2/05-query-brain.md).
Name them on the slide; do not paste the full prompts here:

| # | Ask |
|---|---|
| J1 | Privacy boundary. PAN / CPF must never leave sanitize. Cite the page. |
| J2 | Signed overpunch. `00000001234E`. Trailer vs rows. **Cite Marina.** Do not invent Java. |
| J3 | “Refuse the batch” — not a crash. Do not rewrite the trailer. |
| J4 | Sanitize in inbound language (layout, tokenize, last4). Do not quote `.java`. |
| J5 | Do these sources contain the Java parser? If you need `legacy/processor/src`, **you do not have it.** |

Do **not** show “New notebook / unzip / seven questions” as the action.
That was Day 1 Execute 12. Paste one, wait, then the next.

### Show — OntoLayer + specs

```text
data-act-name="OntoLayer + specs" data-accent="purple"
```

**Different composition from Brain.** Beat 06 is **two** prompts: specs,
then graph. Three sources, one table:

| Source | Job |
|---|---|
| Day 1 tech-spec + `spec/type-01-…` | What we will build |
| `contracts/types/01-…` | The judge. Mail does not outrank it |
| OntoLayer | Grain, keys, which procedure writes paid |

Specs look-up (Prompt 1):

| Ask | Healthy |
|---|---|
| Build | `model → parser → schema → writer → handler` → `modern/landing/` Parquet |
| Not | Java import, SFTP CSV as modern input, dlt tonight, Type 06 |
| Judge | `contracts/` |

Graph (Prompt 2): “Where does **paid** live for Type 01?” Name the
reporting table, the grain, and which procedure writes that table.

**MCP first.** `northwind-ontology` `catalog_ask`, or say to run
`make ontology-ask`. **Do not grep SQL.** Staff, if MCP is down:

```bash
make ontology-ask-sql
make ontology-ask
```

Show **without then with** — the contrast is the value. Gold callout:
paid lives on `reporting.card_settlement_reconciliation`, grain
`batch_id + currency`.

Do not ask the graph what Converge is. Graph down → `make deploy && make ontology`.
Do not guess joins.

### Hands-On B — query

```text
data-act-name="Execute B" data-accent="green"
span.hands-on
```

Clone Recap · closed `.req` density plus Hands-On **chrome** (chip,
`run/d2/` path, look-up / do not).
Two columns of work, not four install tiles:

- Chip: `board b · query` · `run/d2/` · **05–06**
- Heading: `Cite a page. Then cite a routine.`
- Left: Brain J1–J5 — staff file 05 (name them: privacy, overpunch,
  refuse, sanitize, not-here). Paste one, wait, then the next.
- Right: Specs (Prompt 1) then graph without/with (Prompt 2) — staff file 06.
- Look up: J2 cites Marina **173.44** vs **173.45**. J1 names PAN/CPF.
  J5 does **not** invent Java. Paid table + grain named. Notebook still
  **nine** sources. No git writes.
- Do not: rebuild notebook; upload zip/`legacy/`/`contracts/`/tech-spec;
  skip the without pass; Google / empty notebook (pair); dump Java into
  NotebookLM; start Structure on mush.

Verbatim prompts live in `run/d2/05` and `06`. The slide sends them there.
Next after this board: [`07-prompt-kits.md`](../../run/d2/07-prompt-kits.md)
on Dig Show HUD 20.

---

## Hard bans

- Rebuild NotebookLM / unzip nine files as tonight’s action.
- Tenth source (tech-spec, ADRs, Java, Type 06).
- Hands-On badge on the two Show slides.
- Skip Show and jump to Execute B.
- Port Java. Grep SQL as the OntoLayer method.
- Ask the graph what a kit is.
- Factory Loop / `make run` as the proof.
- `make ontology-ask-sql` as the **default** method (MCP / `ontology-ask`
  first; sql is the staff fallback when MCP is down).
- Flatten 16–17 into grey two-column posters. Must match live glass (SWE tiles / Recap papers).

## Done when

- Four FLOOR slides after CRAFT. Hands-On badge only on Execute B.
- Show Brain = query existing notebook. Show graph = without then with.
- Look-up matches `run/d2/05` + `06` proofs.
- Keyboard continues without a JS error.

## Next move (do not do it now)

Move 5 **Dig** HUD 19–24: Show kits (`run/d2/07`), Hands-On C
(`08`–`10` sign), Task-Spec Show + Hands-On D (`11`), Task-Mesh Show
(no file).
