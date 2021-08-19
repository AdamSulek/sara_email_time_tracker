# Overview

dbt does the T in ELT processes – it doesn’t extract or load data, but it’s extremely good at transforming data that’s already loaded into your warehouse. dbt’s only function is to take code, compile it to SQL, and then run against your database. In datahouse are stored files (for example .csv) and this file are transformed by dbt.

dbt allows users to create dev and prod environments and easily transition between the two.

dbt provides additional functions and using variables in sql query that allow users to express data transformation logic, for example:

{% if incremental and target.schema == 'prod' %}         
    where timestamp >= (select max(timestamp) from {{this}})     
{% else %}         
    where timestamp >= dateadd(day, -3, current_date)     
{% endif %}

# Running dbt with docker compose as a service

To best of my knowledge there is no image of dbt.  
To build an image use Dockerfile (context should contain the path to Dockerfile).  
This file install dbt via pip
set environment variables, working dir and cmd["/bin/bash"]

Create volumes for data:  
```
volumes:
  - ./data:/data
  - ./dbt:/dbt_init
```
Port mapping: choose port on local machine for example 5123
dbt is running on port 8080, so mapping looks like:

```
port:
 - 5123:8080
```

dbt depends on database so link it with database service:

```
links:
  - database(service name)
depends_on:
  - database
```

 create bash script(dbt_entrypoint.sh) with dbt -debug, -test, -run, -docs which will test and run dbt
 give permission and run this file with:
```
 command: /bin/bash -c "chmod +x /dbt_init/dbt_entrypoint.sh && /dbt_init/dbt_entrypoint.sh"
```


# Connection with postgres database
In the dbt folder create profile.yml file with all of the required credentials to connect with database  
first row have to be the same with profile in dbt_project.yml

threads limit define on how many models dbt will working on.
sensitive data has to be the same as database credentials

```
timelogs:
  outputs:
    dev:
      type: postgres
      threads: 4
      host:
      port: 5432
      user:
      pass:
      dbname: metabase
      schema: public
  target: dev
```

# dbt Models

model is a data transformation expressed in a single SELECT statement

materialization is strategy by which a data model is built in the warehouse (generally into views and tables).

## How--tos

1. each model is created in another folder in models directory, so to create new model create new folder
2. to build a model minimum requirements is one sql file, name have to be unique so you can use foldername_model.sql
* tell dbt which schema will be used
`{{ config(schema='public') }}`
* create select statement with a source
`select * from {{source('database', 'table')}}`
3. optionally, but highly recommended is that this folder contain schema.yml file with:
* name of the source (whatever you want),
* database: correspond to database
* schema: correspond to schema
Moreover, you can add description on the database or table level. If you specify columns you can add tests like -unique or -not-null.

The auto-generated documentation running on localhost:8080 (depends on previously defined port) is included all of this information which help the users.
