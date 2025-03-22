from django.urls import path
from .consumers import LanguageTutorChatConsumer

websocket_urlpatterns = [
    path("ws/example/chat/language-tutor/", LanguageTutorChatConsumer.as_asgi()),
]
