FROM python:3.9-buster

COPY ./timelogs /timelogs/
COPY ./main.py .
COPY ./setup.py .
COPY ./requirements.txt .

RUN pip install -r requirements.txt
RUN pip install -e .

#CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]
