# Move 6 — Debrief · `d2-translator-java2py.html`

Copy this prompt to the builder. One move. **Append** Debrief after **Dig**.
Do not restyle chrome. Do not edit Opening–Dig copy. Do not add a fifth
Hands-On.

Quality bar: the **live** [`../d2-translator-java2py.html`](../d2-translator-java2py.html)
(Stage divider, Recap `.req`, glass papers, SWE tiles, Why-a-file cinematic).
Visual bible: [`d2-visuals.md`](d2-visuals.md). Silent class comes from
Day 1 chrome already in the file. **Do not** copy Day 1 Debrief copy
(Three Truths / Two Plants / Receipts as extra slides). Night 2 is
**five** Debrief slides that look like Stage, not like a new brand.

Target: [`../d2-translator-java2py.html`](../d2-translator-java2py.html).
Scope: [`../../agenda/d2.md`](../../agenda/d2.md) Debrief HUD 25–29.
Staff: [`../../run/d2/12-research.md`](../../run/d2/12-research.md) only.

**Demo (signed).** Slice **Close**. Mesh Show (HUD 24) already ran — no
typing there. Research is the last beat, then they walk.

| HUD | Kind | Staff |
|---|---|---|
| 25 | Debrief divider | none |
| 26 | In hand | none — what is true now |
| **27** | Research | [`12-research.md`](../../run/d2/12-research.md) — three queries |
| 28 | Next | homework, then walk |
| 29 | Tomorrow | **silent** — Constructor |

If a slide disagrees with a staff file, **the staff file wins**.

**Order:** Dig (HUD 19–24, including Task-Mesh Show) **must already be
in the file**. If the last slide is Hands-On D, stop — Mesh Show is
missing.

HUD integers in the plan (25–29) assume Stage is 02–10. Extra Stage
slides shift numbers. Identify by `data-act-name`. Script counts
`section.slide`.

---

## Goal

Insert **five** `<section class="slide">` `data-act="DEBRIEF"` after the
last DIG slide (Task-Mesh).

| Planned HUD | data-act-name | Kind |
|---|---|---|
| 25 | Debrief | divider |
| 26 | In hand | close |
| 27 | Research | close — they type beat 12 |
| 28 | Next | close |
| 29 | Tomorrow | silent |

No Hands-On badge. No Execute chip. Research sends them to `run/d2/12`;
it is **not** board E.

After this pass the deck is the whole Night. HUD total = number of
`section.slide`. Do not hard-code 29 if Stage still has extras — **prefer
cleaning Stage first** (Move 2). If extras remain, still append these five.

---

## Chrome

Do not copy CSS. Do not rewrite `<script>`. Reuse `.act-num` `.wkrail`
`.h2` `.lede` `.tag` `.three-col` `.req` `.slice-lookup` `.callout`
`.slide--silent` `.rtw-ghost` `.tom-step` `.hands-bg` `.contract`.
Atmosphere + glass: [`d2-visuals.md`](d2-visuals.md).

Images: `../assets/` only (`df-hero-opt.jpg`, `d0-night-drop.jpg`).
Not Day 1 purple hero as a default.

## Visual (this move)

| HUD | Clone live `data-act-name` | Pattern |
|---|---|---|
| 25 Debrief | `Stage` | divider, **gold**, Translator `wkr--done`, Constructor `wkr--now` |
| 26 In hand | `Recap · closed` | six `.req` receipts of what they hold |
| 27 Research | `Recap · papers` three-up | three glass articles (OntoLayer / Brain / `plans/modern.md`) + look-up |
| 28 Next | `SWE Role` 2×2 glass | four homework tiles. No morning/afternoon. |
| 29 Tomorrow | `Why a file` + `.slide--silent` | plant photo, `.rtw-ghost`, Constructor verb, `.tom-step` |

---

## Slide-by-slide

### HUD 25 — Debrief divider

```text
data-act="DEBRIEF" data-act-name="Debrief" data-accent="gold"
```

Clone live **Stage** divider (`data-act-name="Stage"`). Gold aurora. Translator `wkr--done`, Constructor `wkr--now`.

- Tag: `Move 5 of 5 · Debrief · close the translator`
- `act-num` **05**
- H2: `Leaves in hand. The factory is later.`
- Lede: Design is done when the owner **signs**, not when the slide looks
  complete. Tonight you hold Task-Specs, not Parquet. Factory Loop (6–8)
  is Day 4.
- Right `wkrail`: 02 Translator **done**. 03 Constructor **next** (dlt →
  Gold, only if landing exists). 04 Orchestrator factory 6–8. 05 Dark
  Factory sealed Type 06.

Do not say they wrote `modern/`. Do not say Consensus is still unsigned
if HUD 21 look-up was the sign — the Night’s close assumes they signed.
If they did not sign, In hand must not fake a `docs/consensus.md`.

### HUD 26 — In hand

```text
data-act-name="In hand" data-accent="green"
```

