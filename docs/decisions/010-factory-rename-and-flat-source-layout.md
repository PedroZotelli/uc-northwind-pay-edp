# 010 — `factory/` rename and flat source layout

- Date: 2026-07-25
- Phase: pre-workshop review
- Status: accepted
- Supersedes the packaging half of
  [DR-002](002-dark-factory-ownership-and-packaging.md); its ownership rules
  stand unchanged.

## Context

DR-002 established `dark-factory/` as a self-contained component with
`dark-factory/src/darkfactory/` as an importable package on
`PYTHONPATH=dark-factory/src`.

Two problems with that shape surfaced during the pre-workshop review. The
directory name repeated the concept twice on every path
(`dark-factory/src/darkfactory/...`), and the package layer was inconsistent
with `gen/src/`, the repository's other Python component, whose modules sit
flat on the path.

## Decision

### The folder is `factory/` and `src/` is flat

```text
before   dark-factory/src/darkfactory/observations/collect.py
after    factory/src/observations/collect.py
```

Module paths become `cli`, `contracts`, `errors`, `observations.collect`.
`python -m darkfactory.cli` becomes `python -m cli`. All parent-relative imports
(`from ..errors import`) became absolute; sub-package-internal imports
(`from .model import`) were left alone.

`REPOSITORY_ROOT` moved from `parents[3]` to `parents[2]`, one directory level
having been removed.

### The colliding module was renamed, and the test that caught it was not touched

Flattening put `config.py` at the top level of a source root, where
`legacy/runner/config.py` also lives as a flat module. The AST security test —
which forbids an observation adapter from importing a legacy runtime module by
name — could no longer distinguish them, and failed:

```
'config' unexpectedly found in frozenset({… 'config' …})
  : collect.py imports the legacy runtime module config
```

`config.py` is now `detector_config.py`. There is no name shared between
`factory/src/*.py` and `legacy/runner/*.py`.

Weakening the test — excluding the detector's own module names from the
forbidden set — was considered and rejected outright. The whole subject of this
repository is gates that cannot fail; introducing one to accommodate a layout
change would have been self-defeating.

### The detector's contract identity does not change

`northwind-pay-dark-factory-source-control-detector` remains the value in
`scenarios.yaml`, `privacy-allowlist.yaml`, `finding.schema.json`, and all five
approved findings under `contracts/expected/`.

Two reasons. The identity appears inside findings that have already been emitted
and adjudicated, and a directory rename must not retroactively change what a
published finding claims about its own author. And changing it would require
editing approved expected artifacts, which this repository does not do.

The folder is a location; the detector is a thing. They are allowed to differ.

### Prose and history were left alone

"Dark Factory" remains the name of the concept, the workshop, and the plan.
`plans/dark-factory.md`, `docs/workshop-dark-factory-demo.md`, the `DF-SOURCE-*`
scenarios, the `DF-E-*` error codes, and `DarkFactoryError` are unchanged.

Decision records DR-001 through DR-007 keep their original path references.
They are dated records of what was decided at the time, not navigation. This
record is the mapping. `docs/workshop-dark-factory-demo.md` **was** updated,
because it is an operational runbook whose commands are executed rather than
read.

## Alternatives considered

- **Keep the `darkfactory` package layer.** Rejected: the request was explicit,
  and the flat layout matches `gen/src/`.
- **Flatten and relax the security test.** Rejected, as above.
- **Rename the detector identity to match the folder.** Rejected: it would edit
  approved expected artifacts and invalidate the identity of already-published
  findings.
- **Rename `plans/dark-factory.md` and the DR filenames.** Rejected: the concept
  keeps its name, and renaming historical documents obscures the record.

## Consequences

- `make df-check`, `df-detect`, `df-accept`, and `df-manifest` all use the new
  paths; `df-detect` invokes `-m cli`.
- **A new top-level module in `factory/src/` must have a name that does not
  appear in `legacy/runner/`, `gen/src/`, or `validation/oracle/`.** A collision
  shadows silently at import time. This is the standing cost of the flat layout
  and is recorded in [`factory/README.md`](../../factory/README.md).
- Evidence moves from `evidence/dark-factory/` to `evidence/factory/`. Both are
  under the gitignored `evidence/` root, so no history is affected.
- The detector source digest is computed over `factory/src`; the removed package
  `__init__.py` changes the digest value. It is a run-scoped field and appears
  in no approved artifact.
