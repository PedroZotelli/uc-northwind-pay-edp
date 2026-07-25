{% macro conserves_totals(bronze_relation, silver_relation, amount_columns) %}

{#
    Conservation, defined once and applied by every type.

    Silver conforms; it must not change a row count or a monetary total. Each
    named column is summed on both sides and compared with IS DISTINCT FROM, so
    a batch that exists on only one side fails rather than comparing NULL.

    Every column in `amount_columns` must carry the same name in Bronze and
    Silver, which is the case for all five types by construction: Silver
    re-selects Bronze money columns without renaming them.
#}

{%- set aggregates -%}
count(*) as row_count
{%- for column in amount_columns -%}
, sum({{ column }}) as sum_{{ column }}
{%- endfor -%}
{%- endset -%}

with bronze as (
    select batch_id, {{ aggregates }}
    from {{ bronze_relation }}
    group by batch_id
),

silver as (
    select batch_id, {{ aggregates }}
    from {{ silver_relation }}
    group by batch_id
)

select coalesce(bronze.batch_id, silver.batch_id) as batch_id
from bronze
full outer join silver on silver.batch_id = bronze.batch_id
where bronze.row_count is distinct from silver.row_count
{%- for column in amount_columns %}
   or bronze.sum_{{ column }} is distinct from silver.sum_{{ column }}
{%- endfor %}

{% endmacro %}
