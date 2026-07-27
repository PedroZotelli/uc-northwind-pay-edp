{{ config(tags=['type_02']) }}

-- Silver: conformed event at the Bronze grain. The signed amount was derived
-- exactly once in ingestion; Silver only classifies it.

select
    batch_id,
    source_record_number,
    end_to_end_id,
    transaction_id,
    payer_document_token,
    payer_document_masked,
    payee_document_token,
    payee_document_masked,
    cast(event_timestamp as timestamptz)                as event_at,
    event_timestamp                                     as event_timestamp_text,
    amount_brl,
    direction,
    case when amount_brl > 0 then amount_brl else 0.00 end   as credit_amount,
    case when amount_brl < 0 then -amount_brl else 0.00 end  as debit_amount,
    status,
    return_code,
    description,
    source_file
from {{ ref('bronze_instant_payment_event') }}
