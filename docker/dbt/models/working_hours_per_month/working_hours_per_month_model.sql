{{ config(schema='public') }}

with working_hours_per_month as (
    select
    first_name
    ,last_name
    ,date_part('month', date) as "month"
    ,date_part('year', date) as "year"
    ,sum(h) as worked_hours
    from {{source('metabase', 'master_db')}} as a
        left join {{source('metabase', 'timelogs')}} as b on a."user_ID"  = b."user"
    group by
    first_name
    ,last_name
    ,date_part('month', date)
    ,date_part('year', date)
)

select * from working_hours_per_month
