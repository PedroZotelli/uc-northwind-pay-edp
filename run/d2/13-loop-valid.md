# 13 · Pass 8 — Loop · valid-minimal

- Slide: Board 5 · Landing — `valid-minimal` Parquet
- Slice: **G · Landing**
- Who: every seat, through **their** bound agent
- Next: [`14-df-source.md`](14-df-source.md)

Attempt → eval → learn. Eval is done, not attempt-count. Bind stays on.

## Do

**Not** `make run`. That is the frozen Java plant. Drive the **signed leaf** through the bound agent / the Type `01` handler.

Input: `spec/type-01-card-settlement/samples/valid-minimal.dat`

Loop until:

- Five-file package exists under `modern/ingestion/` (or the path the ADR named)
- Deterministic Parquet + readiness under `modern/landing/`
- Replay of the same sample produces the same bytes

```bash
# shape — cvg loop / bound agent against the sample, not javac, not make run
ls modern/landing/
```

## Proof

Parquet on disk. Replay identical. Frozen folders untouched. `signed_off` may flip **only** because the eval passed.

## If fail

Agent wrote `legacy/` → Bind failed. Stop. Do not “fix Java to go green.”
