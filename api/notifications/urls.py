from django.urls import path

from . import views

notifications_list = views.NotificationViewSet.as_view({
    'get': 'get_notifications',
    'post': 'expiration'
})

urlpatterns = [
    path('', notifications_list, name='notifications_list')
]
