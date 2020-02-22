from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('chess/', include('game.urls')),
    path('', include('core.urls')),
]
