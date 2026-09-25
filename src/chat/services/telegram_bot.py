"""Telegram Bot API client and chat bridge helpers."""

from __future__ import annotations

import html
import logging
from typing import Any

import requests
from django.conf import settings
from django.db import transaction

from src.chat.models import ChatMessage, SenderType, SessionStatus, TelegramChatSession

logger = logging.getLogger(__name__)

TELEGRAM_API = "https://api.telegram.org"
DEFAULT_TIMEOUT = 5
MAX_TEXT_LEN = 4000

_HINT_PLAIN = (
    "Это сообщение не ушло на сайт.\n"
    "Нажмите «Ответить» на карточку «Сообщение с сайта» и напишите текст ещё раз.\n"
    "Обычное сообщение в этот чат посетитель не видит.\n"
    "На заявку с формы так ответить нельзя: в карточке «Новая заявка» "
    "откройте Дзвінок, WhatsApp или Telegram."
)
_HINT_UNLINKED = (
    "Ответ не привязан к сообщению с сайта.\n"
    "Нажмите «Ответить» именно на карточку «Сообщение с сайта», "
    "а не на заявку и не на эту подсказку."
)
_HINT_CLOSED = "Этот диалог на сайте уже закрыт. Ответ посетителю не отправлен."


class TelegramBotError(Exception):
    """Base error for Telegram Bot API failures."""


class TelegramRateLimitError(TelegramBotError):
    """Raised when Telegram returns HTTP 429."""

    def __init__(self, retry_after: int | None = None) -> None:
        self.retry_after = retry_after
        super().__init__(f"Telegram rate limit (retry_after={retry_after})")


class TelegramNetworkError(TelegramBotError):
    """Network / timeout errors talking to Telegram."""


def _bot_token() -> str:
    return (getattr(settings, "TELEGRAM_BOT_TOKEN", "") or "").strip()


def _admin_chat_id() -> str:
    return str(getattr(settings, "TELEGRAM_CHAT_ID", "") or "").strip()


def _api_url(method: str) -> str:
    token = _bot_token()
    if not token:
        raise TelegramBotError("TELEGRAM_BOT_TOKEN is not configured")
    return f"{TELEGRAM_API}/bot{token}/{method}"


