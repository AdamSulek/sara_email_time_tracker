#!/bin/bash
dbt init timelogs &&
cp -r /dbt_init/. /dbt/timelogs &&
cp -r /data/. /dbt/timelogs/data &&
rm -rf /dbt/timelogs/models/timelogs &&
#cp -r /dbt/models/example/. /dbt/spotify_analytics/models/example &&
mv /dbt/timelogs/profiles.yml /root/.dbt/profiles.yml
cd /dbt/timelogs &&
dbt debug &&
dbt deps &&
dbt seed &&
dbt run &&
dbt test &&
dbt docs generate &&
dbt docs serve
