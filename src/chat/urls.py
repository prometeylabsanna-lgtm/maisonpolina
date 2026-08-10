from django.urls import path

from src.chat import views

app_name = "chat"

urlpatterns = [
    path("telegram/webhook/", views.telegram_webhook, name="telegram_webhook"),
    path("chat/session/", views.chat_session, name="session"),
    path("chat/send/", views.chat_send, name="send"),
    path("chat/messages/", views.chat_messages, name="messages"),
]
