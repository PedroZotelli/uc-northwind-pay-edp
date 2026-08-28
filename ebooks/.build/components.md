# CONVERGE ebook — component API reference

For the fragment-builder agents writing `src/act-1.html` … `src/act-7.html`, `src/back.html`.
All CSS lives in `src/head.html`. Fragments contain ONLY `<section class="slide">` blocks plus an
optional scoped `<style>` block (document anything you add here). No `<html>/<head>/<body>` tags.
Demonstration pages: **P01–P07** in `src/front.html` (shots at `.build/shots/p001.jpg` … `p007.jpg`).

## Hard rules (violations are defects)

- Facts, numbers, tokens, hashes verbatim from `page-plan.md` / `brf-converge.md`.
- **Gold `#F3B64C` = human authority ONLY** (reviewer, key holder, Pass 4 barrier, explicit risk).
  Never decorative, never brand. `aurora--gold` only on human-authority pages.
- Violet `#A78BFA` = Converge brand/sequencing/contracts (default accent).
  Cyan `#68C7FF` = Seamwise / TaskPlan / lineage / decomposition.
  Green `#3DDC97` = verified / accepted / settled — always with a named gate/receipt/test token nearby.
  Red `#FF6B66` = refused / stale / tamper — always state refusal + safe next action.
  Silver `#CBD3DA` = observer / read-only (Cockpit, W marks). Never use gold for observers.
- **Dotted/dashed = optional/opt-in route or non-authoritative observation only.** Never draw
  Cockpit/Ask/model/tracker arrows writing into canonical state.
- Guided chat and 60-form CLI content always carries a visible `W · CHECKOUT ONLY` mark (`.wribbon`).
- Never say `make check` is green; the layout failure is in the main narrative (P04, P68).
- Task-Spec compatibility is `3.8.x` everywhere. HMAC = tamper evidence under a shared key only.
- Terminal tokens stay exact: SETTLED/LOCAL_SETTLED/NO_OP exit 0; BLOCKED/STALLED/EXHAUSTED/CANCELLED
  exit 1; ERROR nonzero safe failure.

## Slide anatomy (every page, required)

```html
<section class="slide" id="p08" data-act="ACT LABEL" data-act-name="Page name" data-accent="violet">
  <div class="aurora" aria-hidden="true"><b></b></div>
  <div class="wrap top">
    <header class="shead">
      <span class="actcap">ACT LABEL</span>
      <span class="actname">Page name</span>
      <span class="spacer"></span>
      <span class="wordmark"><svg width="13" height="13" viewBox="0 0 1024 1024" aria-hidden="true"><path d="M512 72 L832 256 L832 332 L714 400 L714 338 L512 222 L310 338 L310 570 L512 686 L714 570 L714 510 L832 442 L832 652 L512 836 L192 652 L192 256 Z" fill="#A78BFA"/></svg>CONVERGE · 0.2.0</span>
    </header>
    <h2 class="h2">Headline that is a CLAIM, not a topic</h2>
    <p class="lede">One-sentence core line.</p>
    …primary visual + at most one compact callout…
    <footer class="sfoot">
      <span class="src"><b>[A]</b> path/one · <b>[T]</b> path/two</span>
      <span class="proof">GATE_TOKEN=VALUE</span>
      <span class="pgno">P<b>08</b> / 83</span>
    </footer>
  </div>
  <aside class="speaker-notes">exact paths, versions, hashes, caveats</aside>
</section>
```

- `.slide` is exactly 1440×900, `overflow:hidden`. `data-accent` sets `--ac` for the whole page:
  `violet` (default), `cyan`, `gold`, `green`, `red`, `silver`.
- `.wrap` = flex column, vertically centered. `.wrap.top` pins content to the top — use for dense
  pages. To distribute leftover space evenly, wrap the middle visuals in
  `<div style="flex:1;display:flex;flex-direction:column;justify-content:space-evenly;">` (see P02, P07)
  or `justify-content:center` (P03, P05, P06).
- Build check: `node tools/shoot.js --only pNN` fails on console errors, mermaid errors, and any
  element whose bounding box escapes the slide (±2px). Keep absolutely-positioned decorations INSIDE
  the slide box — see "Decorative containment" below.

## Page chrome

- `.shead` — HUD header row: `.actcap` (accent mono label + dash), `.actname` (muted), `.spacer`,
  `.wordmark` (mono, carries the inline fold SVG). Demo: every page.
