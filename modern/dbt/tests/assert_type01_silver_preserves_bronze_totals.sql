{{ config(tags=['type_01']) }}

-- Silver conforms; it must not change a row count or a monetary total.

{{ conserves_totals(
    ref('bronze_card_settlement'),
    ref('silver_card_settlement'),
    ['amount_brl']
) }}
