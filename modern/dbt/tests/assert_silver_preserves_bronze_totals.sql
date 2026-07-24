-- Silver conforms; it must not change a monetary total.

with bronze as (
    select batch_id, count(*) as n, sum(amount_brl) as total
    from {{ ref('bronze_card_settlement') }} group by batch_id
),
silver as (
    select batch_id, count(*) as n, sum(amount_brl) as total
    from {{ ref('silver_card_settlement') }} group by batch_id
)
select bronze.batch_id
from bronze
full outer join silver on silver.batch_id = bronze.batch_id
where bronze.n is distinct from silver.n
   or bronze.total is distinct from silver.total
