{{ config(tags=['type_02']) }}

-- The signed amount is derived exactly once, in ingestion. This proves nothing
-- downstream re-derived it with a different rule.

select *
from {{ ref('silver_instant_payment_event') }}
where (direction = 'C' and amount_brl <= 0)
   or (direction = 'D' and amount_brl >= 0)
