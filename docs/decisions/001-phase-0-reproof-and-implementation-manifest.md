# 001 — Phase 0 re-proof method and implementation manifest definition

- Date: 2026-07-24
- Phase: 0
- Status: accepted

## Context

`plans/dark-factory.md` requires the committed tree to be re-proven before any
Dark Factory code exists. The 2026-07-24 proof ledger in `plans/legacy.md`
identifies implementation manifest `d3e6e95a…` over 260 files, but that ledger
was produced from working-tree content that preceded the Type `01` parity
refactor. The committed tree carries 268 files, so the recorded manifest hash
cannot be reused and a new one has to be computed with a method that is
reproducible by a later reviewer.

Two further facts had to be settled before the gates could be trusted:

1. The local machine already had a `northwind-pay-legacy` Compose project with
   a populated `sftp_data` volume (143 files, canonical batch IDs already
   consumed) and a Docker build cache entry for the processor image. A gate run
   on that state would have proven nothing about the committed bytes.
2. The host default interpreter is Python 3.14.6, while the repository targets
   Python 3.12 (`mypy --python-version 3.12`, `--strict`).

## Decision

1. **Runtime freshness is established explicitly, never assumed.** Phase 0 ran
   `make clean CONFIRM=clean-runtime` before its first authoritative gate, and
   again between the worker portfolio and the synchronous portfolio. Freshness
   is verified positively — the `sftp_data` volume is asserted to contain zero
   files and PostgreSQL is asserted to apply migrations `001`–`010` from
   scratch — rather than inferred from the clean target's exit code.
2. **The Java regression is proven by execution, not by cache.** `make check`
   reported the processor image as `CACHED`, which means the 78-case Maven
   suite did not run on the committed bytes in this session. Phase 0 therefore
   forced `docker compose build --no-cache processor`, which executed
   `Tests run: 78, Failures: 0, Errors: 0, Skipped: 0`.
3. **The implementation manifest keeps the ledger's published definition.**
   Boundary: root `.dockerignore`, `.env.example`, `Makefile`, `compose.yaml`,
   plus all regular files under `contracts/`, `gen/`, `infra/`, `legacy/`,
   `tests/`, `validation/`. Excluded: `.git`, virtual environments,
   `__pycache__`, `.mypy_cache`, `.pytest_cache`, `target`, `build`, `dist`,
   `node_modules`, `output`, `evidence`, `.runtime`, `*.egg-info`, `.DS_Store`,
   `*.pyc`, `*.pyo`, and symlinks. Relative paths are byte-sorted; each file
   contributes one `{sha256}  {relative_path}\n` record; the manifest hash is
   the SHA-256 of the concatenated records.
4. **The local toolchain pins Python 3.12** by creating the runner virtual
   environment with `PYTHON=python3.12 make init`. Nothing in the repository
   changes; the pin lives in the invocation.

The recomputation is exposed permanently as `make df-manifest`
(`dark-factory/tools/tree_manifest.py`) so any reviewer can reproduce the hash
with one command. That target is additive and does not touch the frozen roots.

## Alternatives considered

- **Reuse the ledger's `d3e6e95a…` hash.** Rejected: it describes a different
  file set (260 vs 268) and would make the ledger self-contradicting.
- **Accept the cached processor image.** Rejected: a cache hit proves the build
  inputs are unchanged relative to some earlier build on this host, not that the
  suite passes on the committed bytes. The mandate asks for a re-proof.
- **Run the gates on the pre-existing dirty runtime.** Rejected outright: the
  canonical batch identities were already consumed, so the acceptance suites
  would have collided with residue from an unrelated session.
- **Rewrite the Makefile to pin the interpreter.** Rejected: `legacy/` and the
  root Make facade are frozen for this run; the pin belongs in the invocation.

## Consequences

- The Phase 0 ledger entry in `plans/legacy.md` records manifest
  `12ce7f449228ae70d4781066b009ce63d5b18e037795ab70c5e0c4e6cd0d0dea` over 268
  files, superseding nothing — it is a second, independently dated proof of a
  different (committed) tree.
- Every later authoritative acceptance in this run inherits rule 1: deploy from
  a wiped runtime and assert emptiness before trusting a result.
- Image identity is environment-bound. The SFTP image reproduced the ledger's
  `55f6da53…` exactly; the processor image did not (`b4ee761a…` vs
  `689ace84…`), which is expected because the processor build embeds the
  changed source tree. Both digests are recorded rather than reconciled.
