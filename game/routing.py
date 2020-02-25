from django.conf.urls import url
from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/chess/<str:game>/', consumers.GameConsumer),
    path('ws/notifications/<str:username>/', consumers.NotificationConsumer),
]