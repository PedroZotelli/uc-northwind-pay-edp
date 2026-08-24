# Presentation

The decks are self-contained HTML files. Open one in a browser and press `F11`.
No build step, no server — the only external fetch is Google Fonts.

Scope is [`agenda/`](../agenda/README.md). Staff execute is [`run/`](../run/README.md).
The engagement map is [`plans/`](../plans/README.md).

| Deck | Brief | Slides | File |
|---|---|---|---|
| Day 1 · Onboard + Archaeologist | [`agenda/d1.md`](../agenda/d1.md) | 44 | [d1-archaeologist.html](d1-archaeologist.html) — **live**. Staff: [`run/d1/`](../run/d1/README.md) |
| Day 2 · Translator | [`agenda/d2.md`](../agenda/d2.md) | 14 | [d2-translator.html](d2-translator.html) — file exists; **not** signed off as follow-along |
| Days 3–5 | [`agenda/d3.md`](../agenda/d3.md)–[`d5.md`](../agenda/d5.md) | — | not built yet |
| Dark Factory workshop | — | 82 | [wrkp-dark-factory.html](wrkp-dark-factory.html) |
| Agentic engineering (YouTube) | — | 44 | [yt-agentic-engineering.html](yt-agentic-engineering.html) |

Day 1 is Capture + Intent only. Structure (ADRs) is the first act of Day 2.
Type `06` is not in `spec/` until Friday. Do not invent a Pass the brief did
not authorize.

## Day 1 · how the deck is laid out

One file, **44 slides, six blocks**. The block name shows in the HUD pill
bottom-right, and it only changes at a block boundary.

| Block | Slides | Mode |
|---|---|---|
| Opening | 1 | title — the two seats, the contract |
| Stage | 7 | presentation, keyboards down |
| Craft | 6 | teaching + Hands-On A (01–04) |
| Floor | 9 | teaching, Hands-On B (05–09), MATCHED look-up |
| Dig | 14 | roles, estate, Show then Hands-On C–F (10–16) |
| Debrief | 7 | truths, receipts, Research (17), Next, silent Tomorrow |

Every block opens with a divider slide. HUD `01`–`44`.

### Hands-On vs Show

Six Hands-On boards only (slices A–F). Show slides teach; they do not wear
the Hands On badge. Dig sandwiches:

| HUD | Show | Then Hands-On |
|---|---|---|
| 32 → 33 | Second Brain (nine packs, whole drop) | Execute 12 |
| 34 → 35 | OntoLayer · the map | Execute 13 (`ontology-ask-sql` then `ontology-ask`) |
| 36 → 37 | Converge · the spine (0–1 tonight) | Execute 14–16 |

Brain handout: [`brain/notebooklm/northwind-pay-brain.zip`](../brain/notebooklm/northwind-pay-brain.zip).
Unzip, upload the **nine** `.md` files — not the zip. Days 2–5 query this
same notebook. Type `06` is not in it.

Close is not a seventh Hands-On: Research (42) → Next (43) → silent Tomorrow (44).

Staff clock: [`run/d1/README.md`](../run/d1/README.md) — slices A–F, then 17.

## Driving it

| Key | Does |
|---|---|
| `→` `↓` `Space` `PageDown` | next slide |
| `←` `↑` `PageUp` | previous |
| `Home` / `End` | first / last |

Dots on the right edge are clickable. The bar across the top is scroll
progress. Slides snap, so a trackpad flick moves exactly one.

## House rules for editing

- **One file per deck.** Styles, markup and script live together — no imports.
- **Every number is traceable.** Amounts, byte offsets and verdicts come from
  `contracts/`, `spec/` or `evidence/`. If it is on a slide, it is in the repo.
- **Hands-On is one mold.** Six boards only (slices A–F). Clone Execute 01–04:
  chip, `run/d1/` path, `.req` beat tiles, look-up / do not. Show slides teach;
  they do not invent a local “beat 01”. Point at `run/d1/NN`, not a leftover
  Floor “beat 03”.
- **Each Show slide shows its information differently.** Flow, annotated artifact,
  diff, matrix, gauges — repeating a mechanism is a smell. The Hands-On boards
  are the exception: they must look the same.
- **Namespace new components.** Two decks merged into this one already collided
  on `.mac`; the second set became `.cmac`. Check before adding a class.
- **Cut HTML blocks by their own closing tag,** not the next `</div>`. Getting
  this wrong once pushed 5 slides outside `.deck` and the counter read `02`.

Images and logos live in [`../assets/`](../assets/) — the Day 1 deck uses 35 of them.
