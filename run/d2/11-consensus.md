# 11 · Pass 4 — Consensus (the barrier)

- Slide: Board 4 · Barrier — Pass 4 sign into `docs/consensus.md`
- Slice: **F · Barrier**
- Who: a **different** voice (another table, or a second agent family), then the owner
- Next: [`12-tasking.md`](12-tasking.md)

If they will not sign, **skip slice G**. An unsigned tech-spec is still not a license. Design is done when the owner signs, not when the slide looks complete.

## Do

1. Adversary pass. Every objection is **FIXED** or **ACCEPTED**. No silent skip.
2. Walk one contradiction in public if it is not already on the board: estate mail vs Type `01` inbound vs `contracts/` vs MATCHED. Keep **173.44**.
3. Owner signs. The record lives at **`docs/consensus.md`** (who, date, FIXED / ACCEPTED). See [`docs/README.md`](../../docs/README.md).

```bash
cvg consensus --sign --json
```

If `cvg` is missing, a dated signature in `docs/consensus.md` still counts. If `cvg` wrote elsewhere, copy the sign into `docs/consensus.md`.

## Proof

`docs/consensus.md` exists. Every objection FIXED or ACCEPTED. The room can point at the sign.

## If fail

Unsigned → **do not run 12–15**. Stay on design. Do not “just write the parser and sign later.”
