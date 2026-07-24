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
