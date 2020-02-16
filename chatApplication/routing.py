from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    )),
})
