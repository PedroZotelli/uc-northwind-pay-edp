{{ config(tags=['type_05']) }}

-- Privacy: the merchant tax identifier must be masked, never clear.

select *
from {{ ref('bronze_merchant_fee_assessment') }}
where not regexp_matches(merchant_tax_id_masked, '^\*{10}[0-9]{4}$')
   or regexp_matches(description, '[0-9]{11,19}')
