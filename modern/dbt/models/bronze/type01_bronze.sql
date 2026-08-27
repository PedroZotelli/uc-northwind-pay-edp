{{ config(alias="type01_card_settlement") }}

-- Source-aligned to landing. Grain: batch_id + source_record_number.
-- Does not re-parse raw. Does not retokenize PAN/CPF.

select
    batch_id,
    source_file,
    source_record_number,
    transaction_id,
    merchant_id,
    card_token,
    card_last4,
    cpf_masked,
    transaction_ts,
    amount_brl,
    movement_code,
    authorization_code,
    nsu,
    terminal_id
from {{ source("landing", "type01_card_settlement") }}
