from django.urls import re_path
from . import consumer

websocket_urlpatterns = [
    re_path(r'ws/charger/(?P<charger_id>\w+)/$', consumer.ChargePointConsumer.as_asgi()),
]