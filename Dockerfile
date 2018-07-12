FROM python:3.6

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 8000/tcp
ENTRYPOINT ["gunicorn",  "-w",  "4", "-b",  "0.0.0.0:8000", "--chdir", "api", "api.wsgi"]


