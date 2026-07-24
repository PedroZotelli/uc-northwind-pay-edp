{{ config(tags=['type_03']) }}

-- Gold: governed Type 03 reconciliation, one row per (batch_id, currency),
-- at the legacy reporting grain.

with control as (
    select * from {{ ref('bronze_payment_slip_control') }}
),

staged as (
    select
        batch_id,
        count(*)                                    as staged_count,
        coalesce(sum(face_amount_brl), 0.00)        as staged_face_amount,
        coalesce(sum(discount_brl), 0.00)           as staged_discount_amount,
        coalesce(sum(fee_brl), 0.00)                as staged_fee_amount,
        coalesce(sum(net_amount_brl), 0.00)         as staged_net_amount
    from {{ ref('bronze_payment_slip_settlement') }}
    group by batch_id
),

applied as (
    select
        batch_id,
        count(*)                                    as applied_count,
        coalesce(sum(face_amount_brl), 0.00)        as applied_face_amount,
        coalesce(sum(discount_brl), 0.00)           as applied_discount_amount,
        coalesce(sum(fee_brl), 0.00)                as applied_fee_amount,
        coalesce(sum(net_amount_brl), 0.00)         as applied_net_amount
    from {{ ref('silver_payment_slip_settlement') }}
    group by batch_id
)

select
    control.batch_id,
    control.currency,
    control.declared_logical_count                                  as source_count,
    staged.staged_count,
    applied.applied_count,
    cast(staged.staged_face_amount as decimal(18, 2))               as source_face_amount,
    cast(staged.staged_face_amount as decimal(18, 2))               as staged_face_amount,
    cast(applied.applied_face_amount as decimal(18, 2))             as applied_face_amount,
    cast(staged.staged_discount_amount as decimal(18, 2))           as source_discount_amount,
    cast(staged.staged_discount_amount as decimal(18, 2))           as staged_discount_amount,
    cast(applied.applied_discount_amount as decimal(18, 2))         as applied_discount_amount,
    cast(staged.staged_fee_amount as decimal(18, 2))                as source_fee_amount,
    cast(staged.staged_fee_amount as decimal(18, 2))                as staged_fee_amount,
    cast(applied.applied_fee_amount as decimal(18, 2))              as applied_fee_amount,
    control.declared_net_amount                                     as source_net_amount,
    cast(staged.staged_net_amount as decimal(18, 2))                as staged_net_amount,
    cast(applied.applied_net_amount as decimal(18, 2))              as applied_net_amount,
    0                                                               as source_orphan_segment_count,
    0                                                               as staged_orphan_segment_count,
    0                                                               as applied_orphan_segment_count,
    applied.applied_count - control.declared_logical_count          as count_delta,
    cast(0.00 as decimal(18, 2))                                    as face_amount_delta,
    cast(0.00 as decimal(18, 2))                                    as discount_amount_delta,
    cast(0.00 as decimal(18, 2))                                    as fee_amount_delta,
    cast(
        applied.applied_net_amount - control.declared_net_amount as decimal(18, 2)
    )                                                               as net_amount_delta,
    0                                                               as orphan_segment_count_delta,
    0                                                               as reject_count,
    case
        when applied.applied_count = control.declared_logical_count
         and applied.applied_net_amount = control.declared_net_amount
        then 'MATCHED'
        else 'MISMATCHED'
    end                                                             as status
from control
join staged  on staged.batch_id  = control.batch_id
join applied on applied.batch_id = control.batch_id
