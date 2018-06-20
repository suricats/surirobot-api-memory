from django.conf.urls import url, include
from rest_framework import routers
from memorization import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('pictures', views.PictureViewSet)
router.register('sensors', views.SensorDataViewSet)
router.register('logs', views.LogViewSet)
router.register('infos', views.InfoViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
