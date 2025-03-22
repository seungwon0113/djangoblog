from django.shortcuts import render


def language_tutor_chat(request):
    return render(request, "pyhub_ai/chat_room_ws.html", {
        "ws_url": "/ws/example/chat/language-tutor/",
    })
