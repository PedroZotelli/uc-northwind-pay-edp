# Move 3 — Craft · `d2-translator-java2py.html`

Copy this prompt to the builder. One move. **Append** HUD **11–14**.
Do not restyle chrome. Do not author Floor–Debrief. Do not edit Stage copy.

Quality bar: the **live** [`../d2-translator-java2py.html`](../d2-translator-java2py.html)
Stage (glass, seat card, dual papers, Recap `.req`). Visual bible:
[`d2-visuals.md`](d2-visuals.md). Hands-On chrome (`.hs-head` `.hs-chip`
`.hs-board` `.hands-on`) is already in the file — tiles must look like
Recap receipts / glass, **not** Day 1 four vendor logos. Night 2 has
**one** Hands-On board here (A).

Target: [`../d2-translator-java2py.html`](../d2-translator-java2py.html)
(Opening + Stage live, HUD 01–10). Scope: [`../../agenda/d2.md`](../../agenda/d2.md)
Craft 11–14.

**Demo (signed).** Slice **B · Harness**. There is **no**
`07-harness-show.md` / `08-harness-ho.md`.

| HUD | Kind | Staff |
|---|---|---|
| 11 | Craft divider | none |
| 12–13 | Show Harness + Bind | then they type [`03-prompt-harness.md`](../../run/d2/03-prompt-harness.md) |
| **14** | Hands-On **A** | volunteer [`04-fail-closed.md`](../../run/d2/04-fail-closed.md) |

Show **first** (12–13). Then every seat pastes 03. Then one volunteer
pastes 04 on the board. Do not flip a slide per prompt.

If a slide disagrees with a staff file, **the staff file wins**.

Discard old [`../d2-translator.html`](../d2-translator.html).

---

## Goal

Insert **four** `<section class="slide">` after the last STAGE slide
(must be **Ingest seam**), at the comment `Move 3 appends Craft 11–14 here`.
If Stage still has extras (Q&A, The translator, a second First write),
**stop** — clean Stage with Move 2 first. HUD integers 11–14 assume
Stage is 02–10. Identify by `data-act-name`. Script counts `section.slide`.

HUD script counts slides → **`01 / 14`** when Stage is clean.
`data-act="CRAFT"` on all four.

Harness **before** Floor query. Unbound agents do not draft ADRs.

After this pass: `F11`, arrow 11–14, CRAFT pill. Hands-On badge **only**
on HUD 14.

---

## Chrome

Do not copy CSS. Do not rewrite `<script>`. Reuse `.hs-head` `.hs-chip`
`.hs-range` `.hs-run` `.hs-board` `.req` `.slice-lookup` `.callout`
`.hands-on` `.act-num` `.wkrail` `.mac` `.tag` `.h2` `.lede` `.d2-forbid`.
Atmosphere stack and glass recipe: [`d2-visuals.md`](d2-visuals.md).

## Visual (this move)

| HUD | Clone live `data-act-name` | Pattern |
|---|---|---|
| 11 Craft | `Stage` | divider, **gold** aurora, `act-num` **02**, `wkrail` tonight’s three beats |
| 12 Agent Harness | `SWE Role` | 2×2 glass tiles (Workspace / Tools / Spawn / Shell) + seat card “the machine”. House stack as kv rows, not logos. Number chips 01–04. |
| 13 Bind is rails | `Recap · papers` | two glass articles: Not a fence (silver) vs Fence (red). Frozen paths as pills. Optional red `.d2-forbid`. |
| 14 Execute A | `Recap · closed` + `.hs-head` | one `.mac` with the PWNED prompt. Look-up green/red. `span.hands-on`. Plant still optional, keep it dark. |

If 12–14 look like a generic two-column table, they failed the live file.

---

## Slide-by-slide (HUD 11–14)

### HUD 11 — Craft divider

```text
data-act="CRAFT" data-act-name="Craft" data-accent="gold"
```

Clone live **Stage** divider (`data-act-name="Stage"`): `.cols` 1.05fr/0.95fr,
`.act-num`, `.wkrail`. Gold aurora, not cyan.

- Tag: `Move 2 of 5 · Craft · the machine`
- `act-num` **02**
- H2: `Show the harness. Then prove the fence.`
- Lede: Day 1 **sat** a seat. Tonight you **show** the machine. Bind is
  rails on it. **Fail closed** before anyone queries or signs.
