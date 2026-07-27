{% macro release_gate(relation, delta_columns) %}

{#
    The release gate, defined once and applied by every type.

    Gold may not publish an unexplained financial difference. A batch whose
    declaration disagrees with its computed total never reaches Gold at all,
    so any surviving non-zero delta is a modern defect.

    `delta_columns` must name only the delta columns that are genuinely
    computed for this type. Several Gold columns are constants shaped to match
    the legacy reporting grain — see `modern/README.md`, "Constant columns in
    Gold". Passing one of those here would produce a test that cannot fail.
#}

select *
from {{ relation }}
where status <> 'MATCHED'
{%- for column in delta_columns %}
   or {{ column }} <> 0
{%- endfor %}

{% endmacro %}
