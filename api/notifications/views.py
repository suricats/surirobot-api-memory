import datetime as dt

from memory.models import Info, User, Encoding, SensorData, Log
from memory.serializers import InfoSerializer, UserSerializer, EncodingSerializer, SensorDataSerializer, LogSerializer
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from datetime import datetime
import pytz
from django.http import JsonResponse

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
        # Memorized information
        latest_temperature = float(latest_temp_obj.data)
        latest_humidity = float(latest_humidity_obj.data)
        date = latest_temp_obj.created
        # Dates
        actual_date = datetime.now(tz=pytz.UTC)
        today = datetime(actual_date.year, actual_date.month, actual_date.day, tzinfo=pytz.UTC)
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
        return JsonResponse(notifications, safe=False)

    def expiration(self, request):
        return Response('WIP')
