from django.conf.urls import url
from . import consumers


websocket_urlpatterns = [
    url(r'^ws/chess/(?P<game>[^/]+)/$', consumers.GameConsumer),
]