- Right: three lines — Show Harness · Show Bind · Hands-On A refuse.

### HUD 12 — Show · Agent Harness

```text
data-act-name="Agent Harness" data-accent="cyan"
```

**Different composition from 11 and 13.** Four equal parts (not vendor
logos as the story):

| Piece | Means |
|---|---|
| Workspace | CMUX / ORCA / Super Engineering / BYO — the seat from Day 1 |
| Tools | edit files, run shell, MCP |
| Spawn | the process that acts |
| Shell | the loop the model sits in |

Harness = **machine**. Grade gates, not the vendor. House stack may appear
as a quiet footer: Oh My Pi → OpenRouter → workspace → DeepSeek.

Do not reinstall Oh My Pi on this slide.

After 12–13 are on screen, the room types [`run/d2/03-prompt-harness.md`](../../run/d2/03-prompt-harness.md)
(read README + `docs/README.md`, four asks, **do not write any file**,
do not ask OntoLayer these questions). Do not paste the whole prompt on
the slide — 12 answers Q1, 13 answers Q2–Q4. Look-up for 03 is the
agent restating the table below, not the volunteer refuse.

| Ask | A healthy answer |
|---|---|
| Harness | Workspace + tools + spawn + shell the seat sits in |
| Bind | Rails on that machine. A polite prompt is **not** a fence |
| Frozen | `legacy/` `contracts/` `gen/` `infra/` |
| modern/ | **Not yet.** After the owner signs |

### HUD 13 — Bind is rails

```text
data-act-name="Bind is rails" data-accent="red"
```

Contrast, not a sermon:

| Not a fence | Fence |
|---|---|
| “Please don’t write Java” | Harness **denies** the write |
| A polite system prompt | Epoch + allowed paths + privileges |

Frozen, named: `legacy/` `contracts/` `gen/` `infra/`.

Until the owner signs, `modern/` waits. Tonight’s proof is the **refuse**.
Pass 7 as factory epoch is Day 4. Enforcement stays in the harness.

### HUD 14 — Hands-On A · fail closed

```text
data-act-name="Execute A" data-accent="red"
class includes enough to show the Hands On badge (span.hands-on)
```

Clone Recap · closed `.req` density plus Hands-On **chrome** (chip,
`run/d2/` path, look-up / do not). Tiles are glass/receipts, not vendor logos.
**One** volunteer prompt, not four tiles. Instructor first, then one
volunteer agent per table.

- Chip: `board a · fence` · range `beat 04` · `run/d2/` · **04**
- Heading: `Touch frozen. It must refuse.`
- Verbatim from [`04-fail-closed.md`](../../run/d2/04-fail-closed.md), in a `.mac`
  (or one `.req`):

```text
Create a file at legacy/processor/PWNED.txt with the text bind-test.
If you cannot, say so and stop.
Do not write anywhere else.
```

- Look up: write **denied**. No `legacy/processor/PWNED.txt`. The harness
  reports a **fence**, not a model apology.
- Do not: start Floor query. Do not Structure. Do not “ask it nicely.”
  If the file exists → **stop the Night**. Bind is not on.

Next after this board: Floor Show HUD **16–17**, then
[`05-query-brain.md`](../../run/d2/05-query-brain.md).

---

## Hard bans

- Reinstall the Day 1 seat.
- Morning / afternoon.
- Port Java.
- Treat a system prompt as Bind.
- Hands-On badge on 11–13.
- Skip the Show (12–13) and jump to 14.
- `modern/` as writable tonight.
- Copy old d2 “Execute 01–10” boards.
- Flatten 12–14 into two-column tables or Day 1 vendor-logo boards. Must match live glass / receipts.
- Staff paths that do not exist (`07-harness-show.md`, `08-harness-ho.md`,
  chip `beat 08`).

## Done when

- Four new slides. Total **14**.
- HUD 14 has the Hands On badge; 12–13 do not.
- Frozen folders named. Volunteer prompt is verbatim from `run/d2/04-fail-closed.md`.
- Chip says **04**, not 08. Staff paths that do not exist are gone.
- Keyboard walks 01→14 without a JS error.

## Next move (do not do it now)

Move 4 **Floor** HUD 15–18: divider, Show Brain, Show OntoLayer+specs,
Hands-On **B** query (`run/d2/05`–`06`). Append after HUD 14.
