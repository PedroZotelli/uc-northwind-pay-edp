{{ config(tags=['type_03']) }}

-- Type 03 release gate. `face_amount_delta`, `discount_amount_delta`,
-- `fee_amount_delta`, `orphan_segment_count_delta`, and `reject_count` are
-- constants and are deliberately excluded; see modern/README.md, "Constant
-- columns in Gold". Per-settlement arithmetic is covered separately by
-- assert_type03_privacy_and_net.

{{ release_gate(ref('gold_payment_slip_reconciliation'), ['count_delta', 'net_amount_delta']) }}
