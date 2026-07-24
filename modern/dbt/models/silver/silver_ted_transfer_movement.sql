{{ config(tags=['type_04']) }}

-- Silver: conformed movement at the Bronze grain. Signs are already correct.

select
    batch_id,
    source_record_number,
    movement_id,
    nullif(original_transfer_id, '')                    as original_transfer_id,
    movement_kind,
    cast(movement_ts as timestamptz)                    as movement_at,
    movement_ts                                         as movement_ts_text,
    amount_brl,
    payer_account_token,
    payer_tax_id_masked,
    beneficiary_account_token,
    beneficiary_tax_id_masked,
    beneficiary_ispb,
    purpose_code,
    status_code,
    nullif(return_reason_code, '')                      as return_reason_code,
    source_file
from {{ ref('bronze_ted_transfer_movement') }}
