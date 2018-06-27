
from django.contrib import admin
from django.urls import path, include
from memorization import urls
from rest_framework.authtoken import views
from . import views as general_views
from django.views.generic.base import RedirectView

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view()

urlpatterns = [
    path('', RedirectView.as_view(url='/docs/', permanent=False), name='docs'),
    path('docs/', schema_view),
    path('accounts/login/', RedirectView.as_view(url='/api-auth/login', permanent=False), name='login'),
    path('accounts/profile/', RedirectView.as_view(url='/', permanent=False), name='login'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('memorize/', include('memorization.urls')),
    path('login/', views.obtain_auth_token),
    path('register/', general_views.create_auth)
]
