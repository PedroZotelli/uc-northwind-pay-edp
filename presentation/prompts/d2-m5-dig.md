# Move 5 — Dig · `d2-translator-java2py.html`

Copy this prompt to the builder. One move. **Append** Dig after **Floor**.
Do not restyle chrome. Do not author Debrief. Do not skip Shows for Hands-On.

Quality bar: the **live** [`../d2-translator-java2py.html`](../d2-translator-java2py.html)
(Opening `.ts-spine`, `.d2-pipe`, Recap `.req`, SWE seat card, First-write
SVG). Visual bible: [`d2-visuals.md`](d2-visuals.md). Day 1 Dig spine
classes (`.d5r-split` `.cvg-spine`) may be reused if already in the file,
but the **look** is Night 2 glass / pipe / receipts — not a purple kit
poster. Tonight 0–1 are **look**. Dig **runs 2–4**, then Task-Spec, then
Mesh **internals**.

Target: [`../d2-translator-java2py.html`](../d2-translator-java2py.html).
Papers: [`../../docs/README.md`](../../docs/README.md).
Scope: [`../../agenda/d2.md`](../../agenda/d2.md) Dig HUD 19–24.

**Demo (signed).** Slices **D · 2–4** and **E · Task-Spec**. Show first.
Do not flip a slide per prompt.

| HUD | Kind | Staff |
|---|---|---|
| 19 | Dig divider | none |
| 20 | Show · Converge 2–4 + Seamwise | then [`07-prompt-kits.md`](../../run/d2/07-prompt-kits.md) — **do not start Pass 2 yet** |
| **21** | Hands-On **C** | [`08-structure.md`](../../run/d2/08-structure.md) → [`09-decompose.md`](../../run/d2/09-decompose.md) → [`10-consensus.md`](../../run/d2/10-consensus.md) |
| 22 | Show · Task-Spec | then 11 (skip if unsigned) |
| **23** | Hands-On **D** | [`11-taskspec.md`](../../run/d2/11-taskspec.md) |
| 24 | Show · Task-Mesh | **none** — pause, then [`12-research.md`](../../run/d2/12-research.md) |

If `10` is unsigned, **do not run 11**. Home is **`docs/`**, not `cvg/docs/`.
If a slide disagrees with a staff file, **the staff file wins**.

**Order:** Floor (query + Hands-On B) **must already be in the file**.
If the last slide is still Stage or Craft, stop.

HUD 19–24 in the plan assume Stage 02–10. Extra Stage slides shift
numbers. Identify by `data-act-name`. Script counts `section.slide`.

---

## Goal

Insert **six** `<section class="slide">` `data-act="DIG"` after the last
FLOOR slide.

| Planned HUD | data-act-name | Kind |
|---|---|---|
| 19 | Dig | divider |
| 20 | Converge + Seamwise | Show |
| 21 | Execute C | Hands-On **C** — Pass **2 then 3 then 4** |
| 22 | Task-Spec | Show |
| 23 | Execute D | Hands-On **D** — one leaf |
| 24 | Task-Mesh | Show — **no** Hands-On |

Hands-On badge **only** on 21 and 23. Do not put a badge on Mesh.

Unsigned Consensus → Hands-On D is **skipped** (still show Mesh).
No `modern/` product code. No factory Loop (6–8). `cvg` gates; the
agent drafts. Home is **`docs/`**, not `cvg/docs/`.

---

## Chrome

Do not copy CSS. Do not rewrite `<script>`. Reuse `.cvg-spine` `.cvg-pass`
`.d5r-split` `.hs-head` `.hs-chip` `.hs-board` `.hs-3` `.req` `.slice-lookup`
`.hands-on` `.act-num` `.mac` `.ts-spine` `.d2-pipe` `.tag` `.h2` `.lede`
`.wkrail`. Atmosphere + glass: [`d2-visuals.md`](d2-visuals.md).

Icons: `../assets/converge-icon.svg`, `../assets/seamwise-icon.svg`,
`../assets/task-spec-icon.svg` if present — **marks on glass**, not a
logo wall.

## Visual (this move)

