import os
from datetime import timedelta

from dotenv import load_dotenv, find_dotenv

# Load .env
load_dotenv(find_dotenv())
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

app = Celery('api')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.autodiscover_tasks(['api.celery.notifications.slack', 'api.celery.notifications.client'])
app.conf.beat_schedule = {
    'slack-notifications-every-20-seconds': {
        'task': 'notifications.slack',
        'schedule': 20
    },
    'client-notifications-every-30-minutes': {
        'task': 'notifications.client',
        'schedule': timedelta(minutes=30)
    },
}
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))