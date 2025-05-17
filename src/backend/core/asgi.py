import os, django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import boxes.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

application = ProtocolTypeRouter({
    "http":   get_asgi_application(),
    "websocket": URLRouter(boxes.routing.websocket_urlpatterns),
})
