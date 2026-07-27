# 005 — Read-only observation adapters and refusal rules

- Date: 2026-07-24
- Phase: 1, Step 2
- Status: accepted

## Context

Step 2 requires reading the source manifest and legacy evidence without
mutation, validating exact batch/type/hash lineage, and refusing missing,
cross-batch, ambiguous, or contradictory observation sets. Its gate is that
"no adapter has a write path to SFTP, PostgreSQL, legacy evidence, or
contracts" — a statement about the code, not about the run.

## Decision

### Four channels, four adapters, four roles

| Adapter | Channel | Truth role |
|---|---|---|
| `observations.source` | `source-manifest.json` in the evidence packet | System of record |
| `observations.evidence` | The rest of the legacy evidence packet | Source of observation |
| `observations.postgres` | `control.*` via a read-only session | Source of observation |
| `observations.transport` | SFTP raw/CSV zone topology | Source of observation |
| `observations.contract` | `contracts/types/**` and the Dark Factory contract | Source of correctness |

Each adapter returns a frozen dataclass. The roles stay separate in code because
they have to stay separate in the finding; merging them in an adapter would make
the separation in the output cosmetic.

### Proving read-only rather than asserting it

Four mechanisms, in increasing order of strength:

1. **PostgreSQL** connects as the non-superuser application role and issues
   `SET TRANSACTION READ ONLY` before its first statement, so a write is refused
   by the server, not by the client.
2. **SFTP** authenticates as the `operator` role and the adapter exposes only
   `listdir`/`stat`/`open(mode="r")`. It never constructs a legacy
   `SftpClient`, which has `put`, `rename`, and `remove`.

   To be precise about what this does *not* buy: `operator` is the **widest**
   SFTP role, not the narrowest. It holds group write on all eight zones
   (`2770`) because the archive step needs it, and it is chosen here only
   because it is the one role that can *see* every zone. The read-only
   guarantee therefore rests on mechanism 4 below — the AST test — and not on
   the operating system. An OS-enforced version would need a fifth role with
   read-only zone membership; see [`infra/README.md`](../../infra/README.md).
3. **The filesystem** is read through a single `_read_bytes` helper; nothing in
   `darkfactory.observations` opens a path for writing, and no module in the
   package imports `os.remove`, `shutil`, or `Path.write_*`.
4. **A source-level security test** parses every module under
   `dark-factory/src/darkfactory/observations/` with `ast` and fails if any
   write-capable call, any file open with a non-read mode, or any import of a
   legacy runtime module appears. This is the gate: it holds for code that has
   never been executed, including future code.

### Refusal rules

The adapter set refuses, with a stable code, when:

- an observation channel is absent or unreadable — `DF-E-OBSERVATION-MISSING`;
- any observation names a different batch than the one requested —
  `DF-E-CROSS-BATCH-OBSERVATION`;
- more than one candidate observation exists for one channel —
  `DF-E-AMBIGUOUS-OBSERVATION`;
- the raw hash, manifest hash, batch identity, or type identity disagree across
  channels — `DF-E-LINEAGE-CONFLICT`;
- two channels report different values for the same control —
  `DF-E-CONTRADICTORY-OBSERVATION`.

Refusal is terminal for that batch and produces no finding. A partially
supported finding is worse than no finding, because it looks like evidence.

### Lineage validation

Every channel is bound to the same `(batch_id, type_number, raw_sha256,
manifest_sha256)` tuple before any comparison runs. The raw hash is checked
against the source manifest, the intake observation, the publication
observation, and the live `control.batches` row; the manifest hash against the
intake observation and `control.batches`. This is what makes the finding's
references meaningful rather than decorative.

## Alternatives considered

- **Reuse `legacy/runner/sftp_client.py` and `legacy/postgres/loader_common.py`.**
  Rejected: both carry write paths, so the Step 2 gate would become a promise
  about how they are called.
- **A read-only database role created for the detector.** Rejected for this
  slice: it would require a new migration, and migrations are frozen. The
  read-only transaction on the existing non-superuser role gives server-side
  enforcement without touching frozen truth. Worth revisiting if the detector
  ever needs its own credentials.
- **Tolerating a missing channel and lowering confidence.** Rejected here and
  used deliberately in the opposite direction by
  [DR-006](006-evidence-based-attribution.md): a *missing* channel is a refusal,
  while a *withheld* channel in the isolation probe is what proves the
  attribution depends on it.

## Consequences

- The detector cannot run against a partially torn-down runtime, which is
  correct: its findings are claims about a specific observed state.
- The security suite's AST check is the artifact that makes "read-only"
  reviewable in a few seconds, and it will fail loudly if a later slice reaches
  for a convenient write.