- `.sfoot` — footer, `margin-top:auto` pins it to the bottom. Children: `.src` (source labels,
  `[A]/[C]/[I]/[T]/[E]/[R]/[D]/[W]` in `<b>`), `.proof` (proof-token pill; variants `.proof.gold`,
  `.green`, `.red`, `.cyan` — violet default), `.pgno` (`P<b>NN</b> / 83`). Demo: P01–P07.
- `.speaker-notes` — hidden in print (`display:none`); carries exact paths/versions/hashes.

## Type primitives

- `.h2` — claim headline, Instrument Serif 46px. `.h2.sm` = 38px (dense pages). `.h2 .thin` dims a
  clause. Demo: P02–P07.
- `.lede` — Newsreader 17px one-sentence core line; `<b>` brightens, `<code>` cyan-mono chip. Demo: all.
- `.kick` — accent kicker line above a headline (alt to `.shead` patterns). `.eyebrow` — small mono
  section label for sub-blocks (demo: P04, P06). `.note` — italic editorial aside (demo: P01).
- `.display` — display serif base (cover wordmark). `.fm-hero` — 128px cover hero (demo: P01).
- Gradient words: `.grad-violet` (brand moments), `.grad-cyan`, `.grad-green`, `.grad-gold`
  (HUMAN AUTHORITY pages only). Demo: P01 (`CONVERGE`).
- `.tag` — inline pill (`display:inline-flex; width:fit-content`, safe inside flex parents).
  Set `--tag-c` inline for color, default violet. Demo: P01. (Fixed in head.html — was stretching to
  full-width bar inside flex columns.)
- `.fm-rule` — 46px accent dash for hero pages. `.hair` — 1px rule.

## Atmosphere (decorative containment — read this)

- `.aurora` + `<b>` child — blurred ambient glow. Variants: default (violet), `.aurora--cyan`,
  `.aurora--green`, `.aurora--gold` (human-authority pages only), `.aurora--red` (refusal pages).
  Contained to the slide box (`inset:0; overflow:hidden`) — do NOT re-extend it; shoot.js flags
  escapees. Demo: all pages.
- `.grid-floor` — perspective grid on covers/dividers. Contained variant (60% base width flares to
  ~97% under perspective). Demo: P01.
- `.ghost` — giant italic watermark word, `opacity:0.03`, whitelisted in the escapee check but its
  glyph INK still counts toward `scrollHeight`: keep it fully inside the slide and ≥70px above the
  bottom edge at large sizes (P01 uses `font-size:300px; left:20px; bottom:74px`).

## Layout helpers

- `.cols` — 2-col grid; variants `.cols.c2w` (1.25fr 1fr), `.cols.c2l`, `.cols.c3`, or set
  `--cols` inline (demo: P04 `--cols:0.92fr 1.08fr`). `.stack` — vertical flex stack, gap 14.
- `.cards.c2/.c3/.c4` + `.card` — standard card grid; `.card` children: `.ck` (kicker), `.ct`
  (title), `.cb` (body, 18–34 words), `.big` (big number). Accent variants `.acc-violet/.acc-cyan/
  .acc-gold/.acc-green/.acc-red/.acc-silver` set kicker color + border. 3 cards preferred, 4 for real
  four-state distinctions.
- `.three-col` + `.req` tiles — rim-lit recap cards: `.req-inner` > `.req-idx`, `.req-name`,
  `.req-note`, `.req-proof`; color via `.req.red/.violet/.gold/.green` or `--rq-c`.
- `.rmgrid` + `.rmcard` — numbered instrument cards: `.rm-head` > `.rm-num` + (`.rm-eyebrow`,
  `.rm-name`), `.rm-when`, `.rm-foot` > `.rm-pill`; color via `--rmc`, pill via `--rmp`.
- `.panel` — bordered info panel; `.panel-k` kicker (color via `--pk`), `.pf` fact rows
  (`.pf-l` mono label, `.pf-r` italic value). Demo: P05, P06.
- `.invariant` — 3-cell strip: `.inv-cell` > `.inv-verb` (big serif, color `--ivc`), `.inv-who`,
  `.inv-gloss`.

## Lists, tokens, tables

- `ul.tick` — dash-marker list; `ul.tick.check` = green ✓ (may-make claims), `ul.tick.cross` = red ✕
  (refusals), `ul.tick.dense` = 10.5px. Demo: P05, P06.
- `.tok` — mono proof chip; variants `.tok.violet/.gold/.green/.red/.cyan/.silver`. `.tokset` = flex
  wrap row. Demo: P01, P05.
