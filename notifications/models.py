from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


class Notification(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
    type = models.TextField(max_length=50, blank=False)
    target = models.TextField(blank=False)
    data = models.TextField(blank=False)
    is_expired = models.BooleanField(blank=False)
    class Meta:
        ordering = ('expiration_date',)


