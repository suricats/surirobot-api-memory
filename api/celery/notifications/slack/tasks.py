import json
import logging
import os
import traceback
from datetime import datetime, timedelta
import requests
from celery import shared_task
from django.db import connection

from memory.models import SensorData, Info
from memory.serializers import InfoSerializer
from api.celery.notifications.constants import OPENING_RANGE, OPENING_DELAY, CLOSING_RANGE, CLOSING_DELAY, mc
from notifications.constants import TZ_DEFAULT
from .random_message import get_random_message

logger = logging.getLogger('REALTIME')
slack_url = os.environ.get('SLACK_URL')
headers = {'Content-Type': 'application/json'}


@shared_task(name="notifications.slack")
def slack():
    logger.info('Slack notifications processing..')
    # Get notifications date
    try:
        last_o_notif = Info.objects.filter(type='opening-notification-slack').latest(
            'created').created
    except Info.DoesNotExist:
        last_o_notif = datetime.now() - timedelta(days=1)
    except:
        traceback.print_exc()
    try:
        last_c_notif = Info.objects.filter(type='closing-notification-slack').latest(
            'created').created
    except Info.DoesNotExist:
        last_c_notif = datetime.now() - timedelta(days=1)
    try:
        # Dates
        curr_date = datetime.now(tz=TZ_DEFAULT)
        today = datetime(curr_date.year, curr_date.month, curr_date.day, tzinfo=TZ_DEFAULT)

        # Rules

        # Case n°1 : opening between range and not closed on the first 5min
        o_in_o_range = SensorData.objects.filter(type=mc).filter(data='0').filter(
            created__range=(today.replace(hour=OPENING_RANGE[0]), today.replace(hour=OPENING_RANGE[1])))

        # Case : Opening happened in range, no notification was send today, actual time is still in approximate range
        lim_o_notif = last_o_notif.replace(hour=0, minute=0, second=0) + timedelta(days=1)
        lim_o_app_range = today.replace(hour=OPENING_RANGE[1]) + OPENING_DELAY + timedelta(minutes=5)

        if o_in_o_range and lim_o_notif < curr_date <= lim_o_app_range:

            last_op = o_in_o_range[len(o_in_o_range) - 1]
            recent_c = SensorData.objects.filter(type=mc).filter(data='1').filter(
                created__range=(last_op.created, last_op.created + OPENING_DELAY))

            # Case : No closings during a short delay
            if not recent_c and curr_date >= last_op.created + OPENING_DELAY:
                serializer = InfoSerializer(data={'type': 'opening-notification-slack'})
                if serializer.is_valid():
                    serializer.save()
                    logger.info('Slack opening notifications sended.')
                    text, _ = get_random_message()
                    data = json.dumps({"text": text})
                    requests.post(url=slack_url, data=data, headers=headers)
                else:
                    logger.error('Slack opening notifications serializer')

        # Case n°2 : closing between 18h and 2h and no opening in the 15min but opening in the day
        c_in_c_range = SensorData.objects.filter(type=mc).filter(data='1').filter(
            created__range=(today.replace(hour=CLOSING_RANGE[0]), today.replace(hour=CLOSING_RANGE[0]) + timedelta(
                hours=abs(CLOSING_RANGE[1] - CLOSING_RANGE[0]))))

        # Case : Closing happened in range, no notification was send today, actual time is still in approximate range , opening notification sent today
        lim_cl_notif = last_c_notif.replace(hour=0, minute=0, second=0) + timedelta(days=1)
        lim_c_app_range = today.replace(hour=CLOSING_RANGE[0]) + CLOSING_DELAY + timedelta(
            hours=abs(CLOSING_RANGE[1] - CLOSING_RANGE[0]))

        if c_in_c_range and curr_date.day == last_o_notif.day and lim_cl_notif < curr_date <= lim_c_app_range:

            last_c = c_in_c_range[len(c_in_c_range) - 1]
            recent_o = SensorData.objects.filter(type=mc).filter(data='0').filter(
                created__range=(last_c.created, last_c.created + CLOSING_DELAY))

            # Case : No recent openings but daily opening
            if not recent_o:
                serializer = InfoSerializer(data={'type': 'closing-notification-slack'})
                if serializer.is_valid():
                    serializer.save()
                    logger.info('Slack closing notifications sended.')
                    _, text = get_random_message()
                    data = json.dumps({"text": text})
                    requests.post(url=slack_url, data=data, headers=headers)
                else:
                    logger.error('Slack closing notifications serializer')

    except Exception as e:
        logger.error('{}: {}'.format(type(e).__name__, e))
        traceback.print_exc()
    connection.close()
