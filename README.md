# timelogs

**Timelogs** is a combination of a technical kit with Nginx, FastApi, dbt and Postgres database.  
The application tracks messages on Slack with crontab script, transform and validate data and saves timelog information to a database.  
The application automatically recognizes the information stored in the Slack message based on **NLP** (Natural Language Processing).
Moreover, application recognize `add me` message from the user and add the user to database.  
**Timelogs** works also as REST API independently and provides creating and removing the user/timelogs with GUI interface.

**Metabase** was used to performs a daily sampling of each field’s values and caches the distinct values in order to make checkbox and select filters work in dashboards and SQL/native questions.
Metabase maintains its own information about the various tables and fields in each database to aid in querying. By default, Metabase performs this lightweight sync hourly to look for changes to the database.

**FastApi** is a modern web framework tool for building APIs with Python 3.6+ based on standard Python type hints.
 Fastapi is one of the fastest Python frameworks available thanks to Starlette and Pydantic.

**PostgreSQL** provides SSL encryption native support on traffic data, between Client and Databases. You can use a robust access-control system, in tables, objects, columns and at row-level too.

**Nginx** is a web server – working as a reverse proxy server can act as a traffic management, sitting in front of your backend servers and distributing client requests across a group of servers in a manner that maximizes speed and capacity utilization.
This makes that Nginx is a load balancer  with extremely low response times even under high loading.

**dbt** - gives the documentation lives with your DBT project and it is automatically generated.   
dbt allows you to test your data (schema tests, referential integrity tests, custom tests) and ensures data quality.


## Nginx Unit configuration

The default Nginx Unit configuration file can be found at fastapi/config.json instead of nginx.conf file used in nginx. It's set to run the site for local development at http://localhost:8000.

## Postgres configuration


## Slack Channel Authorization

To get access to Slack messages put your SLACK_TOKEN into token.json file in base directory.
The file should be a dictionary: `{"SLACK_TOKEN": 'token secret'}`

## Running docker container

To run docker container build the container image from base folder with command:   
`docker build -t python/python:3.9-buster . -f docker/Dockerfile`  
`docker build -t nginx/unit:1.22.0-python3.9 . -f docker/fastapi/Dockerfile`  
and than run container with docker-compose file from docker folder with command:  
`docker-compose up -d `

## pgAdmin

To see changes in database use server `http://localhost:5050`. To log in to pgAdmin server use your email and password authentication defined in docker-compose. In pgAdmin you can also run SQL codex.

## Metabase

To see your access to metabase use server `http://localhost:3000`.
