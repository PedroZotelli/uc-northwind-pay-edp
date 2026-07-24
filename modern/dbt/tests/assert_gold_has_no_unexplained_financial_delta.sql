{{ config(tags=['type_01']) }}

-- The release gate: Gold may not publish an unexplained financial difference.
-- A batch whose declaration disagrees with the computed total never reaches
-- Gold at all, so any non-zero delta here is a modern defect.

select *
from {{ ref('gold_card_settlement_reconciliation') }}
where count_delta <> 0
   or amount_delta <> 0.00
   or status <> 'MATCHED'