- `.tbl` — table; `th` accent underlined, `td:first-child` bright, `.num` right-aligned mono,
  `tr.hl` violet highlight row, `tr.redline` red row, `.tbl.dense` for audit/reference pages.
  ≤6 rows on narrative pages; dense banks allowed on reference pages (P04, P72–P75). `.sw` = inline
  color swatch (demo: P06).

## Callouts

- `.callout` — tinted box: `.co-k` kicker + `.co-b` editorial body. Variants `.green`, `.red`,
  `.gold` (human authority), `.cyan`. One compact callout per page max.
- `.trap` — RED load-bearing refusal box: `.trap-k` kicker, `.trap-h` serif head (with `<em>` red),
  `.trap-b` body. Use for aggregate-gate failures and never-claim traps. Demo: P04.

## Pull quote

- `.pullquote` — accent left border; `.pq-text` (34px serif, scale inline), `.pq-attr` attribution
  row: `.pq-dash`, `.pq-who`, `.pq-sep` (◆), `.pq-gloss`. Set `--pq-c` inline (violet default).
  Demo: P02.

## Code: macOS window

- `.code` — mono block, `white-space:pre`, `data-lang="bash"` adds a language tab (color `--lang-c`).
  `.code--mac` + `.mac-bar` (`.mac-dot--r/y/g` trio + `.mac-title`) = macOS window. 8–18 visible
  lines. Syntax tints: `.c` comment, `.k` keyword violet, `.s` string gold (human-authored literal),
  `.n` number/contract cyan, `.g` verified green, `.r` failure red, `.hl` highlighted line,
  `.cb` block line. Demo: P06.

## Flows and chains

- `.flow` — vertical chain: `.fl-node` (color `--fc`) > `.fl-k`, `.fl-name`, `.fl-note`; `.fl-arrow`
  connector between nodes (gradient `--fa`→`--fb`); `.fl-arrow.opt` = dashed OPTIONAL connector.
- `.hflow` — horizontal chain: `.hf-node` (color `--hc`, variants `.is-empty` dashed placeholder,
  `.is-gate` glowing gate) > `.hf-head` (`.hf-num` + `.hf-k`/`.hf-name`), `.hf-note`, `.hf-tag` pill;
  `.hf-arrow` between nodes with `.hf-al` italic label + `.hf-line`; `.hf-arrow.opt` = DOTTED
  optional/observation connector. This is the primary "passes / pipeline" component.
- `.flowchain` — simple chip chain (cover rail, contract fold): `.fc-node` (color `--fcc`) +
  `.fc-arrow`. Demo: P01 (`intent → topology → contract → execution → evidence`), P06
  (`compose → seal → bind → loop → accept`).

## Converge book components

- **Evidence ladder** `.ladder` > `.lrow` (grid: rank | badge | surface | use): `.lrow.head` header,
  `.lr-rank` number, `.lr-badge` letter chip (`.rk`) + name, `.lr-surf` mono paths, `.lr-use`
  editorial rule. Row color via `--rc` + class `top`; `.lrow.future` dims the F row. Demo: P03 (all
  9 ranks; W row carries `.wribbon`, F row = future).
- **W ribbon** `.wribbon` — `W · CHECKOUT ONLY` dashed silver ribbon, MANDATORY on any working-tree /
  guided-chat / 60-form CLI claim. `.wribbon.big` for page-dominant warnings (P56). Demo: P03, P04.
- **Receipt stack** `.rstack` > `.rcpt` (auto-staggered left margin, up to 6): `.rc-k` kind,
  `.rc-v` verb + `<small>` gloss, `.rc-q` qualifier; color per receipt via `--rc2` (gold = human
  review record, violet = composition/runtime, cyan = HMAC/Task-Spec, green = acceptance/settlement).
  Demo: P06 (3 shown); P13 and P54 use the full six.
- **Descent rail** `.drail` > `.drail-row` > `.dnode` ×9 (passes 0–8): `.dn-num`, `.dn-name`,
  `.dn-sub`. Classes: `.human` (cyan, passes 0–4), `.machine` (violet, 5–8), `.opt` (dashed border —
  optional hops 0 and 6), `.gate` (GOLD Pass 4 barrier, auto "⛨ BARRIER · HUMAN" label).
  `.darc` = dotted bypass arc ABOVE the rail (set `left`/`width` inline, `<span>` label) — the only
  correct way to show skipping an optional hop. `.drail-legend` with `.lg` swatches
  (`.lg.dashed` for the bypass key). Full-size demo on P14; mini variant `.drail.mini` on P06
  (scoped in front.html — copy that block if you need a compact rail).
