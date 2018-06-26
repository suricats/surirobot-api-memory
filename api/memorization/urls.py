from django.urls import path, include
from rest_framework import routers
from memorization import views
from rest_framework_swagger import renderers
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view()

router = routers.DefaultRouter()
# router.register('docs', schema_view)
router.register('users', views.UserViewSet)
router.register('pictures', views.PictureViewSet)
router.register('sensors', views.SensorDataViewSet)
router.register('logs', views.LogViewSet)
router.register('infos', views.InfoViewSet)

urlpatterns = [
    path('docs/', schema_view),
    path('', include(router.urls))
]
