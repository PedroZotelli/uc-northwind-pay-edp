# Plans — the engagement map

These two documents are the guiding process for the whole week. They are
not optional reading and they are not last-run souvenirs. One describes
the use case that already runs. The other is the contract the room must
satisfy when the second implementation is built.

| Plan | What it is | When you open it |
|---|---|---|
| [`legacy.md`](legacy.md) | The completed local baseline: architecture, operating model, 25-batch catalog, and the 2026-07-24 proof ledger | Before anyone touches a later fabric. This is what must stay true. |
| [`modern.md`](modern.md) | The specification the second implementation must satisfy: independence rules, type map, golden-match, milestones, definition of done | Every time a modern package, model, or gate is designed or accepted |

There is no third plan on this tree. The detector is built later against
the same contracts and observations. Its doctrine lives as a section in
[`modern.md`](modern.md#relationship-to-dark-factory), not as a finished
`factory/` folder.

## How the two plans work together

```text
contracts/  ── source of correctness for both sides
    │
    ├── legacy.md   describes the frozen path that already runs
    │                 DataGen → SFTP → Java 21 → PostgreSQL → oracle
    │
    └── modern.md   specifies the path the week constructs
                      same raw bytes → Python → Parquet → lakehouse
                      → golden-match against contract + legacy
```

Legacy is the **observed reference system**. Modern is an **independent
second implementation**. Neither may edit `contracts/`, `legacy/`,
`gen/`, or `infra/` to make a later gate pass.

## What is frozen, what is built

| Frozen on this tree | Built during the week |
|---|---|
| Five signed type contracts | `modern/` ingestion, lakehouse, dbt, Dagster, serving |
| DataGen, SFTP, Java 21, PostgreSQL | Golden-match wiring against live modern observations |
| Independent oracles under `validation/oracle/` | Type `05` modern vertical from the docked kit |
| `validation/golden-match/golden_match.py` (the referee module) | Tests, Make targets, and evidence under `evidence/modern/` |
| This folder | A later read-only detector |

## How to use them in the room

1. **Arrive.** Boot the use case with `make deploy` and one
   `make run TYPE=01 SCENARIO=valid-minimal`. Confirm the packet in
   [`legacy.md`](legacy.md#batch-evidence) and the Type `01` row in the
   [25-batch catalog](legacy.md#canonical-25-batch-catalog).
2. **Design.** Open [`modern.md`](modern.md). Close the standing design
   questions for the current type before writing a parser.
3. **Build one vertical.** Type `01` first. Then `02`–`04`. Type `05`
   is already docked as a kit in
   [`spec/type-05-merchant-fee-assessment/`](../spec/type-05-merchant-fee-assessment/WORK-ORDER.md).
4. **Adjudicate.** Golden-match asks two questions and never nets them:
   did modern match legacy, and did modern match the contract?
5. **Do not repair a source lie.** Every `DF-SOURCE-*` batch is a
   one-cent (or one-cent-equivalent) declaration the source got wrong.
   Compute the truth, keep the declaration, refuse the batch.

## Operator entry

The day-to-day commands live in the root [`README.md`](../README.md).
The plans do not replace that page. They explain *why* those commands
exist and what a green result is allowed to mean.
