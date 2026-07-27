{{ config(tags=['type_03']) }}

-- Privacy and arithmetic: every restricted field is tokenized or masked, and
-- the per-settlement net still equals face minus discount plus fee.

select *
from {{ ref('silver_payment_slip_settlement') }}
where not regexp_matches(payment_reference_token, '^payref_[0-9a-f]{24}$')
   or not regexp_matches(beneficiary_token, '^party_[0-9a-f]{24}$')
   or not regexp_matches(bank_account_token, '^acct_[0-9a-f]{24}$')
   or not regexp_matches(beneficiary_tax_id_masked, '^(\*{7}|\*{10})[0-9]{4}$')
   or net_amount_brl <> recomputed_net_amount_brl
   or net_amount_brl < 0.00
