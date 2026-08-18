# The Factory — the source-defect detector

**5,996 lines across 39 files.** This is the component that reads immutable
legacy observations and decides, with evidence, **who is at fault** when the
declared and computed controls of a batch disagree.

It is the only component in the repository that is neither an implementation
nor a referee. It is a **witness**: it writes findings and nothing else.

```text
factory/
├── src/                       2,480   the detector, flat on PYTHONPATH
│   ├── cli.py                   133   the one entry point
│   ├── detector_config.py       154   paths, runtime settings, source digest
│   ├── contracts.py             123   reads contracts/, the sole contract reader
│   ├── canonical.py              90   byte-stable JSON and finding identity
│   ├── errors.py                 83   every refusal carries a stable code
│   ├── observations/            921   four read-only channels
│   ├── detection/               106   where do the controls differ
│   ├── attribution/             197   whose fault is it
│   └── findings/                569   model · privacy · writer
│
├── contracts/                 1,556   the detector's OWN contract
│   ├── finding.schema.json      282   what a finding must look like
│   ├── privacy-allowlist.yaml   224   every leaf path a finding may carry
│   ├── scenarios.yaml           127   the five approved scenarios
│   ├── error-codes.yaml          87   the stable refusal vocabulary
│   └── expected/                836   five byte-exact approved findings
│
├── tests/                     1,761   contract · unit · security · end-to-end
└── tools/tree_manifest.py       199   the legacy implementation manifest
```

---

## Two "contracts" folders — do not confuse them

| | `contracts/` (repo root) | `factory/contracts/` |
|---|---|---|
| Governs | The five **file types** | The **finding** the detector emits |
| Read by | legacy, modern, oracles, the factory | the factory only |
| Answers | "what is a correct Type 03 batch?" | "what is a well-formed finding?" |

The factory reads both: the root contracts to know what a batch should have
declared, and its own contract to know what it may say about it.

---

## The pipeline: observe → detect → attribute → publish

**`observations/` — four read-only channels.** Each returns a frozen dataclass,
and the four truth roles stay separate in code because they must stay separate
in the finding:

| Adapter | Channel | Truth role |
|---|---|---|
| `evidence.py` | The legacy evidence packet | Source of observation |
| `postgres.py` | `control.*` via a read-only session | Source of observation |
| `transport.py` | SFTP raw/CSV zone topology | Source of observation |
| *(source manifest)* | `source-manifest.json` | System of record |

`collect.py` binds every channel to the same
`(batch_id, type_number, raw_sha256, manifest_sha256)` tuple before any
comparison runs. A missing, cross-batch, ambiguous, or contradictory
observation set is a **terminal refusal with a stable code**, not a
lower-confidence finding — a partially supported finding is worse than none,
because it looks like evidence.

**`detection/control_mismatch.py`** answers only *where* the numbers differ.
**`attribution/source_system.py`** answers *whose fault it is*, and it must
prove it: the isolation probe re-runs attribution with one channel withheld and
requires the conclusion to change. If the answer survives losing a channel, the
channel was not load-bearing and the attribution is not evidence-based.

**`findings/`** models the finding, scans it against the privacy allowlist, and
writes it as byte-stable canonical JSON. Identity is derived from content, so
the same observations always produce the same finding bytes.

---

## Read-only is proven, not asserted

Four mechanisms, in increasing order of strength:

1. PostgreSQL connects as the non-superuser role and issues
   `SET TRANSACTION READ ONLY` — a write is refused by the server.
2. SFTP authenticates as `operator` and the adapter exposes only `listdir`,
   `stat`, and read-mode `open`. It never constructs the legacy `SftpClient`,
   which has `put`, `rename`, and `remove`.
3. The filesystem is read through a single `_read_bytes` helper.
4. **`tests/security/test_no_write_paths.py` parses every module under
   `src/observations/` with `ast`** and fails on any write-capable call, any
   non-read file mode, or any import of a legacy runtime module.

Only the fourth holds for code that has never been executed, and it is the
actual gate. Note that `operator` is the **widest** SFTP role, not the
narrowest — see [`../infra/README.md`](../infra/README.md).

---

## Why `src/` is flat, and the cost that comes with it

Modules live directly on `PYTHONPATH=factory/src` — `cli`, `contracts`,
`errors`, `observations.collect` — matching the `gen/src/` convention already
used in this repository. There is no intermediate package directory.

**The cost is real and was demonstrated, not theorised.** Flattening put a
module named `config.py` at the top level, where `legacy/runner/config.py` also
lives. The security suite failed within seconds:

```
AssertionError: 'config' unexpectedly found in frozenset({… 'config' …})
  : collect.py imports the legacy runtime module config
```

The AST test asserts that no observation adapter imports a legacy runtime
module *by name* — and with a flat layout it genuinely could not tell the
detector's own `config` from legacy's.

The fix was to **remove the ambiguity, not to weaken the test**: the module is
now `detector_config.py`. There is currently no name shared between
`factory/src/*.py` and `legacy/runner/*.py`.

> **Before adding a top-level module here, check the name against
> `legacy/runner/`, `gen/src/`, and `validation/oracle/`.** A collision does not
> fail loudly at import time — it silently shadows, and the security gate is
> what stands between that and a wrong finding.

---

## The detector's identity is not the folder name

The folder is `factory/`. The detector is still
`northwind-pay-dark-factory-source-control-detector`, and that string is
**unchanged** in `scenarios.yaml`, `privacy-allowlist.yaml`,
`finding.schema.json`, and all five approved findings.

That is deliberate. The identity appears inside findings that have already been
emitted and adjudicated; a directory rename must not retroactively change what
a published finding claims about its own author. Renaming it would also have
meant editing approved expected artifacts, which is never done here. See
this README.

---

## Running it

```bash
make df-check            # contract, unit, and security suites + strict mypy
make df-detect TYPE=01   # detect against a deployed legacy runtime
make df-accept TYPE=all  # the live acceptance gate
make df-manifest         # recompute the legacy implementation manifest
```

Or directly:

```bash
PYTHONPATH=factory/src legacy/runner/.venv/bin/python -m cli \
  --type 01 --legacy-evidence-root .runtime/e2e-evidence
```

The detector runs on the **legacy runner's** virtual environment, not its own.
It observes the legacy runtime and needs the same client libraries; a third
environment would add a resolver without adding isolation.

---

## Known gaps

- **`tests/end-to-end/run_detector_suite.py` (413 lines) is not type-checked.**
  `df-check` runs mypy over `src/` and `tools/tree_manifest.py` only. The
  acceptance suite is the largest untyped file in the component.
- **The end-to-end suite is not part of `df-check`.** It needs a deployed
  legacy runtime, so it lives behind `df-accept`. That is correct, but it means
  `make df-check` passing says nothing about live behaviour.

## What must not change

- **The detector never writes outside `evidence/factory/`.** It has no path to
  `legacy/`, `contracts/`, or `modern/`.
- **The AST security test.** It is the read-only guarantee; every other
  mechanism is defence in depth.
- **The isolation probe must require a complete channel set.** It once passed
  with any one of three channels removed, which made it prove nothing.
- **The detector identity string.** It is contract, not configuration.
