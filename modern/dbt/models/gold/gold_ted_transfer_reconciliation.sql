{{ config(tags=['type_04']) }}

-- Gold: governed Type 04 reconciliation, one row per (batch_id, currency),
-- at the legacy reporting grain. Transfers and returns are counted separately
-- because the contract's controls distinguish them.

with control as (
    select * from {{ ref('bronze_ted_transfer_control') }}
),

staged as (
    select
        batch_id,
        count(*) filter (where movement_kind = 'TRANSFER')  as staged_transfer_count,
        count(*) filter (where movement_kind = 'RETURN')    as staged_return_count,
        coalesce(sum(amount_brl) filter (where movement_kind = 'TRANSFER'), 0.00) as staged_gross_amount,
        coalesce(sum(amount_brl) filter (where movement_kind = 'RETURN'), 0.00)   as staged_return_amount,
        coalesce(sum(amount_brl), 0.00)                     as staged_net_amount
    from {{ ref('bronze_ted_transfer_movement') }}
    group by batch_id
),

applied as (
    select
        batch_id,
        count(*) filter (where movement_kind = 'TRANSFER')  as applied_transfer_count,
        count(*) filter (where movement_kind = 'RETURN')    as applied_return_count,
        coalesce(sum(amount_brl) filter (where movement_kind = 'TRANSFER'), 0.00) as applied_gross_amount,
        coalesce(sum(amount_brl) filter (where movement_kind = 'RETURN'), 0.00)   as applied_return_amount,
        coalesce(sum(amount_brl), 0.00)                     as applied_net_amount
    from {{ ref('silver_ted_transfer_movement') }}
    group by batch_id
)

select
    control.batch_id,
    control.currency,
    control.declared_transfer_count                                 as source_transfer_count,
    staged.staged_transfer_count,
    applied.applied_transfer_count,
    staged.staged_return_count                                      as source_return_count,
    staged.staged_return_count,
    applied.applied_return_count,
    cast(staged.staged_gross_amount as decimal(18, 2))              as source_gross_amount,
    cast(staged.staged_gross_amount as decimal(18, 2))              as staged_gross_amount,
    cast(applied.applied_gross_amount as decimal(18, 2))            as applied_gross_amount,
    cast(staged.staged_return_amount as decimal(18, 2))             as source_return_amount,
    cast(staged.staged_return_amount as decimal(18, 2))             as staged_return_amount,
    cast(applied.applied_return_amount as decimal(18, 2))           as applied_return_amount,
    control.declared_net_amount                                     as source_net_amount,
    cast(staged.staged_net_amount as decimal(18, 2))                as staged_net_amount,
    cast(applied.applied_net_amount as decimal(18, 2))              as applied_net_amount,
    applied.applied_transfer_count - control.declared_transfer_count as transfer_count_delta,
    0                                                               as return_count_delta,
    cast(0.00 as decimal(18, 2))                                    as gross_amount_delta,
    cast(0.00 as decimal(18, 2))                                    as return_amount_delta,
    cast(
        applied.applied_net_amount - control.declared_net_amount as decimal(18, 2)
    )                                                               as net_amount_delta,
    0                                                               as reject_count,
    case
        when applied.applied_transfer_count = control.declared_transfer_count
         and applied.applied_net_amount = control.declared_net_amount
        then 'MATCHED'
        else 'MISMATCHED'
    end                                                             as status
from control
join staged  on staged.batch_id  = control.batch_id
join applied on applied.batch_id = control.batch_id
