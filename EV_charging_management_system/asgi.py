"""
ASGI config for EV_charging_management_system project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from api import routing  
from api.consumer import ChargePointConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EV_charging_management_system.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/charge_point/<str:charger_id>/", ChargePointConsumer.as_asgi()),
        ])
    ),
})