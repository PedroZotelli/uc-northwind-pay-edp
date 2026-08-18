# Instructor key — planted inbound issues

Not for the room. The student packs do not list these.

| Type | Where | What they should notice |
|---|---|---|
| Estate | Marina mail; 7 Jul walk-through | Source lies are kept, not patched. Nouns drift (“settlement total”, “the fee”). |
| `01` | May vs Jul proc; `chargeback_flag`; Marina “settlement total” | Use the Jul proc. Dead column. Layout name is **net amount**. |
| `02` | Rafael “pipes are never escaped”; `event_memo` | `escaped-content` sample exists. Dead column. |
| `03` | “240 usually” + pad; `lot_remark` | Layout is exact 240 + CRLF. Dead column. |
| `04` | April proc drops returns; “RT is optional” | June proc is current. Layout requires `R` after `RT`. |
| `05` | “normal rounding” vs schedule | `HALF_UP`. `rounding-half-up` sample is the proof. |

`contracts/` is never wrong on purpose. If inbound disagrees with
`expected/`, the oracle wins.
