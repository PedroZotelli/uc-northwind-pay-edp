# 12 · Pass 5 — Tasking (one leaf, one eval)

- Slide: Board 5 · Landing — one leaf, one eval, `docs/tasks/`
- Slice: **G · Landing**
- Who: instructor authors the first leaf in public, then every seat
- Next: [`13-loop-valid.md`](13-loop-valid.md)

Task-Spec attaches here. No eval, no build. `signed_off` starts **false**.

## Do

Author one Type `01` leaf for ingest → landing (parser **or** writer — one leaf). Write it under **`docs/tasks/`**. The eval must be runnable. See [`docs/README.md`](../../docs/README.md).

The leaf must require:

- Exact Decimal
- Privacy at parse (PAN token + last4, CPF mask)
- Deterministic Parquet under `modern/landing/`
- No write to frozen folders (Bind still on)

```bash
mkdir -p docs/tasks
cvg tasking --draft --json
```

If `cvg` wrote under `cvg/docs/`, move the leaf into `docs/tasks/`.

## Proof

A Task-Spec file exists under `docs/tasks/`. It has an eval. `signed_off` is false. No product code yet.

## If fail

A leaf with no eval → tear it up. Do not Loop.
