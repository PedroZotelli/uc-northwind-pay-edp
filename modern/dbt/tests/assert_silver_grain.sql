-- Grain test: Silver record identity remains batch_id + source_record_number.
select batch_id, source_record_number
from {{ ref("type01_silver") }}
group by 1, 2
having count(*) > 1
