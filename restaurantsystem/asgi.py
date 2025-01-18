"""
ASGI config for restaurantsystem project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from orders.consumers.order_consumer import OrderConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurantsystem.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                path("ws/orders/<int:order_id>/", OrderConsumer.as_asgi()),  # Definir la ruta de websocket
            ]
        )
    ),
})