| HUD | Clone live `data-act-name` | Pattern |
|---|---|---|
| 19 Dig | `Stage` | divider, **gold**, `act-num` **04** |
| 20 Converge + Seamwise | Opening `.ts-spine` or `.d2-pipe` | 0–1 dim, **2–4 on + tonight**, 5 next, 6–8 off. Not a nine-row table. |
| 21 Execute C | Recap `.req` ×3 | `.hs-board.hs-3` · chip **08–10** · look-up **signed**. `span.hands-on`. |
| 22 Task-Spec | SWE seat card | one hero glass: leaf, eval, `signed_off` false, path pill `docs/tasks/`. |
| 23 Execute D | one glass + `.mac` | chip **11**. Dark if unsigned. `span.hands-on`. |
| 24 Task-Mesh | `First write` SVG or `.d2-pipe` | attempt → eval → retry/settle. Show only. No badge. |

---

## Slide-by-slide

### HUD 19 — Dig divider

```text
data-act="DIG" data-act-name="Dig" data-accent="gold"
```

Clone live **Stage** divider (`data-act-name="Stage"`). Gold aurora.

- Tag: `Move 4 of 5 · Dig · design then leaves`
- `act-num` **04**
- H2: `Explain 2–4. Then sign. Then the leaf.`
- Lede: Query already ran. Tonight Structure → Decompose (Seamwise) →
  **Consensus**. Then Task-Spec. Mesh is internals. Factory 6–8 is later.
- Right: Show 2–4 · Hands-On C · Show Task-Spec · Hands-On D · Show Mesh.

### HUD 20 — Show · Converge 2–4 + Seamwise

```text
data-act-name="Converge + Seamwise" data-accent="gold"
```

**Invert Day 1’s spine.** 0–1 are dim/`off` (already written). **2, 3, 4
are `on` + `tonight`.** 5 on but “next board.” 6–8 `off` + “Day 4 factory.”

Must say:

- Converge coordinates. Never writes product code. `cvg` gates; agent drafts.
- Seamwise **is** Pass 3: seam → swimlane → leg. One owner per handoff.
  Attach **at Decompose**, not after the sign.
- One lane tonight: **ingest → landing**. dlt → Gold = Day 3. Dagster = Day 4.
- Papers live in `docs/` (`adrs/` `seams.md` `consensus.md` `tasks/`).
  Method manual may link `presentation/cvg-aut-systems-spine-steps.html`.
  That HTML is **not** the paper trail.

Do not reinstall Converge as the story. Do not teach Pass 0–1 again.

After the Show, every seat types [`07-prompt-kits.md`](../../run/d2/07-prompt-kits.md)
(read `docs/README.md`, may read the Converge HTML, **do not change any
file**, do not ask OntoLayer these questions). Five asks: Converge vs
`cvg`; Seamwise at Pass 3; one lane ingest → landing; papers in `docs/`;
tonight 2–4 then 5, not factory 6–8. **Do not start Pass 2 yet.**

### HUD 21 — Hands-On C · Structure → Decompose → Consensus

```text
data-act-name="Execute C" data-accent="gold"
span.hands-on
```

Clone Recap · closed `.req` ×3 plus Hands-On chrome: **one board, three tiles**, chip
`board c · barrier`, `run/d2/` · **08–10** (beat **07** already ran on
HUD 20). Instructor drafts the first ADR in public, then every seat.
Instructor cuts seams in public. Consensus: a **different** voice, then
the owner.

| Tile | Beat | Does | Proof |
|---|---|---|---|
| 08 Structure | ADRs in `docs/adrs/` + `CONTEXT.md`. What is true, never how. Landing facts must close: first write Parquet not SFTP; five-file unit; Decimal; privacy at parser; source lie keeps **173.44**, refuse, zero Parquet. Park dlt/Gold/Dagster. `cvg structure --draft --json` | Files exist; no “how to parse” |
| 09 Decompose | `docs/seams.md`. Steel thread Type 01 ingest → landing. Three seams: ingest→landing (Translator, tonight) · dlt→Gold (Constructor, Day 3) · orchestrate+serve (Orchestrator, Day 4). No Task-Specs yet | Three seams named; not “Java vs Python” |
| 10 Consensus | Adversary. Every objection **FIXED** or **ACCEPTED**. Keep **173.44**. Owner signs `docs/consensus.md`. `cvg consensus --sign --json`. A dated signature still counts | Sign on disk. Unsigned → **skip D** |

