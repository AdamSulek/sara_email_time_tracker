{{ config(schema='public') }}

with working_hours_per_month as (
    select
    name
    ,date_part('month', date) as "month"
    ,sum(h) as worked_hours
    from {{source('metabase', 'master_db')}} as a
        left join {{source('metabase', 'timelogs')}} as b on a."user_ID"  = b."user"
    group by
    name
    ,date_part('month', date)
)

select * from working_hours_per_month
