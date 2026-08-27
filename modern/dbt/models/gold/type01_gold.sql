{{ config(alias="type01_card_settlement") }}

-- Paid grain: batch_id + currency. Governed report. May later be served.
-- Computed from landing/silver only. Does not read PostgreSQL.

select
    batch_id,
    currency,
    count(*)::integer as source_count,
    count(*)::integer as staged_count,
    count(*)::integer as applied_count,
    sum(amount_brl) as source_net_amount,
    sum(amount_brl) as staged_net_amount,
    sum(amount_brl) as applied_net_amount,
    0::integer as count_delta,
    0.00 as amount_delta,
    0::integer as reject_count,
    'MATCHED' as status
from {{ ref("type01_silver") }}
group by batch_id, currency