- **Terminal cards** `.term` — `.t-name`, `.t-gloss`, `.t-foot` (`.t-exit` exit-code pill + muted
  label); `.term.bad` red, `.term.warn` gold, `.term.neutral` silver (default green). 8-card matrix
  allowed ONLY on P49.
- **Corridor** `.corridor` > `.rail` — evidence corridor rows (release / main / working tree):
  `.rl-k` label + `<small>`, `.rl-v` mono value (`.dim`), `.rl-tag` right tag; color `--rlc`;
  `.rail.dotted` = non-authoritative/working-tree corridor. Owner: P66/P74.
- **Lanes** `.lanes` > `.lane` — everyday-vs-factory lanes: `.ln-k` kicker, color `--lnc`. Owner: P10.
- **Specimen** `.specimen` — glowing task-ID card: `.sp-id` (`T-20260815-health-status`), `.sp-sub`.
  Owner: P12 steel thread.
- **Beats** `.beats` > `.beat` ×7 — emotional arc strip: `.b-n` number, `.b-t` title (color `--bc`),
  `.b-g` gloss. Demo: P02 (Unease red → Separation cyan → Descent violet → Barrier GOLD →
  Bounded motion violet → Settlement green → Honesty silver).
- **Pin cards** `.pin-cards` > `.pin-card` (color `--pinc`) — requirement cards pinned to terrain:
  `.pinmark` (lettered dot), `.pin-t` title, `.pin-b` body. Owner: P20.
- **Stat** `.stat` > `.sv` big number (color `--sac`) + `.sk` mono label.

## Mermaid embeds (canonical diagrams only)

- Only the 8 canonical diagrams from the brief render as mermaid: §1 authority chain (P02 — demo),
  §4 master transition (P07 — demo), library C compose state machine (P26), D binding fences
  (optional P38), E loop kernel (P48), F receipt chain (P54), G observation boundary (P61),
  A authority-without-duplication (P71). Everything else is a DESIGNED HTML component.
- Embed EXACTLY:

```html
<div class="mmd frame" style="--mmd-h:280px;">
  <pre class="mermaid">
flowchart LR
    …exact source from the brief…
  </pre>
</div>
```

- Use the exact diagram source; you may adjust only line breaks inside node labels (`\n`) and
  classDef colors to the palette. Keep the brief's classDef blocks (they already match: human
  `#f3b64c`, engine `#68c7ff`, converge `#a78bfa`, proof `#3ddc97`).
- `--mmd-h` caps svg height; the svg always fills the frame width (fixed in head.html — mermaid
  emits `width:100%`, and `.mermaid` now has `width:100%` so flex centering can't collapse it to
  the 300px replaced-element default). Mermaid config: Fira Code 15px, `nodeSpacing:24,
  rankSpacing:36`, palette themeVariables, `securityLevel:'loose'`, errors collected into
  `window.__mermaidErrors` (shoot.js fails the build on any).
- Wide LR chains render small — that is expected for canonical diagrams (P02 ≈ 8px effective mono);
  do NOT "fix" by restructuring the diagram.

## Front-matter scoped additions (src/front.html `<style>` — copy if needed)

- `.fm-lockup` — cover lockup stack (`.lk-name` serif 34px, `.lk-sub` mono micro). Demo: P01.
- `.drail.mini` — compact descent rail overrides (44px arc clearance, 8.5px names, `⛨ BARRIER`
  gate label). Demo: P06.
- `.conn` / `.conn-line` (+`.dotted`) — connector-rule legend samples. Demo: P06.
- `.rv` — green mono validation result (`48/48`), `.rv.red`. Demo: P04.
- `#p03/.lrow`, `#p05/ul.tick.dense`, `#p07/.tbl` density tuning — page-scoped; do not globalize.

## Self-check before finishing your fragment

1. `bash ebooks/.build/tools/build.sh`
2. `node ebooks/.build/tools/shoot.js --only <your ids>` → report.json: zero console errors, zero
   mermaid errors, zero overflow entries on your pages.
3. Read your `shots/pNNN.jpg` and fix collisions, clipping, widows, off-palette accents.
4. Fragment = only `<section class="slide">` blocks (+ optional scoped `<style>`).
