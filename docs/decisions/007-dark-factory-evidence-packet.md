# 007 — Dark Factory evidence packet layout and publication

- Date: 2026-07-24
- Phase: 1, Step 6
- Status: accepted

## Context

Step 6 requires the canonical finding to be written atomically under a separate
Dark Factory evidence root, to include hashes and references rather than copied
raw values, and to be recreatable by a fresh local run with no privacy leak or
legacy mutation.

## Decision

### A separate root, never the legacy tree

Packets are published under `evidence/dark-factory/<batch-id>/`. The legacy
evidence root is opened read-only and is never written to, so a Dark Factory run
cannot alter the observations it is reasoning about. The acceptance suite
hashes the entire legacy evidence tree before and after each run and fails if a
single byte changed — the mutation boundary is measured, not assumed.

### Four files, each with one job

| File | Contents |
|---|---|
| `finding.json` | The canonical finding |
| `detector-run.json` | Detector identity, version, mode, channels consumed and withheld |
| `observation-index.json` | Every channel with its independence class, plus the bound lineage |
| `privacy-scan.json` | Which layers ran and their result |

A rejected or inconclusive run publishes **nothing**. There is no partial packet
and no "finding with problems": the CLI exits with the stable error code and the
evidence root is untouched. An incomplete finding is worse than no finding
because it still looks like evidence.

### Atomicity and immutability

Files are written into a private `0700` temporary directory inside the evidence
root with `open("xb")`, `fchmod(0o600)`, and `fsync`, then the directory is
renamed into place. A reader therefore sees either no packet or a complete one.

Republishing the *same* finding is idempotent and returns the existing packet;
republishing a *different* finding for the same batch raises
`DF-E-EVIDENCE-CONFLICT`. Dark Factory evidence is immutable for the same reason
legacy evidence is: a packet that can be silently rewritten cannot be cited.

### References, not values

The packet stores `sha256:` references to the raw file, the source manifest, the
contract oracle, the detector's own source, and each consumed observation. It
copies no raw row, no restricted value, and no legacy artifact. The observation
references for the live channels are digests over a canonical projection of what
was read, so a later reader can tell whether two runs saw the same state.

## Alternatives considered

- **Publishing under the legacy evidence root**, one packet per batch alongside
  the legacy files. Rejected: it would put detector output inside the tree the
  detector reads, and it would make "legacy evidence unchanged" impossible to
  assert.
- **Writing a finding with `confidence: inconclusive`** when attribution fails,
  rather than refusing. Rejected: the finding schema is a statement of fact
  about ownership; publishing one that says "I could not tell" invites it to be
  cited as though it did.
- **Overwriting on re-run.** Rejected: immutability is what makes a reference to
  a packet meaningful.
- **Copying the legacy evidence packet into the Dark Factory packet** for
  convenience. Rejected: duplication creates a second copy that can drift, and
  the digests already bind the finding to the originals.

## Consequences

- Re-running the detector on an unchanged runtime is safe and idempotent, which
  is what lets the acceptance gate run it repeatedly to prove byte-stability.
- `make clean CONFIRM=clean-runtime` removes `evidence/`, so Dark Factory
  packets are disposable runtime state like every other evidence artifact.
- Proving "no legacy mutation" costs one hash of the legacy evidence tree per
  acceptance run, which is cheap and turns the boundary into a measurement.
