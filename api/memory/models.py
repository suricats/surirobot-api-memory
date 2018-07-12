from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Info(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    type = models.TextField(max_length=50, blank=False)
    data = models.TextField(blank=False)

    class Meta:
        ordering = ('created',)


class User(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    firstname = models.TextField(max_length=50, null=False)
    lastname = models.TextField(max_length=70, null=True)
    email = models.EmailField(max_length=254, null=True)

    class Meta:
        ordering = ('created',)


class SensorData(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    type = models.TextField(max_length=50, blank=False)
    data = models.TextField(blank=False)
    location = models.TextField(max_length=50, blank=False)

    class Meta:
        ordering = ('created',)


class Encoding(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    value = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)


class Log(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    value = models.IntegerField()

    class Meta:
        ordering = ('created',)


