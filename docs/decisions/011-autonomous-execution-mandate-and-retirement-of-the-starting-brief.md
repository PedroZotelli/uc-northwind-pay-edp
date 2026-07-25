# 011 — The autonomous execution mandate, and retirement of the starting brief

**Date:** 2026-07-25
**Status:** Accepted
**Supersedes the navigational role of:** `plans/dark-factory.md` (deleted)

## Context

`plans/dark-factory.md` was the Dark Factory *starting brief*: a forward-looking
document written before any detector existed. It opened with

> "Implementation pending. This document is the bounded starting brief for the
> next session; it is not evidence that a Dark Factory component exists."

That statement is now false. `factory/` contains the implemented detector,
`modern/` contains the independent second implementation, and the closing entry
of `plans/df-run-journal.md` records that the Dark Factory definition is met.

A brief whose run has already completed is not a plan — it is a historical
authorization plus a set of still-binding rules. Left in `plans/`, it misleads
any reader (human or agent) who starts from the status header.

Three things in it were still load-bearing and are preserved here:

1. the standing authorization for the lights-out run (a dated grant of
   autonomy — the kind of thing a decision record exists to hold);
2. the **first acceptance target** table, which
   `factory/tests/contract/test_finding_contract.py::
   test_type01_matches_the_published_first_acceptance_target` pins value by
   value;
3. the **non-negotiable boundaries**, which bind every phase and are not
   specific to the first slice.

## Decision

Retire `plans/dark-factory.md`. Record the mandate and the acceptance target
here. Move the non-negotiable boundaries into
[`plans/dark-factory-stages.md`](../../plans/dark-factory-stages.md) §9, "What
the factory must never do", where they are stated as standing doctrine rather
than as setup for a first slice.

### The autonomous end-to-end execution mandate — 2026-07-24

This section authorized a lights-out run. A session explicitly invoked to
"execute the autonomous mandate" proceeded end-to-end without waiting for human
approval, under the rules below. For that run only, it superseded the
"stop for review" checkpoints of the brief and the "pending design decisions
belong to a future design turn" deferral in `plans/modern.md`. Interactive
sessions not invoked with the mandate kept stop-for-review behavior.

**Standing authorization.** The executing agent decided every open design
question itself — the finding schema, directory ownership, Python packaging,
Parquet canonicalization, the dlt role, dbt grains and keys, golden-match keys,
the Dagster model, and anything comparable. Every such decision is recorded as a
numbered decision record in `docs/decisions/`, in the same commit that first
implements it. Human review happens after the run — from decision records,
commits, the run journal, and evidence — not during it.

**Phase 0 — re-prove the committed baseline (mandatory first act).** The
2026-07-24 proof ledger identified implementation manifest `d3e6e95a…`
(260 files); the committed tree differed (268 files) because the Type `01`
parity refactor landed after the authoritative five-type proof. Before any
Dark Factory code: `make init && make deploy && make status`; `make check`;
`make test` (the full 25-case automatic-worker portfolio) on a fresh runtime;
`make clean CONFIRM=clean-runtime`, redeploy, then `make test-e2e TYPE=all`
(the two portfolios reuse canonical batch IDs and must not share one runtime);
then a dated ledger entry appended to `plans/legacy.md` with results and a
freshly computed manifest hash. Nothing in `legacy/`, `contracts/`, `gen/`,
`infra/`, or applied migrations could change to make Phase 0 pass — a red gate
was a blocker report, not a license to fix legacy.

**Phase 1** — the Type `01` detector slice, honoring every step gate.
**Phase 2** — detector expansion, `DF-SOURCE-002` through `005`, one completed
type at a time.
**Phase 3** — the modern pipeline built as the factory's product, executing
`plans/modern.md` milestones M0–M6 under all of that plan's boundaries. The
detector may consume modern observations only as an additional read-only
channel; it never computes modern business results.
**Phase 4 — the definition of "Dark Factory 100% running".** Complete only
when, each on a fresh isolated runtime: Phase 0 gates are green on the
committed tree; findings for all five `DF-SOURCE-*` scenarios are byte-stable,
privacy-clean, and acceptance-verified with isolation and peer continuation
proven; modern Types `01`–`05` reach Gold with zero unexplained golden-match
differences; complete privacy-safe evidence packets exist for legacy, detector,
and modern runs; and one documented top-level command per system reproduces
each proof.

**Rules of engagement.** Work only in the dedicated worktree and branch; commit
in small, gate-passing increments; never push, open PRs, send notifications, or
make any external write unless separately instructed. Never weaken, edit, or
"fix" an expected value, contract fixture, or oracle to turn a red gate green —
green must come from the referee. Fresh isolated runtime for every authoritative
acceptance. Maintain `plans/df-run-journal.md`, one dated entry per phase and
gate. Hard-stop and report on: any restricted value outside the privacy
allowlist in a produced artifact; any mutation of frozen legacy inputs; a gate
that cannot pass without changing frozen truth; Docker or the runtime
unavailable.

### The first acceptance target

Pinned value by value by
`factory/tests/contract/test_finding_contract.py::
test_type01_matches_the_published_first_acceptance_target`. **This table is the
published target that test refers to; keep them in step.**

| Field | Expected value |
|---|---|
| Type | `01` |
| Scenario | `DF-SOURCE-001` |
| Batch | `B202607230000004` |
| Source-owned net declaration | `173.44` |
| Independently computed net | `173.45` |
| Detail count | Declared `2`, computed `2` |
| Legacy terminal status | `quarantined` |
| Legacy terminal code | `SOURCE_CONTROL_TOTAL_MISMATCH` |
| Attribution | Source system of record |
| Sanitized CSV | Absent |
| PostgreSQL business mutation | Zero |
| Finding scope | Affected batch only |
| Required peer continuation | `B202402290000001` and `B202607230000002` succeed |

The contract oracle for this target is
`contracts/types/01-card-settlement/main/expected-df-source-001-finding.yaml`.
The legacy proof route is `make test-type01`.

## Alternatives considered

- **Keep `plans/dark-factory.md` and just correct its status header.** Rejected:
  the remainder is a build sequence, an out-of-scope list, and a
  "next-session starting point" for a session that has already run. Correcting
  the header would leave a document whose whole body is spent.
- **Fold the brief into `plans/dark-factory-stages.md` wholesale.** Rejected:
  the stages document is a teaching document about how the factory works.
  Splicing a dated authorization into it would blur the distinction between
  standing doctrine and a one-time grant of autonomy.
- **Delete the brief outright.** Rejected: the mandate is the audit trail for
  why an agent was permitted to decide design questions unsupervised, and the
  acceptance table is referenced by a test.

## Consequences

- `plans/` drops to four engineering documents: `legacy.md` (the frozen oracle),
  `modern.md` (the second implementation), `dark-factory-stages.md` (doctrine),
  and `df-run-journal.md` (what actually ran).
- Records 001, 002, and 010 still cite `plans/dark-factory.md`. They are dated
  records of what was decided at the time and are not rewritten; this record is
  where that path now resolves.
- The docstring in `test_finding_contract.py` is updated to point here.
- `plans/modern.md` and `plans/legacy.md` lose their "next phase" pointers into
  the brief; both now point at the stages document.
