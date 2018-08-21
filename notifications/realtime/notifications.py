import os
from threading import Thread, Timer, Event
import requests
import logging
import json
import time
from datetime import datetime, timedelta
import traceback
import redis
import timezonefinder as timezonefinder
from dateutil import tz
from django.db import connection
from memory.models import SensorData, Info
from memory.serializers import InfoSerializer
logger = logging.getLogger('REALTIME_NOTIFICATIONS')

class NotificationsThread(Thread):
    def __init__(self, interval=1):
        Thread.__init__(self)
        self.setDaemon(True)
        self._stop_event = Event()
        self.interval = interval

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        while not self.stopped():
            logger.info('Notifications processing..')
            try:
                pass
            except Exception as e:
                logger.error('{}: {}'.format(type(e).__name__, e))
                traceback.print_exc()
            connection.close()
            time.sleep(self.interval)

