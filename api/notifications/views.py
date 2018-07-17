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
        sensor = SensorData.objects.filter(type="temperature").latest('created')
        # Memorized information
        latest_temperature = float(sensor.data)
        date = sensor.created
        # Dates
        actual_date = datetime.now(tz=pytz.UTC)
        today = datetime(actual_date.year, actual_date.month, actual_date.day, tzinfo=pytz.UTC)
        # Rule n°1 : temperature is recent and greater than 25°C
        if date > today and latest_temperature > 25:
            notifications.append({'type': 'message', 'target': 'all', 'data': 'La temperature est de {}°C. Pensez à bien vous hydrater !'.format(latest_temperature)})

        return JsonResponse(notifications, safe=False)

    def expiration(self, request):
        return Response('WIP')
