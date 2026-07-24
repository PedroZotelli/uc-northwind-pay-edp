{{ config(tags=['type_04']) }}

select *
from {{ ref('silver_ted_transfer_movement') }}
where (movement_kind = 'TRANSFER' and amount_brl <= 0)
   or (movement_kind = 'RETURN' and amount_brl >= 0)
