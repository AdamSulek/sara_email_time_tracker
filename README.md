## timelogs_tracker

This application tracks messages on Slack and parse important information and saves it to a database.  
The application automatically recognizes the information stored in the Slack message based on natural language processing.
Moreover, application recognize #add me message from the user and add the user to master db


## Authorization

To get access to Slack messages put your SLACK_TOKEN into token.json file in base directory.
The file should be a dictionary: `{"SLACK_TOKEN": 'token secret'}`

## Running docker container

To run docker container build the container image from base folder with command:   
`docker build -t container_name . -f docker/Dockerfile`  
and than run container with docker-compose file from docker container with command:  
`docker-compose up -d `

## Database

To see changes in database use server `0.0.0.0:5050`. To log in to pgAdmin server use your email and password authentication from docker-compose.

## Metabase

To see your access to metabase use server `0.0.0.0:3000`. 
