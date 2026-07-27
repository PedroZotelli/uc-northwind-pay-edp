{{ config(tags=['type_02']) }}

-- Privacy: documents must be tokenized and masked, never clear.

select *
from {{ ref('bronze_instant_payment_event') }}
where not regexp_matches(payer_document_token, '^doc_[0-9a-f]{24}$')
   or not regexp_matches(payee_document_token, '^doc_[0-9a-f]{24}$')
   or not regexp_matches(payer_document_masked, '^\*{7,10}[0-9]{4}$')
   or not regexp_matches(payee_document_masked, '^\*{7,10}[0-9]{4}$')
   or regexp_matches(description, '[0-9]{11,19}')
