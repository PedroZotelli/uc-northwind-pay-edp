# Move 2 — Stage · `d2-translator-java2py.html`

Copy this prompt to the builder. One move. **Append** HUD **02–10**. Do not
restyle chrome. Do not author Craft–Debrief. Do not touch Opening copy
except to keep it valid.

Quality bar: the **live** [`../d2-translator-java2py.html`](../d2-translator-java2py.html)
Opening + Stage (glass papers, SWE seat card, java2py wordmark, two-lane
SVG, cinematic Why-a-file, `.d2-pipe`). Visual bible:
[`d2-visuals.md`](d2-visuals.md). Day 1 is chrome only. Match that
density and **vary composition** — three centered title-only slides in a
row is a smell. If you rebuild Stage, clone the live slides; do not flatten
them back into two-column posters.

Target file: [`../d2-translator-java2py.html`](../d2-translator-java2py.html)
(Opening already live). Scope: [`../../agenda/d2.md`](../../agenda/d2.md)
PPT blocks. Staff clock: [`../../run/d2/README.md`](../../run/d2/README.md).

**Demo (signed).** Recap is Slice **A** — they type two beats, then you
lecture. There is **no** `02-recap-closed.md` / `06-event-driven.md`.

| HUD | Kind | Staff |
|---|---|---|
| 01–02 | Opening + Stage divider | none — already on the deck |
| **03** Recap · closed | they type | [`01-prompt-status.md`](../../run/d2/01-prompt-status.md) |
| **04** Recap · papers | they type | [`02-prompt-papers.md`](../../run/d2/02-prompt-papers.md) |
| **05–10** SWE · java2py · ingest | **pause — deck only** | none |

After beat 02, **do not** jump to Craft. Walk HUD 05–10. Craft starts at
HUD 11 with beat 03.

If a slide disagrees with a staff file, **the staff file wins**.

Discard: [`../d2-translator.html`](../d2-translator.html).

---

## Goal

Insert **exactly nine** `<section class="slide">` after Opening, before
the Craft marker (or `</div><!-- .deck -->`). No tenth Stage slide.

HUD script already counts slides → **`01 / 10`**. Do not hard-code 29.

`data-act="STAGE"` on all nine. **No Hands-On badge. No Execute chip.**
Boards A–D start at Craft. Recap typing is a **look-up strip**, not a
Hands-On board. No `make run` as a slide action — MATCHED is the
**terminal** after they paste `run/d2/01`.

Exactly these nine `data-act-name` values, in this order:
`Stage` · `Recap · closed` · `Recap · papers` · `SWE Role` · `java2py · problem`
· `First write` · `Five-file` · `Why a file` · `Ingest seam`.

If Opening+Stage already contain extras (`Q&A · impressions`,
`The translator`, a second `First write`), **delete them in this pass**
so HUD 02–10 match the table. Do not keep a duplicate.

After this pass: `F11`, arrow through 02–10, STAGE pill, cyan/gold/green
accents as specified. Opening still HUD 01.

---

## Chrome

Do **not** copy CSS from Day 1 again. Do **not** rewrite `<script>`.
Reuse classes already in the file: `.tag` `.h2` `.lede` `.cols` `.act-num`
`.wkrail` `.wkr` `.mac` `.reveal` `.aurora--cyan` `.aurora--gold`
`.aurora--green` `.aurora--red` `.pullquote` `.title-rule`.

Images only from `../assets/`. Prefer `df-legacy-opt.jpg`, `d0-night-drop.jpg`,
`df-gates-opt.jpg` — not Day 1 purple hero as a default.

---

## Slide-by-slide (HUD 02–10)

Every slide: one idea. `data-act-name` = short HUD label.

### HUD 02 — Stage divider

```text
data-act="STAGE" data-act-name="Stage" data-accent="cyan"
```

Clone the **live** Stage divider already in this file (`cols` 1.05fr / 0.95fr,
`act-num`, `wkrail`). Cyan, not purple. If you are rebuilding, keep that
HTML; do not flatten it.

