# Plans — the engagement map

These three documents are the guiding process for the whole week. They
are not optional reading and they are not last-run souvenirs. One
describes the use case that already runs. One is the contract for the
second implementation. One is the later factory idea — a seed, not a
plant that already runs.

| Plan | What it is | When you open it |
|---|---|---|
| [`legacy.md`](legacy.md) | The completed local baseline: architecture, operating model, 25-batch catalog, and the 2026-07-24 proof ledger | Before anyone touches a later fabric. This is what must stay true. |
| [`modern.md`](modern.md) | The specification the second implementation must satisfy: independence rules, type map, golden-match, milestones, definition of done | Every time a modern package, model, or gate is designed or accepted |
| [`dark-factory.md`](dark-factory.md) | The later idea: lights-out build, stages, gates, unattended loop | When the room needs the broader picture. Enhance it as the week writes the factory. |

The detector is still later. It is not a finished `factory/` folder.

## How the two plans work together

```text
contracts/  ── source of correctness for both sides
    │
    ├── legacy.md         frozen path that already runs
    │                       DataGen → SFTP → Java 21 → PostgreSQL → oracle
    │
    ├── modern.md         path the week constructs
    │                       same raw SFTP → Python → modern/landing/
    │                       → dlt → DuckLake/DuckDB → dbt → golden-match
    │
    └── dark-factory.md   later idea — enhance as the factory is built
```

Legacy is the **observed reference system**. Modern is an **independent
second implementation**. Neither may edit `contracts/`, `legacy/`,
`gen/`, or `infra/` to make a later gate pass.

## What is frozen, what is built

| Frozen on this tree | Built during the week |
|---|---|
| Five signed type contracts (`01`–`05`) | `modern/` for those same five types |
| DataGen, SFTP, Java 21, PostgreSQL | Golden-match wiring against live modern observations |
| Independent oracles under `validation/oracle/` | One vertical at a time, `01` first |
| Inbound packs for `01`–`05` under [`spec/`](../spec/README.md) | Understanding, ADRs, then translation |
| `validation/golden-match/golden_match.py` | Tests, Make targets, `evidence/modern/` |
| This folder | Factory later. Day five: Type `06` unseen + **red pill** — a numeric miss attributed to the legacy plant (`CONFIRMED_LEGACY_DEFECT`), found not repaired |

## How to use them in the room

1. **Arrive.** Boot the use case with `make deploy` and one
   `make run TYPE=01 SCENARIO=valid-minimal`. Confirm the packet in
   [`legacy.md`](legacy.md#batch-evidence) and the Type `01` row in the
   [25-batch catalog](legacy.md#canonical-25-batch-catalog).
2. **Design.** Open [`modern.md`](modern.md). Close the standing design
   questions for the current type before writing a parser.
3. **Build the week's types.** `01`–`05` only. Type `01` first. The
   inbound drop is [`spec/`](../spec/README.md). Type `06` stays sealed
   until day five.
4. **Adjudicate.** Golden-match asks two questions and never nets them:
   did modern match legacy, and did modern match the contract?
5. **Do not repair a source lie.** Every `DF-SOURCE-*` batch is a
   one-cent (or one-cent-equivalent) declaration the source got wrong.
   Compute the truth, keep the declaration, refuse the batch.

## Operator entry

The day-to-day commands live in the root [`README.md`](../README.md).
The plans do not replace that page. They explain *why* those commands
exist and what a green result is allowed to mean.
