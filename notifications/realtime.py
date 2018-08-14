import os
import threading
import requests
import logging
import json
from datetime import datetime, timedelta

import timezonefinder as timezonefinder
from dateutil import tz
from django.db import connection
from memory.models import SensorData
logger = logging.getLogger('REALTIME')
SLACK_NOTIFICATIONS_TIME = 10
slack_url = os.environ.get('SLACK_URL')
headers = {'Content-Type': 'application/json'}

last_opening_notification = datetime.now().replace(day=datetime.now().day-1)
last_closing_notification = datetime.now().replace(day=datetime.now().day-1)
opening_range = [6, 11]
opening_delay = timedelta(minutes=5)
closing_range = [18, 2]
closing_delay = timedelta(minutes=15)

def slack_notifications(stop_event):
    global last_opening_notification
    global last_closing_notification
    logger.info('Slack notifications processing..')
    try:
        mc = 'magnetic-contact'
        # Localisation of Paris for timezone
        latitude = 48.8589506
        longitude = 2.276848
        # Timezone
        tf = timezonefinder.TimezoneFinder()
        current_tz = tz.gettz(tf.timezone_at(lng=longitude, lat=latitude))
        # Dates
        actual_date = datetime.now(tz=current_tz)
        today = datetime(actual_date.year, actual_date.month, actual_date.day, tzinfo=current_tz)


        # Rules
        # Case n°1 : opening between range and not closed on the first 5min
        openings_morning = SensorData.objects.filter(type=mc).filter(data='0').filter(
            created__range=(today.replace(hour=opening_range[0]), today.replace(hour=opening_range[1])))
        # Case : Opening happened in range, no notification was send today, actual time is still in approximate range
        logger.info('Opening happened in range : {}'.format(bool(opening_range)))
        logger.info('No notification was sent today : {}'.format(bool(actual_date.day > last_opening_notification.day)))
        logger.info('Actual time is still in approximate range : {}'.format(bool(actual_date <= today.replace(hour=opening_range[1]) + opening_delay)))
        if openings_morning and actual_date.day > last_opening_notification.day and actual_date <= today.replace(hour=opening_range[1])+opening_delay:

            last_opening = openings_morning[len(openings_morning)-1]
            recent_closings = SensorData.objects.filter(type=mc).filter(data='1').filter(
                created__range=(last_opening.created, last_opening.created + opening_delay))
            logger.info('No closings : {}'.format(bool(not recent_closings)))
            logger.info('In short delay : {}'.format(bool(actual_date >= last_opening.created + opening_delay )))
            logger.info('Date observed : {}'.format(last_opening.created))
            # Case : No closings during a short delay
            if not recent_closings and actual_date >= last_opening.created + opening_delay:
                last_opening_notification = actual_date
                logger.info('Slack notifications sended.')
                data = json.dumps({"text": "Beaubourg est ouvert ! :door:"})
                requests.post(url=slack_url, data=data, headers=headers)

        # Case n°2 : closing between 18h and 2h and no opening in the 15min
        closings_evening = SensorData.objects.filter(type=mc).filter(data='1').filter(
            created__range=(today.replace(hour=closing_range[0]), today.replace(day=today.day + 1, hour=closing_range[1])))
        # Case : Closing happened in range, no notification was send today, actual time is still in approximate range
        if closings_evening and actual_date.day > last_closing_notification.day and actual_date <= today.replace(day=today.day + 1, hour=closing_range[1])+closing_delay:
            last_closing = closings_evening[len(openings_morning)-1]
            recent_openings = SensorData.objects.filter(type=mc).filter(data='0').filter(
                created__range=(last_closing.created, last_closing.created + closing_delay))
            # Case : No openings
            if not recent_openings:
                last_closing_notification = actual_date
                logger.info('Slack notifications sended.')
                data = json.dumps({"text": "Bonne nuit les suricats :night_with_stars:"})
                requests.post(url=slack_url, data=data, headers=headers)
    except Exception as e:
        logger.error('{}: {}'.format(type(e).__name__, e))
    if not stop_event.is_set():
        threading.Timer(SLACK_NOTIFICATIONS_TIME, slack_notifications, [stop_event]).start()
    connection.close()

