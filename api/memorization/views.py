from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from memorization.models import Info, User, Picture, SensorData, Log
from memorization.serializers import InfoSerializer, UserSerializer, PictureSerializer, SensorDataSerializer, LogSerializer
from rest_framework.decorators import action
from django.http import JsonResponse

from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get'], detail=True)
    def pictures(self, request, id):
        pass


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


class LogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Logs to be viewed or edited.
    """
    queryset = Log.objects.all()
    serializer_class = LogSerializer
