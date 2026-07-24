{{ config(tags=['type_04']) }}

-- Bronze: typed and source-aligned. Grain: (batch_id, source_record_number).

select
    batch_id,
    source_file,
    cast(source_record_number as integer)      as source_record_number,
    movement_id,
    original_transfer_id,
    movement_kind,
    movement_ts,
    cast(amount_brl as decimal(18, 2))         as amount_brl,
    payer_account_token,
    payer_tax_id_masked,
    beneficiary_account_token,
    beneficiary_tax_id_masked,
    beneficiary_ispb,
    purpose_code,
    status_code,
    return_reason_code
from {{ source('landing', 'ted_transfer_movement') }}