- Tag: `Move 1 of 5 · Stage · keyboards down`
- `act-num` **01** (first **move**, not HUD number)
- H2: `Yesterday closed. Tonight you name the engine.`
- Lede: Recap is **one act**. Then SWE, `java2py`, event-driven. **No parser.**
- Tags: `recap` `java2py` `ingest seam`
- Right `wkrail`: 01 Archaeologist (done, muted), **02 Translator now**, 03 Constructor, 04 Orchestrator, 05 Dark Factory. Job lines: 02 = Recap → java2py → 2–4 → Task-Spec · Mesh internals. 03 = dlt → Gold. 04 = factory 6–8. 05 = sealed Type 06.

### HUD 03 — Recap · what closed

```text
data-act-name="Recap · closed" data-accent="green"
```

Receipts, not a speech. Grid of **six** closed facts (2×3 or 3×2). Each:
mono kicker + one line.

| Kicker | Line |
|---|---|
| PLANT | Type 01 **MATCHED** · net **173.45** · `B202607230000001` |
| BRAIN | Nine packs. Types 01–05. No Type 06. |
| GRAPH | OntoLayer over live Postgres. Without, then with. |
| CAPTURE | `docs/brd-type-01-card-settlement.md` |
| INTENT | `docs/tech-spec-type-01-card-settlement.md` |
| STOP | **No Consensus. No `modern/`. No Pass 2.** |

Footer: `evidence/` in the **terminal**. Do not `make run` unless the packet is missing.

Then a Day 1 `slice-lookup` strip (**not** a Hands-On badge):

- Staff: leave the deck. Type [`run/d2/01-prompt-status.md`](../../run/d2/01-prompt-status.md).
  Agent runs `make status`, then `cat evidence/B202607230000001/reconciliation.json`
  in the **terminal** (not Git).
- Look up: Postgres + four SFTP roles **healthy**. **MATCHED** · **173.45** ·
  **173.45** · **0.00**. MATCHED = source, stage, and books agree to the cent.
- Do not: `make run` unless that evidence file is missing. Do not share
  Compose (`northwind-pay-legacy`, port **2222**) with another checkout.
  Unhealthy → **stop**. Missing packet → Day 1 `05-boot` then `08-prompt-make-run`.

### HUD 04 — Recap · transcript + papers

```text
data-act-name="Recap · papers" data-accent="gold"
```

**Different composition from 03.** Two document cards (BRD / tech-spec)
+ a thin strip: transcript is for **clarifications they actually stumbled
on**, not a re-read. Paths visible in mono:

- `docs/brd-type-01-card-settlement.md`
- `docs/tech-spec-type-01-card-settlement.md`
- `transcripts/tr-d1-archaeologist.cc.vtt`

Do not paste VTT lines. Do not rerun Capture. Map: `docs/` is Converge home,
not `cvg/docs/`.

Restate on the cards, short: Helena; keep **173.44**; inbound `spec/` vs
judge `contracts/`; first write later, not SFTP; no stack.

Look-up strip (still **no** Hands-On badge):

- Staff: [`run/d2/02-prompt-papers.md`](../../run/d2/02-prompt-papers.md).
  Agent **reads** `docs/README.md`, the BRD, and the tech-spec. Does not
  rerun Pass 0–1. Does not invent a BRD.
- Look up: Helena. Type `01` steel thread. Trailer **173.44** vs rows
  **173.45**. `spec/` inbound. `contracts/` judge. First write later, not
  SFTP. No stack. No `modern/`.
- After this beat: **pause**. HUD **05–10** are lecture. No typing until
  Craft Show (HUD 12–13) then [`03-prompt-harness.md`](../../run/d2/03-prompt-harness.md).

HUD **05–10** — **deck only**. You talk; they watch. No `run/d2/` path
on these slides. No look-up strip that sends them to an agent.

### HUD 05 — The SWE Role

```text
data-act-name="SWE Role" data-accent="cyan"
```

Two columns: **does** / **does not**. Not a persona poster.

Does: on the keys; validates; grasps concepts; query then design; Task-Specs
only after the sign.

Does not: have to know Java; port `legacy/processor/src`; stand up dlt or
Dagster tonight; wrap Java CSV.

### HUD 06 — java2py · the problem

```text
data-act-name="java2py · problem" data-accent="cyan"
```

One claim: **second plant**, not a source translator. Nickname `java2py`
in gold/cyan. You may look at Java to **name a concept**. You may not
**copy** Java to compute an answer. Contract is the judge.

