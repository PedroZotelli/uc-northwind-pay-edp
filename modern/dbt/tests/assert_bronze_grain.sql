-- Grain test: Bronze is unique on batch_id + source_record_number.
select batch_id, source_record_number
from {{ ref("type01_bronze") }}
group by 1, 2
having count(*) > 1
