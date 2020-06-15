from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/dialogs/(?P<room_name>\d+-\d+)/$', consumers.ChatConsumer),
]
