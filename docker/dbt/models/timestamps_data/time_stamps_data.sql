{{ config(schema='public') }}

with timestamps as (
    select * from {{source('metabase', 'timestamps')}}
)

select * from timestamps
