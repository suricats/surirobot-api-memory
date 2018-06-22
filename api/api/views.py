from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
import json

@api_view(['POST'])
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
