{{ config(tags=['type_01']) }}

-- Silver: conformed entity at the same grain as Bronze.
-- Adds settled direction and a parsed instant; changes no monetary value.

select
    batch_id,
    source_record_number,
    transaction_id,
    merchant_id,
    card_token,
    card_last4,
    cpf_masked,
    cast(transaction_ts as timestamptz)                as transaction_at,
    transaction_ts                                     as transaction_ts_text,
    amount_brl,
    movement_code,
    case movement_code
        when 'P' then 'PURCHASE'
        when 'R' then 'REFUND'
    end                                                as movement_direction,
    authorization_code,
    nsu,
    terminal_id,
    source_file
from {{ ref('bronze_card_settlement') }}
