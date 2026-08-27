-- valid-minimal Gold: net 173.45, MATCHED, BRL. Not copied from Postgres.
select *
from {{ ref("type01_gold") }}
where batch_id = 'B202607230000001'
  and (
      currency <> 'BRL'
      or applied_count <> 2
      or applied_net_amount <> 173.45
      or amount_delta <> 0
      or status <> 'MATCHED'
  )
