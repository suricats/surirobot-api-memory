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
logger = logging.getLogger('REALTIME')
slack_url = os.environ.get('SLACK_URL')
headers = {'Content-Type': 'application/json'}


@shared_task(name="notifications.slack")
def slack():
    logger.info('Slack notifications processing..')
    # Get notifications date
    try:
        last_opening_notification = Info.objects.filter(type='opening-notification-slack').latest(
            'created').created
    except Info.DoesNotExist:
        last_opening_notification = datetime.now() - timedelta(days=1)
    except:
        traceback.print_exc()
    try:
        last_closing_notification = Info.objects.filter(type='closing-notification-slack').latest(
            'created').created
    except Info.DoesNotExist:
        last_closing_notification = datetime.now() - timedelta(days=1)
    try:
        # Dates
        actual_date = datetime.now(tz=TZ_DEFAULT)
        today = datetime(actual_date.year, actual_date.month, actual_date.day, tzinfo=TZ_DEFAULT)

        # Rules
        # Case n°1 : opening between range and not closed on the first 5min
        openings_morning = SensorData.objects.filter(type=mc).filter(data='0').filter(
            created__range=(today.replace(hour=OPENING_RANGE[0]), today.replace(hour=OPENING_RANGE[1])))
        # Case : Opening happened in range, no notification was send today, actual time is still in approximate range
        limit_opening_notification = last_opening_notification.replace(hour=0, minute=0, second=0) + timedelta(days=1)
        limit_opening_approximate_range = today.replace(hour=OPENING_RANGE[1])+OPENING_DELAY + timedelta(minutes=5)
        if int(os.environ.get('LOG', '0')):
            logger.info('Actual date : {} '.format(actual_date))
            logger.info('Opening :')
            logger.info('Opening happened in range : {}'.format(bool(OPENING_RANGE)))
            logger.info('No notification was sent today : {}'.format(bool(actual_date > limit_opening_notification)))
            logger.info('Last notification date : {}'.format(last_opening_notification))
            logger.info('Actual time is still in approximate range : {}'.format(bool(actual_date <= limit_opening_approximate_range)))
        if openings_morning and actual_date > limit_opening_notification and actual_date <= limit_opening_approximate_range:

            last_opening = openings_morning[len(openings_morning)-1]
            recent_closings = SensorData.objects.filter(type=mc).filter(data='1').filter(
                created__range=(last_opening.created, last_opening.created + OPENING_DELAY))
            if int(os.environ.get('LOG', '0')):
                logger.info('No closings : {}'.format(bool(not recent_closings)))
                logger.info('In short delay : {}'.format(bool(actual_date >= last_opening.created + OPENING_DELAY )))
                logger.info('Date observed : {}'.format(last_opening.created))
            # Case : No closings during a short delay
            if not recent_closings and actual_date >= last_opening.created + OPENING_DELAY:
                serializer = InfoSerializer(data={'type': 'opening-notification-slack'})
                if serializer.is_valid():
                    serializer.save()
                    logger.info('Slack opening notifications sended.')
                    data = json.dumps({"text": "Beaubourg est ouvert ! :door:"})
                    requests.post(url=slack_url, data=data, headers=headers)
                else:
                    logger.error('Slack opening notifications serializer')

        # Case n°2 : closing between 18h and 2h and no opening in the 15min but opening in the day
        closings_evening = SensorData.objects.filter(type=mc).filter(data='1').filter(
            created__range=(today.replace(hour=CLOSING_RANGE[0]), today.replace(hour=CLOSING_RANGE[0]) + timedelta(hours=abs(CLOSING_RANGE[1] - CLOSING_RANGE[0]))))
        # Case : Closing happened in range, no notification was send today, actual time is still in approximate range , opening notification sent today
        limit_closing_notification = last_closing_notification.replace(hour=0, minute=0, second=0) + timedelta(days=1)
        limit_closing_approximate_range = today.replace(hour=CLOSING_RANGE[0])+CLOSING_DELAY + timedelta(hours=abs(CLOSING_RANGE[1] - CLOSING_RANGE[0]))
        if int(os.environ.get('LOG', '0')):
            logger.info('Closing :')
            logger.info('Closing happened in range : {}'.format(bool(closings_evening)))
            logger.info('Opening notification was sent today : {}'.format(bool(actual_date.day == last_opening_notification.day)))
            logger.info('No notification was sent today : {}'.format(bool(actual_date > limit_closing_notification)))
            logger.info('Last notification date : {}'.format(last_closing_notification))
            logger.info('Actual time is still in approximate range : {}'.format(bool(actual_date <= limit_closing_approximate_range)))

        if closings_evening and actual_date > limit_closing_notification and actual_date.day == last_opening_notification.day and actual_date <= limit_closing_approximate_range:
            last_closing = closings_evening[len(closings_evening)-1]
            recent_openings = SensorData.objects.filter(type=mc).filter(data='0').filter(
                created__range=(last_closing.created, last_closing.created + CLOSING_DELAY))
            # Case : No recent openings but daily opening
            if not recent_openings:
                serializer = InfoSerializer(data={'type': 'closing-notification-slack'})
                if serializer.is_valid():
                    serializer.save()
                    logger.info('Slack closing notifications sended.')
                    data = json.dumps({"text": "Bonne nuit les suricats :night_with_stars:"})
                    requests.post(url=slack_url, data=data, headers=headers)
                else:
                    logger.error('Slack closing notifications serializer')

    except Exception as e:
        logger.error('{}: {}'.format(type(e).__name__, e))
        traceback.print_exc()
    connection.close()