### HUD 07 — Two plants · first write

```text
data-act-name="First write" data-accent="gold"
```

Draw both rails. Same `SFTP raw/incoming` at the top.

```text
Legacy (MATCHED):  Java 21 → SFTP csv/outgoing → Postgres
java2py (after the sign):  Python five-file → modern/landing/ Parquet
```

Mixing destinations is a failed day. `modern/` does **not** exist yet.

### HUD 08 — Five-file · not a port

```text
data-act-name="Five-file" data-accent="cyan"
```

Tree, mono, in a `.mac` or equivalent — names only, no code:

```text
model.py   parser.py   schema.py   writer.py   handler.py
```

One line each (typed records / grammar / privacy+controls / atomic Parquet /
compose the batch). Footer: **not a port**. Observation only.

### HUD 09 — Event-driven · why a file

```text
data-act-name="Why a file" data-accent="green"
```

Money lands overnight as **files**, not an API. That landing **is** the
event. Not Kafka. Not a bus. (May reuse night-drop atmosphere; do not
repeat Day 1 “money arrives as files” copy word-for-word — this slide is
*why the architecture is event-driven*.)

## Visual (this move)

Atmosphere + glass + type from [`d2-visuals.md`](d2-visuals.md). Clone
live `data-act-name` structure; keep the signed copy.

| HUD | Clone live | Pattern |
|---|---|---|
| 02 Stage | itself | divider · `wkrail` |
| 03 Recap · closed | itself | six `.req` + rule footer. Add look-up strip for beat 01 (not a Hands-On badge). |
| 04 Recap · papers | itself | dual glass `<article>` + stamps. Add look-up for beat 02. |
| 05 SWE Role | itself | 2×3 glass + seat card — **not** a does/does-not poster |
| 06 java2py | itself | giant `java`/`2`/`py` + three glass |
| 07 First write | itself | two-lane `.arch` SVG |
| 08 Five-file | `Five-file package` | `.d2-pipe` + `.d2-sound` |
| 09 Why a file | itself | cinematic left copy + `.contract` |
| 10 Ingest seam | SWE 3-up glass **or** `.d2-pipe` | **sense → claim → emit** as three equal glass tiles (or pipe nodes). Not a bullet list. Optional cinematic stack like Why a file. |

Delete extras (`Q&A · impressions`, `The translator`) rather than restyling them into the nine.

### HUD 10 — Ingest seam

```text
data-act-name="Ingest seam" data-accent="gold"
```

Three verbs, equal weight, one row:

**sense** the drop → **claim** the batch → **emit** Parquet

Not Dagster (Day 4). Not dlt (Day 3). This is tonight’s seam.

This is the last Stage slide. Next comment in the HTML:
`<!-- Move 3 appends Craft 11–14 here. -->`

---

## Hard bans

- Morning / afternoon.
- Port / transpile / wrap Java CSV.
- Type 06.
- Consensus already signed.
- `modern/` as if it exists.
- Hands-On / Execute chips on any Stage slide.
- A sixth HUD block.
- Copy from old `d2-translator.html`.
- Extra Stage slides: **Q&A**, **The translator**, a second **First write**,
  a second **Five-file**. Recap is **two** slides, not three lectures.
- Staff paths that do not exist (`02-recap-closed.md`, `06-event-driven.md`).
- Fake CI. Fake nets other than **173.45** MATCHED and **173.44** the lie.
- Jumping from HUD 04 to Craft — HUD 05–10 must exist as lecture.
- Flattening live glass (papers, SWE seat, java2py wordmark, SVG lanes, pipe) into two-column posters.

## Done when

- Nine Stage `section.slide` + Opening = **10** slides. No extras.
- HUD `10 / 10` on **Ingest seam**; act **STAGE**.
- HUD 03 look-up matches `run/d2/01` proof. HUD 04 look-up matches `run/d2/02`.
- HUD 05–10 have no staff path. java2py is a second plant. Ingest = three verbs.
- Keyboard walks 01→10 without a JS error.

## Next move (do not do it now)

Move 3 **Craft** HUD 11–14: divider, Show Harness, Bind is rails,
Hands-On **A** fail-closed (`run/d2/03` then `04`). Append after HUD 10.
