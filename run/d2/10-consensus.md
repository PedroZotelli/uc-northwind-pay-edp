# 10 · Pass 4 — Consensus

- Slide: Dig · Hands-On C (HUD 21)
- Slice: **D · 2–4**
- Who: a **different** voice, then the owner
- Next: [`11-taskspec.md`](11-taskspec.md)

If they will not sign, **skip 11**. Design is done when the owner signs.

## Do

1. Adversary pass. Every objection **FIXED** or **ACCEPTED**.
2. Walk one contradiction if needed: mail vs inbound vs `contracts/` vs MATCHED. Keep **173.44**.
3. Owner signs. Record: `docs/consensus.md` (who, date, FIXED / ACCEPTED).

```bash
cvg consensus --sign --json
```

If `cvg` is missing, a dated signature in `docs/consensus.md` still counts. If `cvg` wrote elsewhere, copy it here.

## Proof

`docs/consensus.md` exists. Every objection FIXED or ACCEPTED. The room can point at the sign.

## If fail

Unsigned → **do not run 11**. Stay on design. Do not write the parser and sign later.
