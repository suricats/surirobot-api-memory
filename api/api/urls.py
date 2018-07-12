
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from rest_framework.authtoken import views
from .swagger_schema import SwaggerSchemaView

from . import views as general_views


urlpatterns = [
    path('', RedirectView.as_view(url='/docs/', permanent=False), name='docs'),
    path('docs/', SwaggerSchemaView.as_view()),
    path('accounts/login/', RedirectView.as_view(url='/api-auth/login', permanent=False), name='login'),
    path('accounts/profile/', RedirectView.as_view(url='/', permanent=False), name='login'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('api/memory/', include(('memory.urls', 'reviews'), namespace='Memory')),
    path('login/', views.obtain_auth_token),
    path('register/', general_views.create_auth)
]
