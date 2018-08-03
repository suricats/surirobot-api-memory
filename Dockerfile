FROM python:3.6

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
RUN cp -R /usr/local/lib/python3.6/site-packages/rest_framework_swagger/static /static/
RUN cp -R /usr/local/lib/python3.6/site-packages/rest_framework/static /static/

COPY . /app
WORKDIR /app

EXPOSE 8000/tcp
ENTRYPOINT ["gunicorn",  "-w",  "4", "-b",  "0.0.0.0:8000", "--chdir", "api", "api.wsgi"]
