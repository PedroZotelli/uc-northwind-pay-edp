# 01 · Prompt — make status

- Slide: Stage · Recap · closed (HUD 03)
- Slice: **A · Recap**
- Who: every seat, through **their** agent
- Next: [`02-prompt-papers.md`](02-prompt-papers.md)

Opening + Stage divider (HUD 01–02) are already on the deck. Recap receipts are HUD 03. SWE / java2py / ingest (HUD 05–10) come **after** beat 02 — you talk; they do not type.

## Prompt (verbatim)

```text
Do not change any file.
Run make status.
Then open evidence/B202607230000001/reconciliation.json in the terminal (not Git).
From the files, not from memory:
1. Are Postgres and the four SFTP roles healthy?
2. What is status, source_net_amount, applied_net_amount, amount_delta?
3. What does MATCHED mean on this plant?

Do not make run unless that evidence file is missing.
Do not write any file.
```

## Proof

1. Healthy.
2. **MATCHED** · **173.45** · **173.45** · **0.00**.
3. Source, stage, and books agree to the cent.

## If fail

Unhealthy → stop. Missing packet → [`../d1/05-boot.md`](../d1/05-boot.md) then [`../d1/08-prompt-make-run.md`](../d1/08-prompt-make-run.md). They open `reconciliation.json` themselves. Do not share Compose (`northwind-pay-legacy`, port 2222) with another checkout.
