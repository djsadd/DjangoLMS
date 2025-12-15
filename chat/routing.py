from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),       # старый групповой чат
    re_path(r'ws/chat/bot/$', consumers.ChatBotConsumer.as_asgi()),  # новый чат с ботом
]
