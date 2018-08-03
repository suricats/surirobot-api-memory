import datetime as dt
import time

import timezonefinder as timezonefinder
from dateutil import tz

from memory.models import Info, User, Encoding, SensorData, Log
from memory.serializers import InfoSerializer, UserSerializer, EncodingSerializer, SensorDataSerializer, LogSerializer
from .models import Notification
from .helpers import get_crypto, get_news, get_weather
from .serializers import NotificationSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from datetime import datetime
import pytz
from django.http import JsonResponse
import requests

class NotificationViewSet(viewsets.ModelViewSet):
    """
    API for notifications
    get_notifications:
        Get the notifications

    expiration:
        Expire a notification

    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_notifications(self, request):
        # Rules engine
        notifications = []
        latest_temp_obj = SensorData.objects.filter(type="temperature").latest('created')
        latest_humidity_obj = SensorData.objects.filter(type="humidity").latest('created')

        # Localisation (faked for the moment)
        latitude = 48.8589506
        longitude = 2.276848
        # Timezone
        tf = timezonefinder.TimezoneFinder()
        current_tz = tz.gettz(tf.timezone_at(lng=longitude, lat=latitude))
        # Dates
        actual_date = datetime.now(tz=current_tz)
        today = datetime(actual_date.year, actual_date.month, actual_date.day, tzinfo=current_tz)
        tomorrow = datetime(year=actual_date.year, month=actual_date.month, day=actual_date.day+1, hour=actual_date.hour, tzinfo=current_tz)
        # Memorized information
        latest_temperature = float(latest_temp_obj.data)
        latest_humidity = float(latest_humidity_obj.data)
        date = latest_temp_obj.created
        weather_info_tomorrow = get_weather(latitude=latitude, longitude=longitude, time=tomorrow.timestamp(), language='fr')

        # Rule n°1 : temperature is recent and greater than 25°C
        if date > today and latest_temperature >= 25:
            notifications.append({'type': 'message', 'target': 'all', 'data': 'La temperature est de {}°C. Pensez à bien vous hydrater !'.format(latest_temperature)})
        # Rule n° 2 : temperature is recent and lower than 20°C
        if date > today and latest_temperature <= 20:
            notifications.append({'type': 'message', 'target': 'all',
                                  'data': 'La temperature est de {}°C. Pensez à bien vous couvrir et de boir un café bien chaud !'.format(
                                      latest_temperature)})
        # Rule n° 3 : humidity is recent and greater than 80%
        if date > today and latest_humidity >= 80:
            notifications.append({'type': 'message', 'target': 'all', 'data': "L'humidité est de {}%. N'hésitez pas à vous dégourdir les jambes !".format(latest_humidity)})
        # Rule n° 4 : humidity is recent and lower than 20%
        if date > today and latest_humidity <= 20:
            notifications.append({'type': 'message', 'target': 'all',
                                  'data': "L'humidité est de {}%. Hydratez vous bien la peau et aérez la pièce.".format(
                                      latest_humidity)})
        # Rule n° 5 : Tomorrow is raining
        if weather_info_tomorrow:
            if weather_info_tomorrow['daily']['precipProbability'] >=  0.45 and weather_info_tomorrow['daily'].get('precipType') == 'rain' and weather_info_tomorrow['daily'].get('precipIntensityMax') > 0.5:
                precip_max_time = datetime.fromtimestamp(weather_info_tomorrow['daily']['precipIntensityMaxTime'], tz=current_tz)
                notifications.append({'type': 'message', 'target': 'all',
                                      'data': "Attention ! Demain il risque de pleuvoir aux alentours de {:02d}h{:02d} ! N'oubliez pas votre parapluie.".format(precip_max_time.hour, precip_max_time.minute)})

        # Rule n° 6 : Tomorrow is full moon
        if weather_info_tomorrow:
            if 0.45 <= weather_info_tomorrow['daily'].get('moonPhase') <= 0.55:
                notifications.append({'type': 'message', 'target': 'all',
                                      'data': "Demain c'est la pleine lune. N'oubliez pas votre appareil photo ;)"})

        return JsonResponse(notifications, safe=False)

    def expiration(self, request):
        return Response('WIP')
