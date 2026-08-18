# Merchant Fee Assessment — inbound pack

**Type `05` · `MER_FEESET05` · `.csv` · semicolon, decimal comma, `HALF_UP`**

Same shape as Types `01`–`04`. The old numbered `01-`…`07-` tree is
gone; this is the customer drop.

| Sample | Role | Expected |
|---|---|---|
| `valid-minimal` | Happy | accepted · assessed `12.36` |
| `valid-boundary` | Boundary | accepted |
| `rounding-half-up` | Type edge | accepted · assessed `0.04` on `3.50` |
| `malformed` | Grammar | `INVALID_CSV_QUOTING` |
| `df-source-005` | Source lie | `SOURCE_CONTROL_ASSESSED_FEE_MISMATCH` · declared `0.99` · computed `1.00` |

Python default rounding is `HALF_EVEN`. This type is **`HALF_UP`**.
Ops mail that says “normal rounding” is not the schedule.

Estate: [`../estate/`](../estate/README.md).
