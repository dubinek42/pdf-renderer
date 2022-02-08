FROM python:3.10.2-slim

WORKDIR /app

RUN apt-get update
RUN apt-get install poppler-utils -y

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

CMD [ "gunicorn", "-c", "gunicorn_config.py", "src.api.main:application"]
EXPOSE 8080
