import datetime as dt
import json

import face_recognition as face_recognition
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Info, User, Encoding, SensorData, Log
from .serializers import InfoSerializer, UserSerializer, EncodingSerializer, SensorDataSerializer, \
    LogSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API for users registered by face recognition
    retrieve:
        Return user information.

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
    def delete(self, request):
        pass
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # @action(methods=['get'], detail=True, url_path='pictures', url_name='pictures')
    def encodings(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            encodings = Encoding.objects.filter(user_id=pk)
            serializer = EncodingSerializer(encodings, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class InfoViewSet(viewsets.ModelViewSet):
    """
    API for storing and retrieving general information
    retrieve:
        Return a information.

    list:
        Return all information.

    create:
        Create a new information.

    delete:
        Remove an existing information.

    partial_update:
        Update one or more fields on an existing information.

    update:
        Update a information.
    """
    queryset = Info.objects.all()
    serializer_class = InfoSerializer


class EncodingViewSet(viewsets.ModelViewSet):
    """
    API for storing and retrieving general encoding
    retrieve:
        Return a encoding.

    list:
        Return all encodings.

    create:
        Create a new encoding.

    delete:
        Remove an existing encoding.

    partial_update:
        Update one or more fields on an existing encoding.

    update:
        Update a encoding.

    picture:
        Allow to add an encoding with a picture
    """
    def picture(self, request):
        if 'picture' in request.FILES:
            file = request.FILES['picture']
            img = face_recognition.load_image_file(file)
            encodings = face_recognition.face_encodings(img, None, 10)
            if encodings:
                face = " ".join(map(str, encodings[0]))
                new_dict = request.data.copy()
                new_dict.update({'value': face})
                serializer = self.get_serializer(data=new_dict)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                return Response('No face on the picture.', status=status.HTTP_406_NOT_ACCEPTABLE)

        else:
            return Response({'picture': ['This field is required']}, status=status.HTTP_400_BAD_REQUEST)
    queryset = Encoding.objects.all()
    serializer_class = EncodingSerializer


class SensorDataViewSet(viewsets.ModelViewSet):
    """
    API for storing and retrieving sensor information
    retrieve:
        Return a sensor information.

    list:
        Return all sensor information.

    create:
        Create a new sensor information.

    delete:
        Remove an existing sensor information.

    partial_update:
        Update one or more fields on an existing sensor information.

    update:
        Update a sensor information.

    last:
        Return the last sensor information of the type defined (all by default)

    time_range:
        Return  all sensor information created on the time range of the type (all by default) defined
    """
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer

    def list(self, request, t_type=None):
        if t_type:
            sensors = SensorData.objects.filter(type=t_type)

        else:
            sensors = SensorData.objects.all()
        serializer = self.get_serializer(sensors, many=True)
        return Response(serializer.data)

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
    API for storing and retrieving logs
    retrieve:
        Return a log.

    list:
        Return all logs.

    create:
        Create a new log.

    delete:
        Remove an existing log.

    partial_update:
        Update one or more fields on an existing log.

    update:
        Update a log.
    """
    queryset = Log.objects.all()
    serializer_class = LogSerializer
