# Dark Factory autonomous run journal

One dated entry per phase and gate of the lights-out run authorized by the
"Autonomous end-to-end execution mandate" in [`dark-factory.md`](dark-factory.md).
Each entry records status, evidence paths, decision-record references, and
blockers. Decision records live in [`../docs/decisions/`](../docs/decisions/).

Worktree: `sc-coherent-qubit-9d9e`. Branch: `wktr-dark-factory-e2e`.
No pushes, pull requests, notifications, or external writes occur in this run.

---

## 2026-07-24 — Phase 0, gate 0.0: environment and freshness

**Status:** passed.

Docker 29.6.2 with Compose v5.3.1, GNU Make 3.81, Python 3.12.11 available at
`/opt/homebrew/bin/python3.12`, local ports `2222` and `54329` free. The host
default interpreter is 3.14.6, so the runner virtual environment was created
with `PYTHON=/opt/homebrew/bin/python3.12 make init` — see
[DR-001](../docs/decisions/001-phase-0-reproof-and-implementation-manifest.md).

The machine already carried a `northwind-pay-legacy` Compose project whose
`sftp_data` volume held 143 files under `raw/quarantine`, including canonical
batch identities such as `B202607230000004`. That runtime was **not** fresh and
would have collided with the acceptance suites. It was destroyed with
`make clean CONFIRM=clean-runtime` and rebuilt; emptiness was then verified
positively (`sftp_data` file count `0`, migrations `001`–`010` applied from
scratch, PostgreSQL role `northwind_loader`, `superuser: false`).

Nothing under `legacy/`, `contracts/`, `gen/`, `infra/`, or the applied
migrations was touched.

## 2026-07-24 — Phase 0, gate 0.1: `make init && make deploy && make status`

**Status:** passed.

- `make init` — runner virtual environment on Python 3.12.11; `sftp` and
  `processor` images built.
- `make deploy` — services healthy, verified SFTP host key captured, migrations
  `001, 002, 003, 004, 005, 006, 007, 008, 009, 010` applied.
- `make status` —
  `{"postgres": {"role": "northwind_loader", "status": "healthy", "superuser": false, "version": "16.14"}, "sftp_roles": {"loader": "healthy", "operator": "healthy", "processor": "healthy", "raw-publisher": "healthy"}, "status": "healthy"}`

**Evidence:** `/tmp/dfrun/00-init.log`, `/tmp/dfrun/02-deploy-fresh.log`.

## 2026-07-24 — Phase 0, gate 0.2: `make check`

**Status:** passed.

| Suite | Result |
|---|---:|
| Contracts | `47` OK |
| DataGen | `68` OK |
| Python unit | `144` OK |
| Security | `15` OK |
| Oracle | `31` OK |
| mypy `--strict` (gen) | no issues, 14 source files |
| mypy `--strict` (worker boundary) | no issues, 6 source files |

`make check` initially reported the processor image as `CACHED`, so the Java
suite had not executed on the committed bytes. A forced
`docker compose build --no-cache processor` ran it for real:
`Tests run: 78, Failures: 0, Errors: 0, Skipped: 0` / `BUILD SUCCESS`.

**Evidence:** `/tmp/dfrun/03-check.log`, `/tmp/dfrun/04-java-nocache.log`.

## 2026-07-24 — Phase 0, gate 0.3: `make test` (25-case worker portfolio)

**Status:** passed, on the fresh runtime from gate 0.1.

Source and build gates repeated identically (47 / 68 / 144 / 15 / 31), live
PostgreSQL regressions `13` OK, then the live worker suite:

```json
{"cache_conflict": "verified_retry", "canonical_quarantines": 10,
 "canonical_successes": 15, "daemon_sigterm": "verified",
 "integrity_quarantines": 1, "lock_contention": "verified",
 "oracle_mismatches": 1, "quarantine_uncertainty": "verified_retry",
 "restart_database_commit": "verified", "restart_oracle_mismatch": "verified",
 "restart_raw_archive": "verified", "restart_raw_quarantine": "verified",
 "retained_cache_replay": "verified", "status": "passed", "worker_cases": 25}
```

**Evidence:** `/tmp/dfrun/05-test.log`.

## 2026-07-24 — Phase 0, gate 0.4: runtime rotation and `make test-e2e TYPE=all`

**Status:** passed, on a second fresh runtime.

The two portfolios reuse canonical immutable batch identities and must not
share a runtime, so `make clean CONFIRM=clean-runtime` ran between them and the
new runtime was verified empty (`sftp_data` file count `0`) before redeploying.

| Type | Succeeded | Quarantined |
|---|---:|---:|
| `01` | 3 | 2 |
| `02` | 3 | 2 |
| `03` | 3 | 2 |
| `04` | 3 | 2 |
| `05` | 3 | 2 |

Terminal topology observed read-only after the portfolio:

| Observation | Count |
|---|---:|
| Raw archive / quarantine | `15` / `10` |
| Raw incoming / processing | `0` / `0` |
| CSV archive / quarantine | `15` / `0` |
| CSV outgoing / processing | `0` / `0` |
| `control.batches` | `25` (`15` succeeded, `10` quarantined) |
| `control.rejects` | `10` |
| `control.files` / `loads` / `procedure_runs` | `40` / `15` / `30` |
| Evidence packets | `25` across the five isolated suite roots |

**Evidence:** `/tmp/dfrun/07-e2e-all.log`,
`.runtime/e2e-evidence/`, `.runtime/e2e-type0{2,3,4,5}-evidence/`.

## 2026-07-24 — Phase 0, gate 0.5: committed-tree ledger entry

**Status:** passed.

