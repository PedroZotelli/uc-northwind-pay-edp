# 002 — Dark Factory directory ownership, packaging, and Make facade

- Date: 2026-07-24
- Phase: 1, Step 1
- Status: accepted

## Context

`plans/dark-factory.md` proposes a `dark-factory/` tree but explicitly withholds
approval: "Do not scaffold these directories until their ownership and contracts
are approved." Under the autonomous mandate that approval is mine to give, so
the ownership boundary has to be settled before the first line of detector code.

The constraints that shape it: the detector is read-only over legacy artifacts;
system of record, source of observation, source of correctness, and executable
Git contract must stay separate in code and evidence; and `legacy/`,
`contracts/`, `gen/`, and `infra/` are frozen.

## Decision

### Tree

```text
dark-factory/
├── contracts/          executable Dark Factory contract (source of correctness)
│   ├── finding.schema.json
│   ├── privacy-allowlist.yaml
│   ├── error-codes.yaml
│   └── scenarios.yaml
├── src/darkfactory/
│   ├── observations/   read-only adapters, one per observation channel
│   ├── detection/      deterministic control comparison
│   ├── attribution/    evidence-based ownership reasoning
│   ├── findings/       canonical model, privacy scan, atomic writer
│   ├── canonical.py    canonical JSON and finding identity
│   ├── config.py       read-only runtime settings
│   ├── errors.py       stable error codes
│   └── cli.py          the single bounded entrypoint
├── tools/              measurement instruments (manifest hashing)
└── tests/{contract,unit,security,end-to-end}/
```

`dark-factory/` owns nothing outside itself. It never writes to `legacy/`,
`contracts/`, `gen/`, `infra/`, the SFTP volume, or PostgreSQL.

### Packaging

No new dependency, no new virtual environment, no build backend. The detector
runs on the existing `legacy/runner/.venv` (Python 3.12.11) and imports only the
standard library plus `PyYAML`, `jsonschema`, `psycopg`, and `paramiko` — all
already pinned by `legacy/runner/requirements.txt`. Imports resolve through
`PYTHONPATH=dark-factory/src`, matching how every other component in this
repository is wired.

The package is `darkfactory` (one importable root) rather than the flat
`src/observations/`, `src/detection/`, … the brief sketches. A flat layout would
put generic module names like `evidence` and `config` on `sys.path` beside
`legacy/runner/evidence.py` and `legacy/runner/config.py`, which already own
those names. A named package makes accidental cross-import impossible to do
silently, which matters when the whole point of the component is that it must
not reach into legacy internals.

### Configuration

`darkfactory.config` reads `.env` with its own small parser instead of importing
`legacy.runner.config`. Reusing the legacy loader would be convenient and would
also be the first thread of coupling between an observer and the system it
observes; the duplication is about forty lines and buys a boundary that a test
can assert.

### Make facade

Dark Factory targets are additive, prefixed `df-`, and delegate to the CLI:

| Target | Responsibility |
|---|---|
| `make df-manifest [REV=…]` | Recompute a proof-ledger implementation manifest |
| `make df-check` | Dark Factory contract, unit, and security suites plus strict typing |
| `make df-detect TYPE=NN` | Run the detector for one type against a live runtime |
| `make df-accept TYPE=NN\|all` | Run the live acceptance gate for one type or all five |

No existing target changes behavior. `make check` and `make test` keep proving
the legacy baseline alone, so a Dark Factory regression can never be reported as
a legacy result or vice versa.

## Alternatives considered

- **Flat `src/` as sketched in the brief.** Rejected for the module-shadowing
  reason above. The brief marks those names "provisional until the first task
  specification is approved", which this record is.
- **A separate `dark-factory/.venv` with its own `pyproject.toml`.** Rejected:
  it buys isolation the `PYTHONPATH` boundary already provides, and adds a
  second interpreter to keep in step with the frozen one.
- **Importing `legacy/runner/config.py` and `sftp_client.py`.** Rejected:
  `sftp_client` has write methods. Reusing it would make "no adapter has a write
  path" a claim about discipline rather than about the code.
- **Folding Dark Factory targets into `make check`/`make test`.** Rejected: it
  would blur the evidence boundary the plans insist on.

## Consequences

- `dark-factory/` appears in the tree but stays out of the legacy implementation
  manifest boundary, so legacy ledger hashes remain comparable across this run.
- The root `Makefile` changes (it is not a frozen root), which does move the
  working-tree manifest away from the Phase 0 value. Ledger entries are bound to
  a revision, so this is expected — see
  [DR-001](001-phase-0-reproof-and-implementation-manifest.md).
- Adding a dependency later means editing `legacy/runner/requirements.txt`,
  which is inside a frozen root. That is deliberate friction: it forces the
  question back through a decision record instead of happening by accident.
