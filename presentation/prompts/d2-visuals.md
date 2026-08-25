# Night 2 visual system

**Source of truth:** the live file
[`../d2-translator-java2py.html`](../d2-translator-java2py.html)
(Opening + Stage). Later moves **append** into that file and must look
like they were designed the same night.

Do **not** restyle `:root`, HUD, tracker, or `<script>`. Do **not** copy
the `<style>` block again. Reuse classes already in the stylesheet.
Day 1 [`d1-archaeologist.html`](../d1-archaeologist.html) is chrome
inheritance only — do not clone its purple story slides, two-column
does/does-not posters, or four-logo install boards as the look.

If a later slide looks flatter, greyer, or more “card grid from a
template” than Recap · papers / SWE Role / java2py, it failed.

---

## Atmosphere (every cinematic slide)

Stack, in this order, inside `<section class="slide">`:

1. `.hands-bg` — plant still from `../assets/` (`df-legacy-opt.jpg`,
   `df-gates-opt.jpg`, `df-hero-opt.jpg`, `d0-night-drop.jpg`).
   `transform:scale(1.08–1.22)`, `opacity:0.22–0.28`,
   `filter:saturate(0.6–0.8)`. Opening adds `hue-rotate(160deg)` (cyan
   night). Do not default a purple hero.
2. Absolute overlay `z-index:1` — `linear-gradient(180deg, rgba(8,8,10,0.9)…)`
   plus one or two `radial-gradient`s in the slide accent (cyan / gold /
   green / red). Why-a-file is **left-weighted** `linear-gradient(90deg, …0.97, …0.4)`.
3. `.aurora.aurora--{accent}` at `z-index:1` with `<b></b>`.
4. `.reveal` at `z-index:2`, `max-width:1680px–1780px`, `margin:0 auto`.

Dividers may skip the photo and keep aurora + reveal only (Stage divider).

---

## Type (do not invent a scale)

| Role | Class / font | Notes |
|---|---|---|
| Kick | `.tag` `--tag-c:var(--accent)` | mono, uppercase, letter-spacing |
| Title | `.h2` Instrument Serif | one word in `color:var(--x)` **or** `.gradient-cyan` / `.gradient-gold` / `.gradient-green` / `.gradient-red` |
| Lede | `.lede` Newsreader | 54–82ch. `<b>` lifts to `--text`. Paths in Fira Code |
| Display | `.slide__display` | Opening / silent only |
| Kicker | Fira Code, 8.5–10px, letter-spacing 2.4–2.6px, uppercase, `--text-mute` | above grids and footer strips |
| Proof | `.req-proof` / editorial italic on a `border-top:1px solid var(--rule)` | Recap closed footer |

One idea per slide. Vary composition — three centered title-only slides
in a row is a smell. The live Stage already alternates: receipts grid →
glass documents → trait grid + seat card → giant wordmark → SVG lanes →
cinematic copy → pipe.

---

## Glass (the Night 2 signature)

Recap · papers, SWE Role tiles, java2py three-split, seat card. **Reuse
this recipe**; do not invent a new card language.

```text
border-radius: 18px (tiles) or 24px (hero panel / seat card)
background: linear-gradient(160deg,
  color-mix(in srgb, var(--X) 13%, transparent),
  rgba(17,17,20,0.70) 42%,
  rgba(8,8,10,0.86))
border: 1px solid color-mix(in srgb, var(--X) 32%, transparent)
box-shadow:
  inset 0 1px 0 rgba(255,255,255,0.07),
  0 30px 60px -36px rgba(0,0,0,0.9),
  0 0 50px -30px var(--X)          /* 90–100px on hero panels */
backdrop-filter: blur(12px)         /* 16px on hero panels */
-webkit-backdrop-filter: same
```

Hairline at top of panel:

```text
height: 2px
background: linear-gradient(90deg, transparent, var(--X) 35%, var(--X) 65%, transparent)
```

Watermark (hero panels only): `.act-num` absolute, `font-size:clamp(140px,13vw,250px)`,
`opacity:0.30–0.36`, `letter-spacing:-8px`, accent color.

Number chip (SWE tiles): 30×30px, `border-radius:9px`, mono 12px weight 800,
`color:#000`, `background:var(--X)`, `box-shadow:0 0 18px color-mix(…55%)`.

Path pill: mono, `border-radius:999px`, `padding:5px 12px`,
`border:1px solid rgba(255,255,255,0.12)`, `background:rgba(0,0,0,0.4)`.

Rubber stamp (closed papers): `transform:rotate(-4deg)`, green 2px border,
inset double ring, `closed · do not rerun`. Do not stamp “open” work.

Quote rail: `padding-left` + `border-left:2px solid` accent, Newsreader.

---

## Other live patterns (reuse, don’t restyle)

