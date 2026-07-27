{{ config(tags=['type_01']) }}

-- Type 01 release gate. `reject_count` is a constant and is deliberately
-- excluded; see modern/README.md, "Constant columns in Gold".

{{ release_gate(ref('gold_card_settlement_reconciliation'), ['count_delta', 'amount_delta']) }}
