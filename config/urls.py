from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('api-token-auth/', views.obtain_auth_token),
    path('api/', include('config.api_router')),
    path('accounts/', include('allauth.urls')),
    path('', include('core.urls')),
]
