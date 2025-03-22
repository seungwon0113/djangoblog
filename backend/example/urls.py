from django.urls import path
from . import views

urlpatterns = [
    path("chat/language-tutor/", views.language_tutor_chat, name="language_tutor_chat"),
]
