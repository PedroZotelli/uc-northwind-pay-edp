# NorthWind Pay EDP — the base

The **working legacy use case**. This is what must run, end to end, before
anyone starts building the modern fabric.

```text
contracts
    → DataGen
    → raw SFTP
    → Java 21 privacy boundary
    → sanitized SFTP
    → PostgreSQL COPY + stored procedures
    → reconciliation + independent oracle
    → archive  or  batch-scoped quarantine
```

Every arrow is an explicit interface. DataGen does not call Java. Java does not
write PostgreSQL. Procedures do not read SFTP. The loader is structurally
incapable of seeing a PAN — that is Unix groups, not a comment.

When two components disagree, [`contracts/`](contracts/README.md) decides
which one is wrong. Nothing in `legacy/`, `contracts/`, `gen/`, or `infra/`
may be edited to make a later gate pass.

## The base

Setup and configuration sit at the front. These folders *are* the use case.

| Order | Folder | What it is |
|---|---|---|
| 1 | [`contracts/`](contracts/README.md) | Source of correctness. **Five** file types, signed off. Types `06+` are later kits, not empty folders |
| 2 | [`gen/`](gen/README.md) | DataGen — the simulated upstream. Writes raw bytes, checksum, source manifest |
| 3 | [`infra/`](infra/README.md) | Local SFTP image and the four-role / eight-zone matrix |
| 4 | [`legacy/publisher/`](legacy/publisher/README.md) | Drops a bundle onto `raw/incoming`, manifest last |
| 5 | [`legacy/intake/`](legacy/intake/README.md) | Claims the batch (rename = lock) |
| 6 | [`legacy/processor/`](legacy/processor/README.md) | Java 21: parse, validate, **sanitize**, write CSV |
| 7 | [`legacy/postgres/`](legacy/postgres/README.md) | COPY, stored procedures, reporting reconciliation |
| 8 | [`legacy/runner/`](legacy/runner/README.md) | The one public orchestrator: `make run`, `make worker` |
| 9 | [`validation/oracle/`](validation/README.md) | Independent referee. Recomputes the contract; never repairs |
| 10 | [`tests/`](tests/README.md) | Live acceptance, contract oracles, unit, PostgreSQL, security |

Root control plane: `Makefile`, `compose.yaml`, `.env.example`.

`spec/` holds a docked Type `05` work order (specification + expected
outputs, no modern code). It is an incoming kit, not a second implementation.
New file types for a later unattended run arrive the same way.

## Not the base

These stay in the tree. They are not the starting use case.

| Folder | What it is |
|---|---|
| [`plans/modern.md`](plans/modern.md) | Spec the week must satisfy when the second implementation is built |
| [`validation/golden-match/`](validation/README.md) | Modern referee — attached when that implementation exists |
| [`presentation/`](presentation/agenda.md) | Workshop deck, demo script, five-day agenda seed |
| [`prompts/`](prompts/README.md) | Instructor demo cards |

## Four truth roles

| Role | Meaning here |
|---|---|
| System of record | The simulated source owns its raw file and declared controls; committed PostgreSQL tables own applied legacy state |
| Source of observation | Immutable SFTP bytes, hashes, manifests, database observations, and per-run evidence show what actually happened |
| Source of correctness | Independently reviewed expected CSV, reconciliation, and governed business rules define what should happen |
| Executable Git contract | Versioned YAML, schemas, canonical fixtures, and tests encode the currently approved expectation |

A source system can be the system of record and still emit a defective batch.
A referee may identify that mismatch, but **no implementation is allowed to
silently redefine its own expected answer.**

## Boot the use case

Requirements: Docker with Compose, GNU Make, Python 3.12 or newer.

```bash
make init          # environments, .env, container builds
make deploy        # SFTP + PostgreSQL, migrations, health checks
make status
```

One public runner for every type:

```bash
make run TYPE=01 SCENARIO=valid-minimal
make run TYPE=05 SCENARIO=rounding-half-up
make run TYPE=all SCENARIO=valid-minimal
make run-file TYPE=03 FILE=/absolute/path/to/source.rem
make worker                              # the autonomous poller, foreground
```

`TYPE=all` is supported where one operation applies safely to every registered
type: `gen`, `run`, and `test-e2e`. An explicit file always requires one exact
type.

## Prove the base

```bash
make check              # source, build, Java, and the fast suites
make test-postgres      # rollback-only, against a live database
make test-e2e TYPE=all  # live acceptance, all five types
make test               # check + PostgreSQL + the worker portfolio
```

Live suites need a deployed runtime and **do not clean state on your behalf.**
Canonical batch IDs are immutable, so isolate or clean before repeating one:

```bash
make clean CONFIRM=clean-runtime && make deploy
```

[`tests/README.md`](tests/README.md) is the verification map across all test
locations. Test counts are deliberately not frozen here.

## Safety and lifecycle

Raw synthetic files contain deliberately restricted identifiers. **Java is the
mandatory privacy boundary** on the legacy side: raw values may not enter
sanitized CSV, logs, evidence, staging, operational tables, or reconciliation
unless a contract explicitly permits a validated transformation.

Separation is enforced by the operating system. The four SFTP roles have real
Unix group ownership across eight zones. See [`infra/README.md`](infra/README.md).

Services bind to `127.0.0.1`. PostgreSQL application access is non-superuser,
publication is manifest-last, and terminal failures are batch-scoped: one bad
batch never stops the line.

`make clean CONFIRM=clean-runtime` is destructive and never implicit. It removes
Compose volumes plus the disposable `.runtime/` and `evidence/` trees — but
**not** `gen/output/`, which is immutable and never overwritten.

## The rule the whole system rests on

> **No oracle, no build.** A specification that does not ship its expected
> outputs cannot be adjudicated, so the factory refuses it before doing any
> work.

And its corollary, learned the hard way here more than once:

> **A gate that cannot fail is worse than no gate.** Six have been found and
> closed in this repository. When you add one, prove it red before you accept
> it green.

## Documentation

- [Plans — the engagement map](plans/README.md)
- [Completed legacy baseline and proof ledger](plans/legacy.md)
- [Modern target plan](plans/modern.md) — the contract the later fabric must satisfy, not the implementation
- [ASD — the Agentic Loop](docs/asd-agentic-loop.html) — runtime anatomy
