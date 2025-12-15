import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Твой путь к settings.py

django_asgi_app = get_asgi_application()

import chat.routing  # <= ⚠️ тут у тебя импорт (возможно, проблема)
from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter(
        chat.routing.websocket_urlpatterns
    ),
})
