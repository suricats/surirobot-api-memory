import logging
import os
import redis
from celery import shared_task

from notifications.views import notifications_process

logger = logging.getLogger('REALTIME')
r = redis.StrictRedis(host=os.environ.get('REDIS_URL', 'localhost'), port=os.environ.get('REDIS_PORT', 6379))

@shared_task(name="notifications.client")
def client():
    notifications = notifications_process()
    r.publish(os.environ.get('REDIS_CLIENT_NOTIFICATIONS_CHANNEL', '1'), notifications)
    logger.info('Notifications sended to client')


