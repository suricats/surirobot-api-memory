from memorization.models import Info, User, Picture, SensorData, Log
import datetime as dt

from memorization.models import Info, User, Picture, SensorData, Log
from memorization.serializers import InfoSerializer, UserSerializer, PictureSerializer, SensorDataSerializer, \
    LogSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    """
    API for users detected by face recognition
    retrieve:
        Return user informations.

    list:
        Return all users, ordered by most recently joined.

    create:
        Create a new user.

    delete:
        Remove an existing user.

    partial_update:
        Update one or more fields on an existing user.

    update:
        Update a user.

    encodings:
        Return encodings of specific user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # @action(methods=['get'], detail=True, url_path='pictures', url_name='pictures')
    def encodings(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            pictures = Picture.objects.filter(user_id=pk)
            serializer = PictureSerializer(pictures, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class InfoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Infos to be viewed or edited.
    """
    queryset = Info.objects.all()
    serializer_class = InfoSerializer


class PictureViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Pictures to be viewed or edited.
    """
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class SensorDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows SensorDatas to be viewed or edited.
    """
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer

    def last(self, request, t_type=None):
        try:
            if t_type:
                sensor = SensorData.objects.filter(type=t_type).latest('created')
            else:
                sensor = SensorData.objects.latest('created')
            serializer = SensorDataSerializer(sensor)
            return Response(serializer.data)
        except SensorData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def time_range(self, request, t_from, t_to, t_type=None):
        try:
            t_from = dt.datetime.fromtimestamp(float(t_from))
            t_to = dt.datetime.fromtimestamp(float(t_to))
            if t_type:
                sensors = SensorData.objects.filter(type=t_type)
                sensors = sensors.filter(created__range=(t_from, t_to))
            else:
                sensors = SensorData.objects.filter(created__range=(t_from, t_to))
            serializer = SensorDataSerializer(sensors, many=True)
            return Response(serializer.data)
        except SensorData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class LogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Logs to be viewed or edited.
    """
    queryset = Log.objects.all()
    serializer_class = LogSerializer
