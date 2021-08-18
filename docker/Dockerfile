FROM python:3.9-buster

COPY ./timelogs /timelogs/
COPY ./docker /docker/
COPY ./task_flow.py .
COPY ./setup.py .
COPY ./main.py .

RUN pip install -e .
# cron job
RUN apt-get update && \
    apt-get install -y cron vim
COPY docker/crontab.txt .
RUN crontab crontab.txt

#CMD [ "uvicorn", "../main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["cron", "-f"]

COPY ./requirements.txt .

RUN pip install -r requirements.txt
RUN pip install python-multipart

RUN python -m nltk.downloader punkt