**Different composition from 25 and 27.** Receipts of **what they hold**,
not a speech. Six facts (2×3 or ledger), each mono kicker + one line:

| Kicker | Line |
|---|---|
| RECAP | MATCHED · papers in `docs/` · transcript clarifications |
| ENGINE | `java2py` = second plant, not a port |
| FENCE | Fail-closed on `legacy/` `contracts/` `gen/` `infra/` |
| SIGN | ADRs · `docs/seams.md` · **owner signed** `docs/consensus.md` |
| LEAF | One Task-Spec + eval in `docs/tasks/` · `signed_off` **false** |
| MESH | Internals named. **No factory Loop.** No `modern/` required |

Footer strip: same Second Brain and OntoLayer — **not rebuilt**. No dlt.
No Gold. No Dagster. No Type 06. No repair of **173.44**.

Truths (may be a thin gold callout, not a second slide):

- You did not need to *be* a Java engineer.
- The agent is a seat. **Bind is the law.** The eval is the judge. The
  mesh is how signed leaves run.

### HUD 27 — Research

```text
data-act-name="Research" data-accent="cyan"
```

Clone Recap · papers glass (three articles, not flat `.card` posters). Tag:
`Close · run/d2/12 · query, then walk`.

The room does not re-read. It **queries**. Same notebook. Do not rebuild.

Three cards, verbatim from [`12-research.md`](../../run/d2/12-research.md):

| n | Tool | Ask |
|---|---|---|
| 1 | OntoLayer | What grain and keys must dlt register, and what is the grain of `reporting.card_settlement_reconciliation`? |
| 2 | Second Brain | From the sources only — architecture / independence meeting: what does the new plant write after the independent parser (**Parquet vs SFTP CSV**)? Must it call Java? **Cite the page.** |
| 3 | `plans/modern.md` | Read the golden-match **two questions**. Day 3 attaches them. Do not rewrite the referee. |

The two questions (may sit as a quiet footnote, exact from the plan):

1. Legacy parity — did modern reach the same observable outcome as legacy?
2. Business correctness — did modern satisfy the approved contract?

Look up: citations, not guesses. Grain named. First write = **Parquet,
not SFTP**. Two golden-match questions restated.

Do not: invent the lakehouse to close the Night. No citation → re-ask,
or mark it open for Day 3.

### HUD 28 — Next

```text
data-act-name="Next" data-accent="gold"
```

**No morning / afternoon.** One Night, then Constructor tomorrow.

Homework (four, from the agenda — short cards or a numbered list):

1. Re-read the signed brief, the ADRs, and the seam list. Restate them
   with the file closed.
2. The Task-Spec leaf still has an eval. `signed_off` is still **false**.
3. Skim Types `02`–`04` inbound **layouts only** (brain packs 04–06).
   Do not start Type `05`.
4. The golden-match two questions stay in `plans/modern.md`. Attach when
   landing exists. Do not rewrite the referee.

One line: tomorrow the constructor **registers** landing **only if those
files exist**. dlt does not re-parse. dlt does not invent Parquet.

### HUD 29 — Tomorrow (silent)

```text
data-act-name="Tomorrow" data-accent="cyan"
class="slide slide--silent"
```

Clone Why-a-file cinematic stack plus `.slide--silent` (`.rtw-ghost`,
display type, few words). **Do not** clone Day 1 copy (“Tomorrow, you
translate” / “First write”).

- Ghost: `TOMORROW`
- Tag: `Day 3 · the constructor seat`
- Display: `Tomorrow, you` / `register.` (or `construct.` — one verb)
- Body, one sentence: Constructor · dlt → Gold **only if** landing Parquet
  exists. **dlt does not re-parse.** Type 06 stays sealed.
- Steps (if you keep `.tom-step`): `landing?` → `dlt` → `Gold` →
  `golden-match attach` — not `First write` as tonight’s leftover.

No staff path. Lights down. They walk.

---

## Hard bans

- Morning / afternoon.
- Day 1 Debrief extras (Two Plants, Receipts, Three Truths as extra slides).
- Hands-On badge / board E.
- `modern/` required / factory Loop as tonight’s proof.
- “Tomorrow you write Parquet” / “Tomorrow you translate.”
- Type 06. Port Java. Repair **173.44**.
- Rebuild the notebook.
- Copy old `d2-translator.html` Debrief.
- Day 1 purple Tomorrow / extra Receipts slides. In hand = Recap `.req`. Tomorrow = Why-a-file cinematic.
- Staff paths that do not exist.

## Done when

- Five DEBRIEF slides after DIG. Silent class on Tomorrow only.
- Research cards match `run/d2/12` three queries.
- In hand does not claim Parquet on disk.
- Tomorrow is Constructor, not a second Translator night.
- Keyboard walks the full deck without a JS error.

## Next move

None. The prompt pack is complete. Build slides in order: clean Stage
→ Craft → Floor → Dig → Debrief. Staff `run/d2/` is already signed.
