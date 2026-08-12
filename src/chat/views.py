import json
import logging
import secrets
import uuid

from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import translation
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from src.chat.models import ChatMessage, SenderType, SessionStatus, TelegramChatSession
from src.chat.services.telegram_bot import (
    TelegramBotError,
    TelegramRateLimitError,
    forward_site_message,
    handle_webhook_update,
)
from src.core.rate_limit import client_ip, is_rate_limited

logger = logging.getLogger(__name__)

RATE_LIMIT = 30
RATE_WINDOW = 3600
MAX_TEXT = 2000
SESSION_COOKIE = "chat_uid"
_ALLOWED_LANGS = {code for code, _name in settings.LANGUAGES}


def _activate_request_language(request: HttpRequest) -> str:
    """API chat поза i18n_patterns — мову беремо з хедера сторінки."""
    raw = (
        request.headers.get("X-Requested-Language")
        or request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
        or ""
    ).strip().lower()
    lang = raw[:2] if raw[:2] in _ALLOWED_LANGS else ""
    if not lang:
        lang = translation.get_language_from_request(request, check_path=False) or settings.LANGUAGE_CODE
        lang = lang[:2]
    if lang not in _ALLOWED_LANGS:
        lang = settings.LANGUAGE_CODE
    translation.activate(lang)
    request.LANGUAGE_CODE = lang
    return lang


def _client_ip(request: HttpRequest) -> str:
    return client_ip(request)


def _rate_limited(ip: str, *, action: str) -> bool:
    return is_rate_limited(
        f"chat_rate:{action}:{ip}",
        limit=RATE_LIMIT,
        window=RATE_WINDOW,
    )


def _parse_uuid(value: str | None) -> uuid.UUID | None:
    if not value:
        return None
    try:
        return uuid.UUID(str(value))
    except (ValueError, TypeError, AttributeError):
        return None


def _user_identifier(request: HttpRequest) -> str:
    raw = (
        request.POST.get("user_identifier")
        or request.GET.get("user_identifier")
        or request.COOKIES.get(SESSION_COOKIE)
        or ""
    ).strip()
    if raw and len(raw) <= 64:
        return raw
    return secrets.token_urlsafe(24)


def _get_active_session(
    session_id: uuid.UUID,
    user_identifier: str,
) -> TelegramChatSession | None:
    return TelegramChatSession.objects.filter(
        session_id=session_id,
        user_identifier=user_identifier,
        status=SessionStatus.ACTIVE,
    ).first()


@csrf_exempt
@require_http_methods(["POST"])
def telegram_webhook(request: HttpRequest) -> HttpResponse:
    expected = (getattr(settings, "TELEGRAM_WEBHOOK_SECRET", "") or "").strip()
    provided = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
    if not expected or not secrets.compare_digest(provided, expected):
        return HttpResponse(status=403)

    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except (UnicodeDecodeError, json.JSONDecodeError):
        logger.warning("Invalid JSON on telegram webhook")
        return HttpResponse(status=400)

    if not isinstance(payload, dict):
        return HttpResponse(status=400)

    try:
        handle_webhook_update(payload)
    except Exception:
        logger.exception("Webhook processing failed")
        # Always 200 to Telegram after auth — avoid retry storms on app bugs
        return HttpResponse(status=200)

    return HttpResponse(status=200)


@require_http_methods(["POST"])
def chat_session(request: HttpRequest) -> JsonResponse:
    _activate_request_language(request)
    ip = _client_ip(request)
    if _rate_limited(ip, action="session"):
        return JsonResponse({"error": "rate_limited"}, status=429)

    user_identifier = _user_identifier(request)
    session_id = _parse_uuid(request.POST.get("session_id"))

    session = None
    if session_id:
        session = TelegramChatSession.objects.filter(
            session_id=session_id,
            user_identifier=user_identifier,
        ).first()
        if session and session.status == SessionStatus.CLOSED:
            session = None

    if session is None:
        session = TelegramChatSession.objects.create(user_identifier=user_identifier)

    response = JsonResponse(
        {
            "session_id": str(session.session_id),
            "user_identifier": session.user_identifier,
            "status": session.status,
        }
    )
    response.set_cookie(
        SESSION_COOKIE,
        session.user_identifier,
        max_age=60 * 60 * 24 * 90,
        httponly=True,
        samesite="Lax",
        secure=request.is_secure(),
    )
    return response


@require_http_methods(["POST"])
def chat_send(request: HttpRequest) -> HttpResponse:
    _activate_request_language(request)
    ip = _client_ip(request)
    if _rate_limited(ip, action="send"):
        return render(
            request,
            "partials/chat-error.html",
            {"error": "rate_limited"},
            status=429,
        )

    user_identifier = _user_identifier(request)
    session_id = _parse_uuid(request.POST.get("session_id"))
    text = (request.POST.get("text") or "").strip()

    if not session_id or not text:
        return render(
            request,
            "partials/chat-error.html",
            {"error": "invalid"},
            status=422,
        )

    if len(text) > MAX_TEXT:
        text = text[:MAX_TEXT]

    session = _get_active_session(session_id, user_identifier)
    if session is None:
        return render(
            request,
            "partials/chat-error.html",
            {"error": "session"},
            status=404,
        )

    message = ChatMessage.objects.create(
        session=session,
        sender_type=SenderType.SITE_USER,
        text=text,
    )
    try:
        forward_site_message(session, message)
    except TelegramRateLimitError:
        logger.warning("Rate limited forwarding chat message %s", message.pk)
    except TelegramBotError:
        logger.exception("Telegram forward failed for message %s", message.pk)

    messages = session.messages.order_by("created_at")
    return render(
        request,
        "partials/chat-messages.html",
        {"messages": messages, "session": session},
    )


@require_http_methods(["GET"])
def chat_messages(request: HttpRequest) -> HttpResponse:
    _activate_request_language(request)
    user_identifier = _user_identifier(request)
    session_id = _parse_uuid(request.GET.get("session_id"))
    after_id = request.GET.get("after_id", "")

    if not session_id:
        return render(request, "partials/chat-messages.html", {"messages": []})

    session = TelegramChatSession.objects.filter(
        session_id=session_id,
        user_identifier=user_identifier,
    ).first()
    if session is None:
        return render(request, "partials/chat-messages.html", {"messages": []})

    qs = session.messages.order_by("created_at")
    if after_id.isdigit():
        qs = qs.filter(pk__gt=int(after_id))

    return render(
        request,
        "partials/chat-messages.html",
        {
            "messages": qs,
            "session": session,
            "poll_append": bool(after_id.isdigit()),
        },
    )
