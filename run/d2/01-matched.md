# 01 · The plant still MATCHED

- Slide: Board 1 · Recap — this file is the clock (HUD not signed)
- Slice: **A · Yesterday**
- Who: instructor first, room confirms
- Next: [`02-review-capture.md`](02-review-capture.md)

The Night starts where Day 1 stopped. If the plant is down, do not translate.

## Do

```bash
make status
```

If they need the receipt again, **terminal** (not the Git sidebar):

```bash
cat evidence/B202607230000001/reconciliation.json
```

Do not `make run` again unless the packet is missing. Canonical IDs are immutable.

## Proof

Postgres + four SFTP roles **healthy**. Status **MATCHED**. Net **173.45**. Delta **0.00**.

## If fail

Unhealthy → stop. Missing evidence (fresh worktree) → boot the plant first: [`../d1/05-boot.md`](../d1/05-boot.md) then [`../d1/08-prompt-make-run.md`](../d1/08-prompt-make-run.md). Do not start Bind on a dead plant. Do not share Compose ports with another checkout.
