-- df-source-001 / 173.44 has zero Parquet, so no Gold row.
select *
from {{ ref("type01_gold") }}
where batch_id = 'B202607230000004'
