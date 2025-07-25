from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/socket-server/(?P<id>[^/]+)/$', consumers.ChatConsumer.as_asgi())
]
