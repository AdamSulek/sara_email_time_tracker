{{ config(schema='public') }}

with master_db as (
    select * from {{source('metabase', 'master_db')}}
)

select * from master_db
