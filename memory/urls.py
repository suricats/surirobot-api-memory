from django.urls import path, include, re_path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('encodings', views.EncodingViewSet)
router.register('sensors', views.SensorDataViewSet)
router.register('logs', views.LogViewSet)
router.register('infos', views.InfoViewSet)
"""
user_list = views.UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
user_detail = views.UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
"""
user_encodings = views.UserViewSet.as_view({
    'get': 'encodings'
})
sensor_list = views.SensorDataViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
sensor_last = views.SensorDataViewSet.as_view({
    'get': 'last'
})
sensor_duration = views.SensorDataViewSet.as_view({
    'get': 'time_range'
})
slack_keys = views.InfoViewSet.as_view({
    'post': 'slack_keys'
})

urlpatterns = [

    # re_path(r'^users/$', user_list, name='user-list'),
    # re_path(r'^users/(?P<pk>[0-9]+)/$', user_list, name='user-detail'),
    re_path(r'^slack/keys/$', slack_keys, name='slack_keys'),
    re_path(r'^users/(?P<pk>[0-9]+)/encodings/$', user_encodings, name='user_encodings'),
    re_path(r'^sensors/last/$', sensor_last, name='sensor_last'),
    re_path(r'^sensors/last/(?P<t_type>[\w\-]+)/$', sensor_last, name='sensor_last_type'),
    re_path(r'^sensors/(?P<t_type>[\w\-]+)/$', sensor_list, name='sensor_list'),
    re_path(r'^sensors/(?P<t_from>[0-9]+)/(?P<t_to>[0-9]+)/(?P<t_type>[\w\-]+)/$', sensor_duration, name='sensor_duration_t'),
    re_path(r'^sensors/(?P<t_from>[0-9]+)/(?P<t_to>[0-9]+)/$', sensor_duration, name='sensor_duration'),
    path('', include(router.urls)),
]
