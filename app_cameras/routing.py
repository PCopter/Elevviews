from django.urls import re_path
from app_cameras.consumers import WebRTCConsumer

websocket_urlpatterns = [
    re_path(r'ws/signaling/$', WebRTCConsumer.as_asgi()),
]
