{{ config(schema='public') }}

with timelog as (
    select * from {{source('metabase', 'timelogs')}}
)

select * from timelog