If `cvg` wrote under `cvg/docs/`, move ADRs, `CONTEXT.md`, `seams.md`,
`consensus.md` into `docs/`.

Look up: **signed**. Do not: write `modern/`; pick a lakehouse as an ADR;
start Task-Spec without a sign.

Verbatim prompts stay in `run/d2/08` `09` `10`. Slide does not paste them
all.

### HUD 22 — Show · Task-Spec

```text
data-act-name="Task-Spec" data-accent="cyan"
```

**Different composition from 20.** Leaves, not lanes.

Must say:

- Attaches at Pass **5**. One leaf, one eval. `signed_off` starts **false**.
- Eval is runnable, not “the agent said it worked.”
- Translation-as-design **ends** here: you can see the work in `docs/tasks/`.
- No eval, no build. No product code tonight.

### HUD 23 — Hands-On D · one leaf

```text
data-act-name="Execute D" data-accent="cyan"
span.hands-on
```

Clone one Recap-papers glass panel plus Hands-On chrome. Chip `board d · leaf`, `run/d2/` · **11**.
Instructor authors the first leaf in public, then every seat.
**Skip this board if Consensus is unsigned.**

One Type 01 leaf (parser **or** writer). Path `docs/tasks/`.
`cvg tasking --draft --json`. If `cvg` wrote under `cvg/docs/`, move the
leaf into `docs/tasks/`. Requires: Exact Decimal; privacy at parse (PAN
token + last4, CPF mask); deterministic Parquet under `modern/landing/`
**when the mesh later runs**; no frozen writes. No product code tonight.

Look up: file + eval, `signed_off` false, **no `modern/` required**.
Do not: Loop; treat Mesh as a license to write Parquet; skip if unsigned
(if 21 failed, this board is dark). No eval → tear it up.

Next after this board: **pause** HUD 24 Show · Task-Mesh (no typing),
then [`12-research.md`](../../run/d2/12-research.md).

### HUD 24 — Show · Task-Mesh internals

```text
data-act-name="Task-Mesh" data-accent="green"
```

**Show only.** How signed leaves run: attempt → eval → retry / settle.
Input = Task-Spec. Output = evidence, not a chat.

Must say:

- Does not replace Consensus. Unsigned leaves do not enter.
- Does not replace Bind. Frozen folders still fail closed.
- Pass **8** unattended + Pass **7** epoch = Day 4 factory.
- Pass **6** Register is opt-in.
- Not `make run` (that is Java). Not dlt.

No Hands-On badge. No fifth board unless you later decide to run Type 01
on the mesh tonight (agenda forbids by default).

---

## Hard bans

- Re-teach Capture / Intent as tonight’s run.
- Seamwise after Consensus.
- Three Hands-On slides for 2–4 (must be **one** board C).
- Hands-On on Mesh.
- Write `modern/` / `make run` as the SWE proof.
- `cvg/docs/` as the home (move into `docs/` if `cvg` emits there).
- Port Java. Type 06. Morning/afternoon.
- Copy old `d2-translator.html` Execute 01–10 / landing smokes.
- Chip **07–10** on board C (07 belongs on HUD 20).
- A fifth Hands-On for Mesh / landing Loop.
- Nine-row pass table as the Show. Spine or `.d2-pipe`, like Opening / Five-file.

## Done when

- Six DIG slides after FLOOR. Badges only on Execute C and D.
- Spine shows 2–4 tonight; 0–1 look; 6–8 Day 4.
- Hands-On C look-up is the **sign**. Hands-On D is the leaf.
- Mesh is internals, not a Loop night.
- Keyboard continues without a JS error.

## Next move (do not do it now)

Move 6 **Debrief** HUD 25–29: divider, In hand, Research (`run/d2/12`),
Next, silent Tomorrow. Append after HUD 24.
