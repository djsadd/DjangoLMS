from django.urls import path
from .views import chat_page, chat_bot_page

urlpatterns = [
    path('', chat_page, name='chat_page'),
    path('bot/', chat_bot_page, name='chat_bot_page'),
]
