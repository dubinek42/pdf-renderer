FROM python:3.10.2-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "gunicorn", "-c", "gunicorn_config.py", "src.api.main:application"]
EXPOSE 8080