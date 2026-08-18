# Documentation index

The executable contracts and source code remain the system's approved
expectation. These documents explain how to operate, verify, and evolve that
implementation **without becoming a second contract**. Where a document and the
code disagree, the code and `contracts/` win, and the document is the bug.

`docs/` holds this index, the **empty Converge factory** the room will fill,
and **external reference material** (PDFs and one HTML). Every narrative
document lives with the work it describes — plans in `plans/`, workshop
material in `presentation/`, and component guides in the component's own
folder. This page is the map to all of it.

## The base — start here

The root [README](../README.md) is the operator document for the **working
legacy use case**. That use case is the base. Read it, boot it, prove it,
before anything else.

| Order | Folder | Covers |
|---|---|---|
| 1 | [`contracts/`](../contracts/README.md) | The source of correctness: transport envelopes, the five types, and the no-oracle-no-build rule |
| 2 | [`gen/`](../gen/README.md) | DataGen's module map and the never-overwrite output rule |
| 3 | [`infra/`](../infra/README.md) | The SFTP image, the six sshd locks, and the role/zone matrix |
| 4 | [`legacy/`](../legacy/README.md) | The frozen oracle: five components, one batch end to end |
| 5 | [`legacy/publisher/`](../legacy/publisher/README.md) | Manifest-last publication onto raw SFTP |
| 6 | [`legacy/intake/`](../legacy/intake/README.md) | The raw zone authority and claim-by-rename |
| 7 | [`legacy/processor/`](../legacy/processor/README.md) | Raw-to-sanitized conversion and the privacy boundary |
| 8 | [`legacy/postgres/`](../legacy/postgres/README.md) | Typed loading, procedures, reconciliation, and the migration sequence |
| 9 | [`legacy/runner/`](../legacy/runner/README.md) | Orchestration, the adapter registry, and crash safety |
| 10 | [`validation/`](../validation/README.md) | Both referees and the rule that they never repair |
| 11 | [`tests/`](../tests/README.md) | The five-type verification map across all six test locations |

Architecture, ownership, and the proof ledger live in the
[completed legacy baseline](../plans/legacy.md).

## Plans — what is being built and why

| Document | Use it for |
|---|---|
| [Completed legacy baseline](../plans/legacy.md) | Consolidated architecture, ownership, operation, change control, and the proof ledger |
| [Modern pipeline spec](../plans/modern.md) | The independent second implementation: boundaries, golden-match rules, per-type checklist |
| [Dark Factory](../plans/dark-factory.md) | The doctrine: seven stages, four gate kinds, and what the factory must never do |

## Workshop and Bootcamp agendas

`presentation/` stays on `main`. It is not the base, but it is what we will
use to write the five-day agendas.

| Document | Use it for |
|---|---|
| [Master content & run of show](../presentation/agenda.md) | The single narrative source: act order, timings, beats, key lines, numbers, quotes, and the rehearsal checklist |
| [Live demo script](../presentation/demo.md) | Operator cheat-sheet for Acts 3A/3B — verified commands, the corrected reveal, and the failure protocol |

## Not the base

These guides describe work that is **not** the starting use case. They stay
in the tree; they are not what you boot on day zero.

| Folder | Covers |
|---|---|
| [`modern/`](../modern/README.md) | The independent second implementation and its lakehouse gates |
| [`factory/`](../factory/README.md) | The source-defect detector |

## Converge — fill this together

The document factory starts empty. ADRs, plans, and task notes are written
here during the week. See [`converge/README.md`](converge/README.md).

Prior-run records (`docs/decisions/001`–`011` and the July journal) were
removed from this tree so the room cannot copy last time’s answers. They
remain in git history.

## Reference material

External methodology and workshop artifacts. They are **inputs and background**,
not descriptions of this repository, and they do not replace the executable
contracts under `contracts/`.

| File | |
|---|---|
| `kurv-edp-v2.pdf` | The KurvPay EDP reference the Dark Factory stages are mapped against |
| `task-spec-v3.2.0.pdf` | The Task-Spec methodology |
| `boot-uc-northwind-pay-edp-oss-v2.pdf` | The originating brief for this use case |
| `cvg-aut-systems-spine-steps-v5.pdf` | Autonomous-systems spine steps |
| `wrksp-secret-dark-factory-v1.pdf` | Workshop framing and offer mechanics |
| `asd-agentic-loop-v1.0.html` | The agentic loop reference |

## Documents that moved

Nothing was lost; several documents were consolidated or relocated. If a link
or a memory points at one of these, this is where it went:

| Was | Now |
|---|---|
| `docs/content.md`, `docs/workshop-run-of-show-v1.md` | [`presentation/agenda.md`](../presentation/agenda.md) — merged into one narrative source |
| `docs/workshop-dark-factory-demo.md` | [`presentation/demo.md`](../presentation/demo.md) — beside the agenda it serves |
| `plans/dark-factory.md` (the old starting brief) | Retired. Standing boundaries → [`plans/dark-factory.md`](../plans/dark-factory.md) §9 |
| `plans/df-run-journal.md` and `docs/decisions/001`–`011` | Removed from this tree (clean slate). Recover from git history if needed |
| Developer, operator, and standalone architecture docs | [`plans/legacy.md`](../plans/legacy.md) |
| New ADRs | [`converge/02-structure/`](converge/02-structure/README.md) — written during the week |

---

**Link integrity is enforced.** `tests/unit/test_make_facade.py::
DocumentationLinksTest::test_local_markdown_links_resolve` fails `make check` if
any relative link on this page — or in any tracked Markdown file — points at
something that does not exist. Deleting a document without updating its
referrers turns the build red.