Implementation manifest of the committed tree recomputed under the ledger's
published boundary: `268` files,
`12ce7f449228ae70d4781066b009ce63d5b18e037795ab70c5e0c4e6cd0d0dea`. Working
tree was clean at the time of computation. Recorded as a dated ledger entry in
[`legacy.md`](legacy.md). Method and its rationale: [DR-001](../docs/decisions/001-phase-0-reproof-and-implementation-manifest.md).

**Phase 0 verdict: the committed baseline is re-proven green. No blockers. No
frozen input was modified.**

---

## 2026-07-24 — Phase 1: Type 01 detector slice, Steps 1–6

**Status:** passed. Decision records
[DR-002](../docs/decisions/002-dark-factory-ownership-and-packaging.md),
[DR-003](../docs/decisions/003-finding-contract-canonical-json-and-identity.md),
[DR-004](../docs/decisions/004-privacy-allowlist-and-restricted-value-scan.md),
[DR-005](../docs/decisions/005-read-only-observation-adapters.md),
[DR-006](../docs/decisions/006-evidence-based-attribution.md),
[DR-007](../docs/decisions/007-dark-factory-evidence-packet.md).

| Step | Gate | Result |
|---|---|---|
| 1 | Contract tests reject drift, extra fields, restricted values | `16` contract tests pass; schema closed at every depth |
| 2 | No adapter has a write path | AST scan of every observation module passes; server-side `SET TRANSACTION READ ONLY`; SFTP `RejectPolicy` |
| 3 | Deterministic input produces byte-identical canonical data | Two runs, identical `finding_id` and identity bytes |
| 4 | Removing any required observation prevents a conclusive attribution | All four required channels proven by withhold probe |
| 5 | Isolation and continuation both observed | No sanitized CSV, `0` staging and business rows, quarantine batch-scoped, both peers `succeeded`/`MATCHED` |
| 6 | Fresh run recreates the expected finding, no leak, no legacy mutation | Packet published atomically; legacy evidence tree byte-identical before and after |

Source gate: `16` contract, `30` unit, `23` security, `mypy --strict` clean over
21 files. Live gate: `make df-accept TYPE=01`, finding
`sha256:2ba123ee0dfd24d31dc12db93e300c0ce949fc7cd113ddabf7ff0e3bd0807710`,
acceptance target values matched exactly (declared `173.44`, computed `173.45`,
detail count `2`/`2`, `quarantined`, `SOURCE_CONTROL_TOTAL_MISMATCH`, source
system of record, no sanitized CSV, zero business mutation, batch scope, peers
`B202402290000001` and `B202607230000002`).

**Two gates were vacuous on first implementation and were tightened rather than
accepted:**

1. The Step 4 withhold probe passed with every channel withheld, because the
   attribution rule required "at least two" corroborating channels and three
   were available. The rule now requires its complete channel set — see
   [DR-006](../docs/decisions/006-evidence-based-attribution.md).
2. The privacy corpus scan reported violations for values carrying no restricted
   content — zero-padding runs, the batch identity, and hex digests. Scoping was
   corrected and the alphabetic corpus match was removed with a structural
   argument in its place — see
   [DR-004](../docs/decisions/004-privacy-allowlist-and-restricted-value-scan.md).

Nothing under `legacy/`, `contracts/`, `gen/`, `infra/`, or the applied
migrations was modified. No expected value, fixture, or oracle was edited.

---

## 2026-07-24 — Phase 2: detector expansion, DF-SOURCE-002 through 005

**Status:** passed, one completed type at a time in order `02 → 03 → 04 → 05`.
Each type passed all six step gates and its acceptance target before the next
began.

The detector is contract-driven and type-generic: control pairs are discovered
by pairing `declared_*` with `computed_*` keys in the legacy processor result
rather than from a per-type field list, so expansion added scenario bindings,
frozen expected findings, and gate runs — not new detection logic. The one
per-type binding that could not be derived is the mapping from the control
plane's generic `computed_count` / `computed_net_amount` columns to each type's
control names, which is declared explicitly in `scenarios.yaml`.

| Type | Scenario | Batch | Difference | Finding identity |
|---|---|---|---|---|
| `02` | `DF-SOURCE-002` | `B202607230000105` | `net_amount` `173.44` → `173.45` | `sha256:056997d0…` |
| `03` | `DF-SOURCE-003` | `B202607230000205` | `net_amount` `198.49` → `198.50` | `sha256:16dfbac3…` |
| `04` | `DF-SOURCE-004` | `B202607230000305` | `net_amount` `999.99` → `1000.00` | `sha256:1c79a11f…` |
| `05` | `DF-SOURCE-005` | `B202607230000405` | `assessed_fee` `0.99` → `1.00` | `sha256:ba312588…` |

Every type: byte-stable, privacy-clean, isolation verified, peer continuation
verified, all four required channels proven by withhold probe, legacy evidence
byte-identical before and after, terminal code equal to the frozen legacy
oracle's.

**An honest difference between Type 01 and Types 02–05 is recorded in the
findings themselves.** Type `01` publishes `postgres-diagnostic.json` with
`mode: read_only` — a genuine independent SQL recomputation — so its diagnostic
channel carries `independence: independent_computation`. Types `02`–`05` publish
`mode: source-parser-observation`, a projection of the Java result, so theirs
carries `derived_projection`. The classification is read from the artifact's own
`mode`, not from a table maintained by hand, and it means Types `02`–`05` reach
`conclusive` on a strictly weaker corroboration set than Type `01`. A reader can
see that in `observations[].independence` without consulting a document. See
[DR-006](../docs/decisions/006-evidence-based-attribution.md).

Source gate after expansion: `18` contract, `30` unit, `23` security,
`mypy --strict` clean over 21 files.
