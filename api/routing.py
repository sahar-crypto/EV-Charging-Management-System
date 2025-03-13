from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/charger/(?P<charger_id>\w+)/$', consumers.ChargePointConsumer.as_asgi()),
]