| Pattern | Live slide `data-act-name` | Classes |
|---|---|---|
| Move divider | `Stage` | `.cols` 1.05fr/0.95fr · `.act-num` · `.h2` · `.lede` · tag chips · `.wkrail` (`wkr--done` / `wkr--now`) |
| Six receipts | `Recap · closed` | `.three-col` · `.req` · `.req-idx` / `name` / `note` / `proof` · rule footer |
| Dual glass docs | `Recap · papers` | two `<article>` glass + watermark 0/1 + path pill + stamp |
| Trait grid + seat | `SWE Role` | 2×3 glass tiles + 24px seat `aside` with kv rows |
| Giant wordmark | `java2py` | mono `clamp(84px,9.6vw,160px)` + three glass splits |
| Two-lane SVG | `First write` | `.arch` · rx 14–16 nodes · Fira kicker · Instrument title · outer glow stroke 5 · `.rulequote` |
| Cinematic copy | `Why a file` | left copy + night photo + `.contract` `.ct` three cells |
| Pipe | `Five-file package` | `.d2-pipe` `.d2-pipe-node` `.d2-pipe-arrow` `.d2-pipe-out` · `.d2-sound` |
| Job four | `The translator` | `.d2-job4` · `.card` · `.d2-forbid` (do **not** keep this extra slide) |
| Ledger + rails | `Q&A · impressions` | `.ledger` · quote rails · waveform strip (extra — don’t clone unless asked) |
| Opening contract | `Translator` | `.title-foot` `.contract` `.pullquote` `.ts-spine` |
| Hands-On chrome | Day 1 classes already in file | `.hs-head` `.hs-chip` `.hs-range` `.hs-run` `.hs-board` `.hands-on` · tiles as `.req` **or** glass, not four vendor logos |
| Look-up | Recap footer / Day 1 | `.slice-lookup` `.callout.green` + `.callout.red` |
| Terminal | in CSS | `.mac` `.mac-bar` `.mac-dots` `.mac-body` |
| Silent close | Day 1 class in file | `.slide--silent` `.rtw-ghost` `.tom-step` `.tom-step.hot` · plant photo stack |

---

## Per-move clone map (builder)

Identify slides by `data-act-name`. Clone **structure**, write **new copy**.

### Craft (HUD 11–14)

| Slide | Clone | Why |
|---|---|---|
| Craft divider | `Stage` divider, gold | same `wkrail`, `act-num` **02**, three beats on the right |
| Agent Harness | `SWE Role` | 2×2 glass tiles (Workspace / Tools / Spawn / Shell) + seat card “the machine” (house stack as kv rows). Do not put vendor logos as the story. |
| Bind is rails | `Recap · papers` | two glass articles: **Not a fence** (silver/red) vs **Fence** (red). Watermarks optional. Frozen paths as pills. Footer `.d2-forbid` or red tags. |
| Hands-On A | Recap closed receipts + `.hs-head` | chip `board a · fence` · `run/d2/` · **04**. One `.mac` with the PWNED prompt. Look-up green/red. Badge `span.hands-on`. |

### Floor (HUD 15–18)

| Slide | Clone | Why |
|---|---|---|
| Floor divider | `Stage` divider, green | `act-num` **03** |
| Second Brain | `SWE Role` tiles **or** Recap closed `.req` | five J-asks as numbered glass (J1–J5). No unzip/new-notebook UI. NotebookLM icon only as a quiet mark, not a hero. |
| OntoLayer + specs | `Recap · papers` dual glass | left: specs (five-file, nots, judge). right: graph without→with. Gold callout for paid table. Optional `.d5r-split` if a map helps — do not grep SQL as the picture. |
| Hands-On B | Recap receipts + `.hs-head` | two columns (brain / graph), chip **05–06**, look-up Marina + grain. |

### Dig (HUD 19–24)

| Slide | Clone | Why |
|---|---|---|
| Dig divider | `Stage` divider, gold | `act-num` **04** |
| Converge + Seamwise | Opening `.ts-spine` **or** `.d2-pipe` | passes as a spine: 0–1 dim, **2–4 on**, 5 next, 6–8 off. Not a bullet list. |
| Hands-On C | Recap `.req` ×3 + `.hs-head` | `.hs-board.hs-3` · chip **08–10** · look-up **signed**. |
| Task-Spec | SWE seat card + one glass | leaf anatomy (eval, `signed_off` false, `docs/tasks/`). |
| Hands-On D | one glass + `.mac` path | chip **11**. Dark if unsigned. |
| Task-Mesh | `First write` SVG **or** `.d2-pipe` | attempt → eval → retry/settle. Show only. No Hands-On badge. |

### Debrief (HUD 25–29)

| Slide | Clone | Why |
|---|---|---|
| Debrief divider | `Stage` divider, gold | Translator `wkr--done`, Constructor `wkr--now` |
| In hand | `Recap · closed` six `.req` | receipts of what they hold, not a speech |
| Research | three glass articles (papers scale) | beat 12 queries + `.slice-lookup` |
| Next | `SWE Role` 2×2 glass | four homework tiles. **No** morning/afternoon. |
| Tomorrow | `Why a file` cinematic + `.slide--silent` | plant photo, `.rtw-ghost`, Constructor verb, `.tom-step` ending on dlt/Gold **if landing exists** |

---

## Hard visual bans

- Restyle tokens, HUD, or script.
- Clone Day 1 purple Opening / “does vs does not” two-column poster as the SWE slide (live SWE is glass + seat card).
- Vendor-logo Hands-On (Oh My Pi / OpenRouter tiles) on Night 2 boards.
- Flat `#111114` boxes with no hairline, no blur, no accent glow — that is the old discarded HUD.
- Copy layouts from [`../d2-translator.html`](../d2-translator.html) except the pipe/job4 **classes already imported**.
- Centered title-only slides.
- Overflow: if a slide needs a scroll on a 1080p projector, cut copy, don’t shrink type below the scale above.
- Fake screenshots, fake CI badges, nets other than **173.45** / **173.44**.
