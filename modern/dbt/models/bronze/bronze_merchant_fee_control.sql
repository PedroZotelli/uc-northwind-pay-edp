{{ config(tags=['type_05']) }}

-- Bronze controls for Type 05: the source declaration and computed totals.

select
    batch_id,
    type_number,
    contract_code,
    currency,
    cast(declared_detail_count as integer)          as declared_row_count,
    cast(computed_detail_count as integer)          as computed_row_count,
    cast(declared_net_amount as decimal(18, 2))     as declared_assessed_fee,
    cast(computed_net_amount as decimal(18, 2))     as computed_assessed_fee,
    cast(record_count as integer)                   as record_count,
    raw_sha256,
    parquet_sha256,
    source_file
from {{ source('landing', 'merchant_fee_assessment_control') }}
