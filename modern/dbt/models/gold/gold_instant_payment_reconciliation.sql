{{ config(tags=['type_02']) }}

-- Gold: governed Type 02 reconciliation, one row per (batch_id, currency),
-- at the legacy reporting grain.
--
-- CONSTANT COLUMNS: `credit_amount_delta`, `debit_amount_delta`,
-- `returned_count_delta`, and `reject_count` are literals, and
-- `source_credit_amount` / `source_debit_amount` / `source_returned_count` are
-- aliases of their `staged_*` counterparts — so those pairs are self-equal by
-- construction. They exist so the grain matches the legacy report. Never
-- assert on them. Real deltas are `count_delta` and `net_amount_delta`.

with control as (
    select * from {{ ref('bronze_instant_payment_control') }}
),

staged as (
    select
        batch_id,
        count(*)                                                     as staged_count,
        coalesce(sum(case when amount_brl > 0 then amount_brl else 0.00 end), 0.00) as staged_credit_amount,
        coalesce(sum(case when amount_brl < 0 then -amount_brl else 0.00 end), 0.00) as staged_debit_amount,
        coalesce(sum(amount_brl), 0.00)                              as staged_net_amount,
        count(*) filter (where status = 'RETURNED')                  as staged_returned_count
    from {{ ref('bronze_instant_payment_event') }}
    group by batch_id
),

applied as (
    select
        batch_id,
        count(*)                                        as applied_count,
        coalesce(sum(credit_amount), 0.00)              as applied_credit_amount,
        coalesce(sum(debit_amount), 0.00)               as applied_debit_amount,
        coalesce(sum(amount_brl), 0.00)                 as applied_net_amount,
        count(*) filter (where status = 'RETURNED')     as applied_returned_count
    from {{ ref('silver_instant_payment_event') }}
    group by batch_id
)

select
    control.batch_id,
    control.currency,
    control.declared_event_count                                    as source_count,
    staged.staged_count,
    applied.applied_count,
    cast(staged.staged_credit_amount as decimal(18, 2))             as source_credit_amount,
    cast(staged.staged_credit_amount as decimal(18, 2))             as staged_credit_amount,
    cast(applied.applied_credit_amount as decimal(18, 2))           as applied_credit_amount,
    cast(staged.staged_debit_amount as decimal(18, 2))              as source_debit_amount,
    cast(staged.staged_debit_amount as decimal(18, 2))              as staged_debit_amount,
    cast(applied.applied_debit_amount as decimal(18, 2))            as applied_debit_amount,
    control.declared_net_amount                                     as source_net_amount,
    cast(staged.staged_net_amount as decimal(18, 2))                as staged_net_amount,
    cast(applied.applied_net_amount as decimal(18, 2))              as applied_net_amount,
    staged.staged_returned_count                                    as source_returned_count,
    staged.staged_returned_count,
    applied.applied_returned_count,
    applied.applied_count - control.declared_event_count            as count_delta,
    cast(0.00 as decimal(18, 2))                                    as credit_amount_delta,
    cast(0.00 as decimal(18, 2))                                    as debit_amount_delta,
    cast(
        applied.applied_net_amount - control.declared_net_amount as decimal(18, 2)
    )                                                               as net_amount_delta,
    0                                                               as returned_count_delta,
    0                                                               as reject_count,
    case
        when applied.applied_count = control.declared_event_count
         and applied.applied_net_amount = control.declared_net_amount
        then 'MATCHED'
        else 'MISMATCHED'
    end                                                             as status
from control
join staged  on staged.batch_id  = control.batch_id
join applied on applied.batch_id = control.batch_id
