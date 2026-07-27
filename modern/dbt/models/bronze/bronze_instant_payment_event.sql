{{ config(tags=['type_02']) }}

-- Bronze: typed and source-aligned. Grain: (batch_id, source_record_number).

select
    batch_id,
    source_file,
    cast(source_record_number as integer)      as source_record_number,
    end_to_end_id,
    transaction_id,
    payer_document_token,
    payer_document_masked,
    payee_document_token,
    payee_document_masked,
    event_timestamp,
    cast(amount_brl as decimal(18, 2))         as amount_brl,
    direction,
    status,
    return_code,
    description
from {{ source('landing', 'instant_payment_event') }}
