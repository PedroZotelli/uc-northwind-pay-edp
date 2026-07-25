{{ config(tags=['type_02']) }}

-- Silver splits the signed amount into credit and debit legs, but the signed
-- amount itself must survive untouched.

{{ conserves_totals(
    ref('bronze_instant_payment_event'),
    ref('silver_instant_payment_event'),
    ['amount_brl']
) }}
