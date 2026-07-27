{{ config(tags=['type_03']) }}

-- Silver: conformed settlement at the Bronze grain. The per-settlement net was
-- computed in ingestion as face minus discount plus fee; Silver only types it.

select
    batch_id,
    lot_number,
    sequence,
    settlement_id,
    source_record_number_a,
    source_record_number_b,
    payment_reference_token,
    payment_reference_last4,
    beneficiary_token,
    beneficiary_tax_id_type,
    beneficiary_tax_id_masked,
    bank_account_token,
    bank_account_last4,
    cast(due_date as date)                      as due_date,
    cast(payment_date as date)                  as payment_date,
    face_amount_brl,
    discount_brl,
    fee_brl,
    net_amount_brl,
    face_amount_brl - discount_brl + fee_brl    as recomputed_net_amount_brl,
    status,
    bank_reference,
    client_reference,
    source_file
from {{ ref('bronze_payment_slip_settlement') }}
