{{ config(tags=['type_04']) }}

-- Silver nulls two empty-string columns and parses an instant; no money moves.

{{ conserves_totals(
    ref('bronze_ted_transfer_movement'),
    ref('silver_ted_transfer_movement'),
    ['amount_brl']
) }}
