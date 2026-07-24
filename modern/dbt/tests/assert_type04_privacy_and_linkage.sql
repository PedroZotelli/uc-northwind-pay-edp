{{ config(tags=['type_04']) }}

-- Privacy and linkage: accounts tokenized, tax identifiers masked, a return
-- always names its transfer, and a transfer never carries a reason code.

select *
from {{ ref('bronze_ted_transfer_movement') }}
where not regexp_matches(payer_account_token, '^tedacct_[0-9a-f]{24}$')
   or not regexp_matches(beneficiary_account_token, '^tedacct_[0-9a-f]{24}$')
   or not regexp_matches(payer_tax_id_masked, '^(\*{7}|\*{10})[0-9]{4}$')
   or not regexp_matches(beneficiary_tax_id_masked, '^(\*{7}|\*{10})[0-9]{4}$')
   or (movement_kind = 'RETURN' and (original_transfer_id = '' or return_reason_code = ''))
   or (movement_kind = 'TRANSFER' and (original_transfer_id <> '' or return_reason_code <> ''))
