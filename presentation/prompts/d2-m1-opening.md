# Move 1 — Opening · `d2-translator-java2py.html`

Copy this prompt to the builder. One move. Do not author Stage–Debrief in this pass.

You are building Night 2 of the NorthWind Pay bootcamp. Quality bar is
[`../d1-archaeologist.html`](../d1-archaeologist.html) — the live Day 1
deck. Match its chrome, type, HUD, motion, and density. Do **not** match
its story. Do **not** open [`../d2-translator.html`](../d2-translator.html)
(old 32-slide night; discarded).

Scope for the Night: [`../../agenda/d2.md`](../../agenda/d2.md) → **PPT blocks**.
This pass is **Opening only** (HUD 01).

---

## Goal

Create [`../d2-translator-java2py.html`](../d2-translator-java2py.html):

1. Full Day 1 design system (tokens, atmosphere, HUD, tracker, keyboard, reveal).
2. **One** slide: Opening title.
3. HUD total = number of `<section class="slide">` in the file (**1** tonight).
   Later moves **append** slides before `</div><!-- .deck -->` and the counter
   follows. Do not hard-code `29` in the HUD.

After this pass the file must open in a browser, `F11`, HUD `01 / 01`,
OPENING pill in **cyan**.

---

## Chrome (copy, do not invent)

From `d1-archaeologist.html`:

- `<head>` fonts, CSS through `</style>` (the whole Day 1 design system).
- Atmosphere, `.deck-progress`, `#hud`, `#tracker`, `.deck` wrapper.
- Trailing `<script>` HUD / keyboard / reveal / spotlight — **byte-identical
  behavior**. It already counts `section.slide`. Do not rewrite it.
- Self-contained HTML. Google Fonts only external fetch. Images from
  `../assets/` only.

Change in head:

| Field | Value |
|---|---|
| `<title>` | `Translator · java2py` |
| `meta description` | `Night 2 — Translator. Recap, java2py, harness, Converge 2–4, Task-Spec, Task-Mesh internals. Second plant, not a Java port.` |
| favicon diamond | fill `#22d3ee` (cyan), not Day 1 blue |
| CSS comment banner | `DAY 2 · TRANSLATOR — java2py` — inherits Day 1 system |

Do not add a new visual brand. Cyan is the Night 2 accent (Day 1 was purple).
`.title-rule` on this slide may use `var(--cyan)` via inline style; do not
globally restyle `.title-rule` (later slides may use other accents).

---

## Slide 01 — title (the only slide this move)

```text
<section class="slide"
  data-act="OPENING"
  data-act-name="Translator"
  data-accent="cyan">
```

**Composition** — clone Day 1 S01 *structure* (asymmetric `title-grid`,
five-move `ts-spine`, pullquote, `title-foot` with presenter + contract).
Do not clone Day 1 *copy*.

**Atmosphere**

- Background image: `../assets/df-legacy-opt.jpg` (the plant we do not edit).
  Overlay: left-weighted dark gradient (same math as Day 1 S01).
- Local aurora: `aurora--cyan`.
- Tag: `Agentic Engineering Bootcamp · Day 2 of 5 · NorthWind Pay` (`--tag-c: var(--cyan)`).

**Left column**

- Cyan `title-rule`.
- Display: `Translator` then a break then `java2py` in `var(--cyan)`.
  Instrument Serif, same clamp as Day 1 h1 (`30px`–`68px`).
- Sub (editorial, ≤2 sentences):

  > **Yesterday you understood.** Tonight the SWE designs the second plant.
  > **Consensus is the barrier.** Task-Mesh is internals. The factory Loop is later.

- Two seats (border-left, tags), not Day 1’s Operator / Archaeologist:

  | Tag | Title | Line |
  |---|---|---|
  | `Translator` cyan | The SWE | On the keys. Validates. Does not have to know Java. |
  | `java2py` gold | The engine | Second plant. Same raw bytes. Parquet, not a port of `legacy/processor/src`. |

**Right column** — tag `Five moves · the night`. Spine (same `ts-item` mold):

| n | Name | Job | `--c` |
|---|---|---|---|
| 01 | Stage | Recap, SWE, java2py, event-driven | cyan |
| 02 | Craft | Agent Harness — seat, tools, spawn; Bind is rails | gold |
| 03 | Floor | Query brain + ontology until 2–4 has evidence | green |
| 04 | Dig | Converge 2–4 + Seamwise, Task-Spec, Task-Mesh internals | cyan |
| 05 | Debrief | Leaves in hand; factory 6–8 is later | gold |

Note under the spine (italic, one line):

> Nobody ports Java tonight. **java2py reads the same bytes.** Design until the owner signs. Mesh internals — not lights-out.

**Pullquote**

- Text: `An unsigned tech-spec is not a license to code.`
- Who: `The barrier`
- Gloss: `yesterday stopped at Intent · papers live in docs/`

**Footer** (`title-foot`)

- Presenter: `../assets/luan-moreno.png`, Luan Moreno, same role line as Day 1.
- Contract three cells:

  | k | color | v |
  |---|---|---|
  | Machine | cyan | Oh My Pi → OpenRouter → workspace → DeepSeek. Grade gates, not vendors. |
  | Fence | red | Frozen: `legacy/` `contracts/` `gen/` `infra/`. Bind is rails on the harness. |
  | Proof | gold | Owner **signs**. Task-Specs in `docs/tasks/`. Mesh understood. No factory Loop. |

---

## Hard bans

- Do not mention morning / afternoon.
- Do not port Java. Do not say “translate Java source.”
- Do not put Type `06` on this slide.
- Do not say Consensus was signed (it was not).
- Do not say `modern/` exists.
- Do not install Converge on this slide.
- Do not add Stage divider or any second `<section class="slide">`.
- Do not copy copy from `d2-translator.html`.
- Do not invent a sixth HUD block.
- Numbers on screen must exist in the repo (`docs/`, frozen folders). No fake CI.

---

## Done when

- File exists at `presentation/d2-translator-java2py.html`.
- One `section.slide`. HUD `01 / 01`, act `OPENING`, accent cyan.
- Title reads Translator / java2py. Five moves match the table above.
- Keyboard `→` does nothing useful (only one slide) without error.
- `F11` looks like Day 1 Opening with a **cyan** night, not a purple clone of Archaeologist.

## Next move (do not do it now)

Move 2 appends Stage HUD 02–10 after this section, still in this file.
Same chrome. Do not restyle tokens.
