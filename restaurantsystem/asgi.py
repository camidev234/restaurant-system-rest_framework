"""
ASGI config for restaurantsystem project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurantsystem.settings')

from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from orders.consumers.order_consumer import OrderConsumer
from restaurantsystem.middleware.JwtAuthSocketMiddleware import JWTAuthMiddleware
from orders.routing import websocket_urlpatterns as orders_routing_urls

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleware(
        URLRouter(
            orders_routing_urls 
        )
    ),
})
