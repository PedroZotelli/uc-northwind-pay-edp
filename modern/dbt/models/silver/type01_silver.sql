{{ config(alias="type01_card_settlement") }}

-- Conformed grain. Record identity remains batch_id + source_record_number.
-- Paid / batch grain is batch_id + currency (BRL). Privacy columns pass through.

select
    batch_id,
    source_file,
    source_record_number,
    transaction_id,
    merchant_id,
    card_token,
    card_last4,
    cpf_masked,
    cast(transaction_ts as timestamptz) as transaction_ts,
    amount_brl,
    case
        when amount_brl > 0 then 1
        when amount_brl < 0 then -1
        else 0
    end as amount_sign,
    movement_code,
    authorization_code,
    nsu,
    terminal_id,
    'BRL' as currency
from {{ ref("type01_bronze") }}
