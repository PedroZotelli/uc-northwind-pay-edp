# 11 · Pass 5 — Task-Spec

- Slide: Dig · Show · Task-Spec, then Hands-On D (HUD 22–23)
- Slice: **E · Task-Spec**
- Who: instructor authors the first leaf in public, then every seat
- Next: HUD **24** Show · Task-Mesh (no typing), then [`12-research.md`](12-research.md)

Show first. Skip this beat if Consensus is unsigned. No eval, no build. `signed_off` starts **false**. No product code tonight.

## Prompt (verbatim)

```text
You are Pass 5 Tasking on NorthWind Pay.
Author one Type 01 leaf for ingest → landing (parser or writer — one leaf).
Write it under docs/tasks/.
The eval must be runnable.

The leaf must require:
- Exact Decimal
- Privacy at parse (PAN token + last4, CPF mask)
- Deterministic Parquet under modern/landing/ (when the mesh later runs)
- No write to frozen folders

Do not write modern/ product code tonight.
Do not change frozen folders.
```

```bash
mkdir -p docs/tasks
cvg tasking --draft --json
```

If `cvg` wrote under `cvg/docs/`, move the leaf into `docs/tasks/`.

## Proof

A Task-Spec exists under `docs/tasks/`. It has an eval. `signed_off` is false. No `modern/` required tonight.

## If fail

No eval → tear it up. Do not Loop. HUD 24 Task-Mesh is Show — internals, not a license to write Parquet.
