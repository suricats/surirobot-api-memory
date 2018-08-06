from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from django.template import loader
from rest_framework.permissions import IsAdminUser
import json


@api_view(['POST'])
@permission_classes((IsAdminUser, ))
def create_auth(request):
    try:
        print(request.body)
        if request.method == 'POST':
            json_data = json.loads(request.body.decode("utf-8", "strict"))
            email = json_data['email']
            username = json_data['username']
            password = json_data['password']
            User.objects.create_user(
                username,
                email,
                password
            )
        return Response("OK", status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


def home(request):
    if request.method == 'GET':
        return HttpResponse("<html><body>Surirobot Memory API</body></html>")


def login(request):
    template = loader.get_template('rest_framework/login_base.html')
    context = {}
    return HttpResponse(template.render(context, request))

@api_view(['GET'])
def swagger_file(request):
    try:
        content = open('./docs/openapi.yaml', 'r')
        return Response(content)
    except FileNotFoundError:
        return Response(status=404)