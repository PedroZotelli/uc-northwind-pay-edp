# 04 · First write & independence

- Slide: Board 2 · Picture — first write is Parquet, not SFTP
- Slice: **B · Picture**
- Who: instructor draws, room looks — keyboards down until 05
- Next: [`05-brain-java.md`](05-brain-java.md)

This is Day 1’s “use-case & structure” for the **second** plant. Draw it. Do not code it yet.

## Do

Draw both first writes:

```text
Legacy (already MATCHED):
  SFTP raw/incoming → Java 21 → SFTP csv/outgoing → Postgres

Modern (tonight, after the sign):
  same SFTP raw/incoming
    → Python (model → parser → schema → writer → handler)
    → modern/landing/ Parquet + readiness manifest
```

Say out loud:

- **First write** = where the new plant first puts bytes. Ours is Parquet in `modern/landing/`.
- **Independence** = same raw bytes. No Java import. No stored-proc reuse. No CSV-as-input. No Parquet back onto SFTP.
- Event-driven tonight = sense the drop, claim the batch, emit Parquet. Not a bus. Not Dagster.

## Proof

The room can point at two destinations and not mix them. `modern/` still does not exist — that is correct until Consensus.

## If fail

Someone says “we wrap the Java CSV” → stop. That is not a second plant.
