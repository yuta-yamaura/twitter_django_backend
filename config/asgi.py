"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django_applecation = get_asgi_application()

from . import urls
from directmessages.middlewares import WebSocketJWTAuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from config import urls

application = ProtocolTypeRouter({
    "http": django_applecation,
    "websocket": WebSocketJWTAuthMiddleware(URLRouter(urls.websocket_urlpatterns)),
})
