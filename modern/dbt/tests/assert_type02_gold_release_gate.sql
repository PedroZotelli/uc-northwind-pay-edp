{{ config(tags=['type_02']) }}

-- Type 02 release gate. `credit_amount_delta`, `debit_amount_delta`,
-- `returned_count_delta`, and `reject_count` are constants and are
-- deliberately excluded; see modern/README.md, "Constant columns in Gold".

{{ release_gate(ref('gold_instant_payment_reconciliation'), ['count_delta', 'net_amount_delta']) }}
