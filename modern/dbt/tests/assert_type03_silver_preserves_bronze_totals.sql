{{ config(tags=['type_03']) }}

-- Type 03 carries four money columns to Silver. All four must survive, not
-- only the net: a compensating error across face, discount, and fee would
-- leave the net correct and every component wrong.

{{ conserves_totals(
    ref('bronze_payment_slip_settlement'),
    ref('silver_payment_slip_settlement'),
    ['face_amount_brl', 'discount_brl', 'fee_brl', 'net_amount_brl']
) }}
