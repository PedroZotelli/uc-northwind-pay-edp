# 07 · Packet + Type 01 Dagster hash

- Slide: Execute 06–07 (Hands-On **slice c · loop**) — tile 07
- Slice: **C · Loop**
- Who: instructor first, then every seat
- Next: [`08-type05-unattended.md`](08-type05-unattended.md) on Execute 08–09

Telemetry is the packet. Dagster is lineage — **not** the parser. Skip the hash look-up if Type 01 Gold is missing; the packet from tile 06 still counts.

## Prompt (verbatim)

```text
Look up the packet from the leaf you just cranked (terminal, not Git).
Name: leaf, attempt, eval, exit, classification or skip, paths.

If Type 01 Gold exists on disk:
- Direct rebuild from landing and orchestrated (Dagster) must hash the same Gold.
- Parsing does not move into the orchestrator.
If Gold is missing, say so and stop the hash — do not stand up Dagster to look busy.

Do not serve unresolved Gold.
Do not write FastAPI unless the ADR for 0006 row 9 is signed and Gold is approved.
```

## Proof

Packet restatable with files closed. If Gold exists: direct and orchestrated **same hash**. Parsing still in the plant.

## If fail

No packet → go back to [`06-mesh-crank.md`](06-mesh-crank.md). Dagster that parses → **stop**. FastAPI on unresolved Gold → tear it up.
