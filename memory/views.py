import datetime as dt
import logging
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Info, User, Encoding, SensorData, Log
from .serializers import InfoSerializer, UserSerializer, EncodingSerializer, SensorDataSerializer, \
    LogSerializer

logger = logging.getLogger('TESTER')


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
    slack_keys_type = 'key_keeper_beaubourg'

    @permission_classes((AllowAny,))
    def slack_keys(self, request):
        logger.info(request.data)
        if 'text' in request.data and 'user_name' in request.data:
            text = request.data['text']
            username = request.data['user_name']
            msg = '?'
            if text == 'add':
                serializer = self.serializer_class(data={'type': self.slack_keys_type, 'data': username})
                if serializer.is_valid():
                    serializer.save()
                    msg = "@{} Tu es maintenant enregisitré comme possedant une clé.".format(username)
            elif text == 'remove':
                key_keeper = Info.objects.filter(type=self.slack_keys_type).filter(data=username)
                if key_keeper:
                    key_keeper.delete()
                    msg = "Je t'ai enlevé de la liste @{}.".format(username)
                else:
                    msg = 'Nope'
            elif text == 'who':
                key_keepers = Info.objects.filter(type=self.slack_keys_type)
                msg = 'Les suricats possédant une clé : s'
                for keeper in key_keepers:
                    msg += ' @{}'.format(keeper.data)
            return Response(msg, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SlackViewSet(viewsets.ModelViewSet):
    """
    API for communicating with Slack
    slack_keys:
        Get informations about key keepers of Beaubourg
    """
    queryset = Info.objects.all()
    serializer_class = InfoSerializer
    hadji = 'M. Hadji'
    slack_keys_type = 'key_keeper_beaubourg'
    slack_keys_away_type = 'key_keeper_beaubourg_away'
    permission_classes = (AllowAny,)
    
    def slack_keys(self, request):
        msg = {
            "response_type": "in_channel",
            "text": "Je n'ai pas compris cette commande\n Les commandes valables sont : help, add, remove, who, away, available",
        }
        logger.info(request.data)
        if 'text' in request.data and 'user_name' in request.data:
            text = request.data['text']
            username = request.data['user_name']
            if text == 'add' or text == 'hadd':
                key_keeper = Info.objects.filter(type__in=[self.slack_keys_type, self.slack_keys_away_type]).filter(
                    data=username)
                if key_keeper:
                    msg['text'] = "Tu es déjà dans la liste."
                else:
                    serializer = self.serializer_class(data={'type': self.slack_keys_type, 'data': self.hadji if text == 'hadd' else username})
                    if serializer.is_valid():
                        serializer.save()
                        msg['text'] = "{}, tu es maintenant enregisitré(e) comme possedant une clé.".format(username)
            elif text == 'remove' or text == 'hremove':
                key_keeper = Info.objects.filter(type__in=[self.slack_keys_type, self.slack_keys_away_type]).filter(
                    data=self.hadji if text == 'hadd' else username)
                if key_keeper:
                    key_keeper.delete()
                    msg['text'] = "Je t'ai enlevé de la liste {}.".format(username)
                else:
                    msg['text'] = "Tu n'étais pas dans la liste."
            elif text == 'who':
                key_keepers = Info.objects.filter(type__in=[self.slack_keys_type, self.slack_keys_away_type])
                msg['text'] = 'Les suricats possédant une clé : '
                if not key_keepers:
                    msg['text'] = "Personne ne s'est enregistré comme possédant une clé."
                for keeper in key_keepers:
                    msg['text'] += '\n- {}'.format(keeper.data)
                    if keeper.type == self.slack_keys_away_type:
                        msg['text'] += '(indisponible)'
            elif text == 'away':
                key_keeper = Info.objects.filter(type__in=[self.slack_keys_type, self.slack_keys_away_type]).filter(
                    data=username)
                if key_keeper:
                    if key_keeper[0].type == self.slack_keys_away_type:
                        msg['text'] = "Tu es déjà considéré comme indisponible"
                    else:
                        logger.info('before')
                        key_keeper[0].type = self.slack_keys_away_type
                        key_keeper[0].save()
                        msg['text'] = "Tu es maintenant considéré comme indisponible"
                else:
                    msg['text'] = "Tu n'étais pas dans la liste."
            elif text == 'available':
                key_keeper = Info.objects.filter(type__in=[self.slack_keys_type, self.slack_keys_away_type]).filter(
                    data=username)
                if key_keeper:
                    if key_keeper[0].type == self.slack_keys_type:
                        msg['text'] = "Tu es déjà considéré comme disponible"
                    else:
                        logger.info('before')
                        key_keeper[0].type = self.slack_keys_type
                        key_keeper[0].save()
                        msg['text'] = "Tu es maintenant considéré comme disponible"
                else:
                    msg['text'] = "Tu n'étais pas dans la liste."
            elif text == 'help':
                msg['text'] = "La commande /bbkey [commande] permet de gérer les possesseurs des clés de Beaubourg\n" \
                              "Voici les commandes : \n" \
                              "- add : Vous ajoute en tant que possesseur de clé\n" \
                              "- remove : Vous enlève de la liste des possesseurs de clé \n" \
                              "- who : Affiche les possesseurs de clé\n" \
                              "- away : Indique que vous possédez une clé mais que vous n'êtes pas en mesure d'ouvrir BB\n" \
                              "- available : Annule la commande précédente\n" \
                              "- hadd/hremove : Commandes spécifiques à M. Hadji"
            return Response(msg, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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
    """
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
