import os
import threading
import requests
import pytz
import json
from datetime import datetime, timedelta

import timezonefinder as timezonefinder
from dateutil import tz

from memory.models import SensorData

SLACK_NOTIFICATIONS_TIME = 10
slack_url = os.environ.get('SLACK_URL')
headers = {'Content-Type': 'application/json'}
last_opening_notification = datetime.now().replace(day=datetime.now().day-1)
last_closing_notification = datetime.now().replace(day=datetime.now().day-1)

def slack_notifications(stop_event):
    global last_opening_notification
    global last_closing_notification
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

    print('SLACK NOTIFICATIONS STARTED')
    # Rules
    # Case n°1 : opening between 6h and 10h and not closed on the first 5min
    openings_morning = SensorData.objects.filter(type=mc).filter(data='0').filter(
        created__range=(today.replace(hour=6), today.replace(hour=11)))
    if openings_morning and actual_date.day > last_opening_notification.day:
        delay = timedelta(minutes=5)
        last_opening = openings_morning[len(openings_morning)-1]
        recent_closings = SensorData.objects.filter(type=mc).filter(data='1').filter(
            created__range=(last_opening.created, last_opening.created + delay))

        if not recent_closings and last_opening.created + delay <= actual_date:
            last_opening_notification = actual_date
            data = json.dumps({"text": "Beaubourg est ouvert !"})
            requests.post(url=slack_url, data=data, headers=headers)

    # Case n°2 : closing between 18h and 2h and no opening in the 15min
    closings_evening = SensorData.objects.filter(type=mc).filter(data='1').filter(
        created__range=(today.replace(hour=18), today.replace(day=today.day + 1, hour=2)))
    if closings_evening and actual_date.day > last_closing_notification.day:
        last_closing = closings_evening[len(openings_morning)-1]
        recent_openings = SensorData.objects.filter(type=mc).filter(data='0').filter(
            created__range=(last_closing.created, last_closing.created + timedelta(minutes=15)))

        if not recent_openings:
            last_closing_notification = actual_date
            data = json.dumps({"text": "Bonne nuit les suricats"})
            requests.post(url=slack_url, data=data, headers=headers)
    if not stop_event.is_set():
        threading.Timer(SLACK_NOTIFICATIONS_TIME, slack_notifications, [stop_event]).start()



