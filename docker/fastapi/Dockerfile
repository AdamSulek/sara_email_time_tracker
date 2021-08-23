FROM nginx/unit:1.22.0-python3.9

COPY ./timelogs/source.py /app/timelogs/source.py
COPY ./timelogs/fastapi.py /app/timelogs/fastapi.py
COPY ./timelogs/slack.py /app/timelogs/slack.py

COPY ./docker/fastapi/requirements.txt /app/requirements.txt
COPY ./docker/fastapi/main.py /app/
COPY ./docker/fastapi/html /app/html/
COPY ./docker/fastapi/config.json /docker-entrypoint.d/config.json

WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install Jinja2
RUN pip install python-multipart

RUN apt-get update && \
    apt-get install -y vim
