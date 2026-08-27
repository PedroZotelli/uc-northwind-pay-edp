# ebook-converge build protocol

Every builder agent MUST follow this protocol exactly. Read it fully before writing any HTML.

## Product

We are rebuilding `ebooks/prt-converge.html` (a page-per-slide HTML document) that is screenshotted
into `ebooks/ebook-converge.pdf` (1440×900 pt pages). The design model is `ebooks/prt-task-spec.html`
(dark austere editorial deck system). The result must look like the same product family, with the
accent identity adapted to Converge (violet), per the palette semantics below.

## Workspace layout

- `ebooks/.build/src/head.html` — doctype, meta, fonts, ALL CSS, mermaid boot script. Owned by the
  foundation agent; later agents may APPEND new component CSS in their own fragment's <style> block
  only if a needed component is missing (document additions in `components.md`).
- `ebooks/.build/src/front.html`, `act-1.html` … `act-7.html`, `back.html` — slide fragments.
- `ebooks/.build/src/tail.html` — speaker-notes/JS-free closing, `</body></html>`.
- `ebooks/.build/tools/build.sh` — concatenates head + front + act-1..7 + back + tail into
  `ebooks/prt-converge.html`, INLINING `mermaid.min.js` (replace the `<script src="...">` tag with
  the file contents) so the final HTML is self-contained like the model.
- `ebooks/.build/tools/shoot.js` — node + puppeteer-core (Chrome at
  `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`): viewport 1440×900,
  deviceScaleFactor 1.5, screenshots each `section.slide` to `ebooks/.build/shots/pNNN.jpg`
  (jpeg quality 88), waiting for fonts + mermaid renders; collects console errors, mermaid errors,
  and per-slide overflow (scrollWidth/scrollHeight vs client box) into `ebooks/.build/shots/report.json`.
- `ebooks/.build/tools/assemble.py` — img2pdf → `ebooks/ebook-converge.pdf` with dpi=108 so pages
  are exactly 1440×900 pt.
- `ebooks/.build/components.md` — component API reference (foundation agent writes it; builders use it).
- `ebooks/.build/assets/` — converge-icon.svg (copied from `assets/converge-icon.svg`), mermaid.min.js.

## Slide anatomy (every page)

```html
<section class="slide" data-act="ACT LABEL" data-act-name="Page name" data-accent="purple" id="p08">
  <div class="wrap">
    <header class="shead">…kicker / HUD…</header>
    <h2 class="h2">Headline that is a CLAIM, not a topic</h2>
    <p class="lede">…one-sentence core line…</p>
    …primary visual + at most one compact callout…
    <footer class="sfoot">source labels [A]/[I]/[T] + proof token + page number</footer>
  </div>
  <aside class="speaker-notes">exact paths, versions, hashes, caveats</aside>
</section>
```

- `.slide` is exactly 1440×900 px, `overflow:hidden`, padding from the kit, dark background.
- Pages are STATIC: everything visible on load, no IntersectionObserver reveals, no scroll-snap JS,
  no animations that leave content hidden. (Decorative CSS is fine; content must not depend on JS.)
- Every page footer carries its source labels and proof token; every green claim needs its named
  gate/receipt/test token nearby; every red claim states the refusal + the safe next action.
- Headline is a claim sentence. Keep body copy 18–34 words per card. 3 cards preferred, 4 for real
  four-state distinctions, 8 only for the terminal-state matrix (P49).

## Design tokens (adapted kit)

Base kit tokens from the task-spec model stay (bg #070A0F, surfaces, borders, text #F5F2EA, dim
#8f969f, mute #59616d, fonts: 'Instrument Serif' display, 'Newsreader' editorial, 'DM Sans' body,
'Fira Code' mono, 'Space Grotesk' for labels). Converge identity overrides:

- `--accent`/brand = violet `#A78BFA` (grad-violet replaces grad-gold for brand moments).
- `--gold: #F3B64C` is RESERVED for human authority (reviewer, key holder, barrier). Never decorative.
- `--cyan: #68C7FF` = Seamwise/TaskPlan/lineage. `--green: #3DDC97` = verified/accepted/settled.
- `--red` = refused/stale/tamper. `--silver: #CBD3DA` / warm gray = observer/read-only surfaces.
- Dotted/dashed connectors = optional or non-authoritative observation only.
- Aurora/atmospheric background tints: violet + cyan (NOT gold).

## Diagrams

1. CANONICAL mermaids from the brief get rendered with mermaid.js (vendored `mermaid.min.js`):
   §1 authority chain (P02), §4 master transition (P07), library C compose state machine (P26),
   library D binding fences (optional on P38), library E loop kernel (P48), library F receipt chain
   (P54), library G observation boundary (P61), library A authority-without-duplication (P71).
   - Embed as `<pre class="mermaid">` with the EXACT diagram source from the brief (you may adjust
     only line breaks inside node labels and the classDef colors to match the palette).
   - Mermaid config: `startOnLoad:true`, `securityLevel:'loose'`, dark theme with themeVariables
     matched to the palette (bg transparent, primaryColor #18152a, primaryBorderColor #A78BFA,
     primaryTextColor #F5F2EA, lineColor #8f969f, fontFamily Fira Code).
   - The shoot harness fails the build if any `.mermaid` element contains render-error output or
     `window.__mermaidErrors` is non-empty (head.html must collect them).
2. DESIGNED diagrams (flows, rails, gates, fences, cards, balances, matrices) are hand-built
   HTML/CSS components like the task-spec model — never paste raw mermaid when a designed diagram
   communicates better. Reuse/extend the kit's component classes (documented in components.md).
3. Code specimens use the macOS code-window component (`mac-bar`, `mac-dot` trio, mono font,
   8–18 visible lines, syntax tint classes).

## Truth rules (violations are defects)

- Facts/numbers/tokens/hashes must match the page plan and brief EXACTLY (e.g. 57 committed forms /
  60 checkout; `58b1ddb`; `3de9f0b`; 42 commits; 145/145; `dispatch_authorized: false`).
- Never show Cockpit/Ask/tracker/`cvg next` writing into canonical state; observation = dotted.
- `LOCAL_SETTLED` when external writes denied; `SETTLED` only for permitted publication.
- Guided chat and 60-form CLI content always carry a visible `W · CHECKOUT ONLY` mark.
- Never say `make check` is green; the layout failure appears in the main narrative (P04, P68).
- HMAC = tamper evidence under a shared key; never identity/secrecy/isolation.
- Task-Spec compatibility is `3.8.x` everywhere.
- Failure tokens and exit codes stay exact: BLOCKED/STALLED/EXHAUSTED/CANCELLED exit 1;
  SETTLED/LOCAL_SETTLED/NO_OP exit 0; ERROR is a nonzero safe failure.

## Self-check before finishing your fragment

1. Run `bash ebooks/.build/tools/build.sh` (after foundation exists) and confirm it assembles.
2. Run `node ebooks/.build/tools/shoot.js --only <your-page-ids>` and open the report: zero console
   errors, zero mermaid errors, zero overflow flags on your pages.
3. Visually inspect 2–3 of your own pages (`shots/pNNN.jpg`) for collisions, clipping, orphan text.
4. Your fragment must contain ONLY `<section class="slide">` blocks (+ optional scoped `<style>`).
   No <html>/<head>/<body> tags in fragments.
