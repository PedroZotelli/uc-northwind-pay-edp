# Move 2 — Stage · `d2-translator-java2py.html`

Copy this prompt to the builder. One move. **Append** HUD **02–10**. Do not
restyle chrome. Do not author Craft–Debrief. Do not touch Opening copy
except to keep it valid.

Quality bar: [`../d1-archaeologist.html`](../d1-archaeologist.html) Stage
(divider, `wkrail`, `h2`/`lede`, `mac`, receipts, two-rail flows). Match
density and **vary composition** — three centered title-only slides in a
row is a smell.

Target file: [`../d2-translator-java2py.html`](../d2-translator-java2py.html)
(Opening already live). Scope: [`../../agenda/d2.md`](../../agenda/d2.md)
PPT blocks + staff [`../../run/d2/02-recap-closed.md`](../../run/d2/02-recap-closed.md)–[`06-event-driven.md`](../../run/d2/06-event-driven.md).

Discard: [`../d2-translator.html`](../d2-translator.html).

---

## Goal

Insert **nine** `<section class="slide">` after Opening, before
`</div><!-- .deck -->` (the comment `Move 2 appends Stage 02–10 here`).

HUD script already counts slides → **`01 / 10`**. Do not hard-code 29.

`data-act="STAGE"` on all nine. Keyboards down. No Hands-On board. No
Execute chip. No `make run` on a slide (staff look-up for MATCHED is
the **terminal**, not a Hands-On).

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

Clone Day 1 S03 divider **structure** (`cols` 1.05fr / 0.95fr, `act-num`,
`wkrail`). Cyan, not purple.

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

### HUD 10 — Ingest seam

```text
data-act-name="Ingest seam" data-accent="gold"
```

Three verbs, equal weight, one row:

**sense** the drop → **claim** the batch → **emit** Parquet

Not Dagster (Day 4). Not dlt (Day 3). This is tonight’s seam.

---

## Hard bans

- Morning / afternoon.
- Port / transpile / wrap Java CSV.
- Type 06.
- Consensus already signed.
- `modern/` as if it exists.
- Hands-On / Execute chips.
- A sixth HUD block.
- Copy from old `d2-translator.html`.
- Fake CI. Fake nets other than **173.45** MATCHED and **173.44** the lie.

## Done when

- Nine new `section.slide` + Opening = **10** slides.
- HUD `10 / 10` on the last Stage slide; act **STAGE**.
- Recap is two slides (closed / papers), not three lectures.
- java2py clearly second plant. Ingest seam three verbs.
- Keyboard walks 01→10 without a JS error.

## Next move (do not do it now)

Move 3 **Craft** HUD 11–14: divider, Show Harness, Bind is rails,
Hands-On **A** fail-closed. Append after HUD 10.
