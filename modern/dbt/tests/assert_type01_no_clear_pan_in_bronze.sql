{{ config(tags=['type_01']) }}

-- Privacy: no Bronze column may carry a sixteen-digit clear card number.
-- Structural rather than value-based, so it holds for data it has never seen.

select *
from {{ ref('bronze_card_settlement') }}
where regexp_matches(card_token, '^[0-9]{16}$')
   or regexp_matches(card_last4, '^[0-9]{5,}$')
   or not regexp_matches(card_token, '^tok_[0-9a-f]{24}$')
   or not regexp_matches(cpf_masked, '^\*{7}[0-9]{4}$')
