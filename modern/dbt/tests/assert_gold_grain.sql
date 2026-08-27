-- Grain test: Gold is one row per batch per currency.
select batch_id, currency
from {{ ref("type01_gold") }}
group by 1, 2
having count(*) > 1
