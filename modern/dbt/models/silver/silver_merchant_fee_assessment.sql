{{ config(tags=['type_05']) }}

-- Silver: conformed assessment at the same grain as Bronze. Changes no money.

select
    batch_id,
    source_record_number,
    assessment_id,
    merchant_id,
    merchant_tax_id_masked,
    fee_code,
    description,
    gross_amount_brl,
    rate_percent,
    assessed_fee_brl,
    calculated_fee_brl,
    cast(assessment_date as date)                       as assessment_date,
    rounding_mode,
    assessed_fee_brl - calculated_fee_brl               as assessment_calculation_delta,
    source_file
from {{ ref('bronze_merchant_fee_assessment') }}
