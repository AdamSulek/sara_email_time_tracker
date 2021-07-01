FROM python:3.9-buster

COPY ./timelogs /timelogs/
COPY ./task_flow.py .


# cron job
RUN apt-get update && \
    apt-get install -y cron vim
COPY docker/crontab.txt .
RUN crontab crontab.txt
CMD ["cron", "-f"]

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt
RUN python -m nltk.downloader punkt
RUN python -m spacy download en_core_web_sm
