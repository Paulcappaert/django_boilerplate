from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import core.routing
import task

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            core.routing.websocket_urlpatterns
        )
    ),
    "channel": ChannelNameRouter({
        "chat-bot": task.PrintConsumer.as_asgi(),
    })
})
