{{ config(tags=['type_03']) }}

-- Bronze: typed and source-aligned. Grain: one logical settlement, which is an
-- adjacent A/B segment pair, keyed (batch_id, lot_number, sequence).

select
    batch_id,
    source_file,
    cast(source_record_number_a as integer)    as source_record_number_a,
    cast(source_record_number_b as integer)    as source_record_number_b,
    lot_number,
    sequence,
    settlement_id,
    payment_reference_token,
    payment_reference_last4,
    beneficiary_token,
    beneficiary_tax_id_type,
    beneficiary_tax_id_masked,
    bank_account_token,
    bank_account_last4,
    due_date,
    payment_date,
    cast(face_amount_brl as decimal(18, 2))    as face_amount_brl,
    cast(discount_brl as decimal(18, 2))       as discount_brl,
    cast(fee_brl as decimal(18, 2))            as fee_brl,
    cast(net_amount_brl as decimal(18, 2))     as net_amount_brl,
    status,
    bank_reference,
    client_reference
from {{ source('landing', 'payment_slip_settlement') }}
