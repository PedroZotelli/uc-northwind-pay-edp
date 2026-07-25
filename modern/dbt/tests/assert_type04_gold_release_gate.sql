{{ config(tags=['type_04']) }}

-- Type 04 release gate. Note the count delta is `transfer_count_delta` here,
-- not `count_delta`. `return_count_delta`, `gross_amount_delta`,
-- `return_amount_delta`, and `reject_count` are constants and are deliberately
-- excluded; see modern/README.md, "Constant columns in Gold".

{{ release_gate(ref('gold_ted_transfer_reconciliation'), ['transfer_count_delta', 'net_amount_delta']) }}
