FROM python:3.9-buster

COPY ./timelogs .
COPY ./docker /docker/
COPY ./task_flow.py .
#COPY ./setup.py /timelogs/
#COPY ./main.py .

#WORKDIR /timelogs

RUN pip install -e .
# cron job
RUN apt-get update && \
    apt-get install -y cron vim
COPY docker/crontab.txt .
RUN crontab crontab.txt

CMD ["cron", "-f"]

COPY ./requirements.txt .
#COPY ./requirements.txt /timelogs/

RUN pip install -r requirements.txt
RUN pip install python-multipart

RUN python -m nltk.downloader punkt
RUN python -m spacy download en_core_web_sm