def call_telegram_api(
    method: str,
    payload: dict[str, Any] | None = None,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """POST to Telegram Bot API. Raises TelegramBotError subclasses on failure."""
    url = _api_url(method)
    try:
        response = requests.post(url, json=payload or {}, timeout=timeout)
    except requests.Timeout as exc:
        raise TelegramNetworkError("Telegram API timeout") from exc
    except requests.RequestException as exc:
        raise TelegramNetworkError(f"Telegram API network error: {exc}") from exc

    if response.status_code == 429:
        retry_after = None
        try:
            retry_after = int(response.headers.get("Retry-After", 0)) or None
            data = response.json()
            retry_after = data.get("parameters", {}).get("retry_after") or retry_after
        except (ValueError, TypeError, requests.JSONDecodeError):
            pass
        raise TelegramRateLimitError(retry_after=retry_after)

    try:
        data = response.json()
    except ValueError as exc:
        raise TelegramBotError("Invalid JSON from Telegram API") from exc

    if response.status_code >= 400 or not data.get("ok"):
        description = data.get("description") if isinstance(data, dict) else None
        raise TelegramBotError(
            f"Telegram API error {response.status_code}: {description or response.text}"
        )
    return data


def set_webhook(url: str, secret_token: str) -> dict[str, Any]:
    return call_telegram_api(
        "setWebhook",
        {
            "url": url,
            "secret_token": secret_token,
            "allowed_updates": ["message"],
            "drop_pending_updates": False,
        },
        timeout=10,
    )


def delete_webhook() -> dict[str, Any]:
    return call_telegram_api("deleteWebhook", {"drop_pending_updates": False}, timeout=10)


def send_message(
    chat_id: str | int,
    text: str,
    *,
    parse_mode: str | None = "HTML",
    reply_to_message_id: int | None = None,
    reply_markup: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "chat_id": chat_id,
        "text": text[:4096],
        "disable_web_page_preview": True,
    }
    if parse_mode:
        payload["parse_mode"] = parse_mode
    if reply_to_message_id is not None:
        payload["reply_to_message_id"] = reply_to_message_id
    if reply_markup is not None:
        payload["reply_markup"] = reply_markup
    return call_telegram_api("sendMessage", payload)


def forward_site_message(session: TelegramChatSession, message: ChatMessage) -> int | None:
    """Send site user message to admin chat. Returns Telegram message_id."""
    admin_chat = _admin_chat_id()
    if not _bot_token() or not admin_chat:
        logger.info("Telegram credentials missing — skip chat forward")
        return None

    short_id = str(session.session_id).split("-")[0]
    safe_text = html.escape(message.text[:MAX_TEXT_LEN], quote=False)
    body = (
        "<b>Сообщение с сайта</b>\n"
        f"Сессия: <code>{html.escape(short_id)}</code>\n"
        "Чтобы ответ появился у посетителя на сайте, нажмите «Ответить» "
        "на это сообщение и напишите текст.\n"
        "Обычное сообщение в этот чат на сайт не попадает.\n"
        "—\n"
        f"{safe_text}"
    )
    try:
        data = send_message(
            admin_chat,
            body,
            reply_markup={"force_reply": True},
        )
    except TelegramRateLimitError:
        logger.warning("Telegram rate limit while forwarding session %s", session.session_id)
        raise
    except TelegramBotError:
        logger.exception("Failed to forward chat message %s", message.pk)
        raise

    result = data.get("result") or {}
    tg_id = result.get("message_id")
    if tg_id is not None:
        message.telegram_message_id = int(tg_id)
        message.save(update_fields=["telegram_message_id"])
    return message.telegram_message_id


def _hint_admin(admin_chat: str, text: str) -> None:
    try:
        send_message(admin_chat, html.escape(text, quote=False))
    except TelegramBotError:
        logger.exception("Failed to send Telegram reply hint")


def handle_webhook_update(payload: dict[str, Any]) -> bool:
    """
    Process a Telegram update.
    Returns True if a chat message was stored.
    Only reply-to messages from the configured admin chat are accepted.
    """
    message = payload.get("message")
    if not isinstance(message, dict):
        return False

    admin_chat = _admin_chat_id()
    if not admin_chat:
        logger.warning("TELEGRAM_CHAT_ID missing — ignore webhook")
        return False

    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    if chat_id is None or str(chat_id) != str(admin_chat):
        logger.info("Ignore webhook from unexpected chat_id=%s", chat_id)
        return False

    text = (message.get("text") or "").strip()
    reply_to = message.get("reply_to_message")
    if not isinstance(reply_to, dict):
        _hint_admin(admin_chat, _HINT_PLAIN)
        return False

    reply_msg_id = reply_to.get("message_id")
    if reply_msg_id is None or not text:
        _hint_admin(admin_chat, _HINT_PLAIN)
        return False

    tg_message_id = message.get("message_id")

    with transaction.atomic():
        original = (
            ChatMessage.objects.select_for_update()
            .filter(
                telegram_message_id=int(reply_msg_id),
                sender_type=SenderType.SITE_USER,
            )
            .select_related("session")
            .first()
        )
        if original is None:
            logger.info("No site message for reply_to=%s", reply_msg_id)
            hint = _HINT_UNLINKED
        elif original.session.status != SessionStatus.ACTIVE:
            logger.info("Session %s is closed — ignore reply", original.session.session_id)
            hint = _HINT_CLOSED
        else:
            hint = ""

    if hint:
        _hint_admin(admin_chat, hint)
        return False

    session = original.session

    with transaction.atomic():
        if tg_message_id is not None:
            exists = ChatMessage.objects.filter(
                telegram_message_id=int(tg_message_id),
                sender_type=SenderType.TELEGRAM_ADMIN,
            ).exists()
            if exists:
                return False

        ChatMessage.objects.create(
            session=session,
            sender_type=SenderType.TELEGRAM_ADMIN,
            text=text[:MAX_TEXT_LEN],
            telegram_message_id=int(tg_message_id) if tg_message_id is not None else None,
        )
        session.save(update_fields=["updated_at"])

    return True
