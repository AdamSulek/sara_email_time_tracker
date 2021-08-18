FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY . .
COPY ./main.py  .
#COPY requirements.txt .
#WORKDIR /fastapi

RUN pip install -r requirements.txt
RUN pip install Jinja2
RUN pip install python-multipart


CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
