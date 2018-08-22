FROM python:3.6

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY . /app
WORKDIR /app

ENTRYPOINT celery -A api worker -B --concurrency=20 --loglevel=info
