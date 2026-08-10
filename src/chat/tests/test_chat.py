import json
from unittest.mock import patch

import pytest
from django.test import Client
from django.urls import reverse

from src.chat.models import ChatMessage, SenderType, TelegramChatSession


@pytest.mark.django_db
def test_create_session(client: Client):
    url = reverse("chat:session")
    response = client.post(url, {})
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"]
    assert data["user_identifier"]
    assert TelegramChatSession.objects.count() == 1


@pytest.mark.django_db
def test_reuse_session(client: Client):
    url = reverse("chat:session")
    first = client.post(url, {}).json()
    second = client.post(
        url,
        {
            "session_id": first["session_id"],
            "user_identifier": first["user_identifier"],
        },
    ).json()
    assert first["session_id"] == second["session_id"]
    assert TelegramChatSession.objects.count() == 1


@pytest.mark.django_db
def test_send_and_list_messages(client: Client):
    session = client.post(reverse("chat:session"), {}).json()
    with patch("src.chat.views.forward_site_message", return_value=101):
        response = client.post(
            reverse("chat:send"),
            {
                "session_id": session["session_id"],
                "user_identifier": session["user_identifier"],
                "text": "Здравствуйте",
            },
        )
    assert response.status_code == 200
    assert ChatMessage.objects.count() == 1
    assert "Здравствуйте".encode() in response.content

    listed = client.get(
        reverse("chat:messages"),
        {
            "session_id": session["session_id"],
            "user_identifier": session["user_identifier"],
        },
    )
    assert listed.status_code == 200
    assert "Здравствуйте".encode() in listed.content


@pytest.mark.django_db
def test_send_rejects_foreign_session(client: Client):
    own = client.post(reverse("chat:session"), {}).json()
    other = TelegramChatSession.objects.create(user_identifier="other-user")
    response = client.post(
        reverse("chat:send"),
        {
            "session_id": str(other.session_id),
            "user_identifier": own["user_identifier"],
            "text": "hack",
        },
    )
    assert response.status_code == 404
    assert ChatMessage.objects.count() == 0


@pytest.mark.django_db
def test_webhook_requires_secret(client: Client, settings):
    settings.TELEGRAM_WEBHOOK_SECRET = "secret-token"
    settings.TELEGRAM_CHAT_ID = "12345"
    url = reverse("chat:telegram_webhook")
    response = client.post(
        url,
        data=json.dumps({"update_id": 1}),
        content_type="application/json",
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_webhook_reply_creates_admin_message(client: Client, settings):
    settings.TELEGRAM_WEBHOOK_SECRET = "secret-token"
    settings.TELEGRAM_CHAT_ID = "999"
    session = TelegramChatSession.objects.create(user_identifier="u1")
    ChatMessage.objects.create(
        session=session,
        sender_type=SenderType.SITE_USER,
        text="Hello",
        telegram_message_id=50,
    )
    payload = {
        "update_id": 10,
        "message": {
            "message_id": 77,
            "chat": {"id": 999},
            "text": "Ответ администратора",
            "reply_to_message": {"message_id": 50},
        },
    }
    response = client.post(
        reverse("chat:telegram_webhook"),
        data=json.dumps(payload),
        content_type="application/json",
        HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN="secret-token",
    )
    assert response.status_code == 200
    admin_msg = ChatMessage.objects.filter(sender_type=SenderType.TELEGRAM_ADMIN).get()
    assert admin_msg.text == "Ответ администратора"
    assert admin_msg.telegram_message_id == 77


@pytest.mark.django_db
def test_webhook_ignores_wrong_chat(client: Client, settings):
    settings.TELEGRAM_WEBHOOK_SECRET = "secret-token"
    settings.TELEGRAM_CHAT_ID = "999"
    session = TelegramChatSession.objects.create(user_identifier="u1")
    ChatMessage.objects.create(
        session=session,
        sender_type=SenderType.SITE_USER,
        text="Hello",
        telegram_message_id=50,
    )
    payload = {
        "update_id": 11,
        "message": {
            "message_id": 78,
            "chat": {"id": 111},
            "text": "spam",
            "reply_to_message": {"message_id": 50},
        },
    }
    response = client.post(
        reverse("chat:telegram_webhook"),
        data=json.dumps(payload),
        content_type="application/json",
        HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN="secret-token",
    )
    assert response.status_code == 200
    assert ChatMessage.objects.filter(sender_type=SenderType.TELEGRAM_ADMIN).count() == 0


@pytest.mark.django_db
def test_webhook_invalid_json(client: Client, settings):
    settings.TELEGRAM_WEBHOOK_SECRET = "secret-token"
    response = client.post(
        reverse("chat:telegram_webhook"),
        data="{not-json",
        content_type="application/json",
        HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN="secret-token",
    )
    assert response.status_code == 400
