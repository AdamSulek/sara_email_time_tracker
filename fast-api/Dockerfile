FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7


COPY ./fast-api /fast-api/
COPY ./main.py  /fast-api/
COPY ./timelogs /fast-api/timelogs/
WORKDIR /fast-api

RUN pip install -r requirements.txt
RUN pip install Jinja2
RUN pip install python-multipart

RUN apt-get update && \
    apt-get install -y vim

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]
