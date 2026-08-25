# 14 · Smoke · DF-SOURCE-001

- Slide: Board 5 · Landing — `DF-SOURCE-001` zero Parquet
- Slice: **G · Landing**
- Who: every seat
- Next: [`15-malformed.md`](15-malformed.md)

The lie we kept on Day 1 must still be a lie. The new plant refuses. It does not patch.

## Do

**Not** `make run TYPE=01 SCENARIO=df-source-001` — that is Java. Drive the **modern** handler at:

`spec/type-01-card-settlement/samples/df-source-001.dat`

Trailer **173.44**, rows **173.45**. Keep the declaration. Refuse. Zero Parquet.

## Proof

| Fact | Must be |
|---|---|
| Declaration | **173.44** kept |
| Computed | **173.45** |
| Classification | `SOURCE_CONTROL_TOTAL_MISMATCH` (or the contract’s name) |
| Parquet | **zero** |
| Peers | may continue |

## If fail

Parquet exists on the lie → failed night. Do not rewrite the trailer to 173.45.
