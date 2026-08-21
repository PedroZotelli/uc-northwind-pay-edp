# Presentation

The decks are self-contained HTML files. Open one in a browser and press `F11`.
No build step, no server — the only external fetch is Google Fonts.

| Deck | Brief | Slides | File |
|---|---|---|---|
| Day 1 · Onboard + Archaeologist | [`agenda/d1.md`](../agenda/d1.md) | 37 | [d1-archaeologist.html](d1-archaeologist.html) |
| Dark Factory workshop | — | 82 | [wrkp-dark-factory.html](wrkp-dark-factory.html) |
| Agentic engineering (YouTube) | — | 44 | [yt-agentic-engineering.html](yt-agentic-engineering.html) |

Days 2–5 have no deck yet. Build them from [`agenda/`](../agenda/README.md).

## Day 1 · how the deck is laid out

One file, 37 slides, four blocks. The block name shows in the HUD pill
bottom-right, and it only changes at a block boundary.

| Block | Slides | Mode |
|---|---|---|
| Opening | 1 | title — the two seats, the contract |
| Stage | 6 | presentation, keyboards down |
| Craft | 8 | presentation + the two-minute agent demo |
| Floor | 13 | instructor demo, then students at keyboards |
| Debrief | 9 | close — exit criteria, homework |

Every block opens with a divider slide.

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
- **Each slide shows its information differently.** Flow, annotated artifact,
  diff, matrix, gauges — repeating a mechanism is a smell.
- **Namespace new components.** Two decks merged into this one already collided
  on `.mac`; the second set became `.cmac`. Check before adding a class.
- **Cut HTML blocks by their own closing tag,** not the next `</div>`. Getting
  this wrong once pushed 5 slides outside `.deck` and the counter read `02`.

Images and logos live in [`../assets/`](../assets/) — this deck uses 35 of them.
