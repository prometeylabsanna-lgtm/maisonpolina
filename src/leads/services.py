import html
import logging

import requests
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from src.leads.models import Lead

logger = logging.getLogger(__name__)


def notify(lead: Lead) -> None:
    """Send Telegram and email. Never raise to the caller for channel failures."""
    errors = []
    try:
        _send_telegram(lead)
    except Exception:
        logger.exception("Telegram notify failed for lead %s", lead.pk)
        errors.append("telegram")
    try:
        _send_email(lead)
    except Exception:
        logger.exception("Email notify failed for lead %s", lead.pk)
        errors.append("email")
    if not errors:
        lead.mark_notified()


def _admin_url(lead: Lead) -> str:
    path = reverse("admin:leads_lead_change", args=[lead.pk])
    base = getattr(settings, "SITE_URL", "").rstrip("/")
    return f"{base}{path}"


def _send_telegram(lead: Lead) -> None:
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    if not token or not chat_id:
        logger.info("Telegram credentials missing — skip")
        return

    def e(value: str) -> str:
        return html.escape(str(value or "—"), quote=False)

    text = (
        "<b>Новая заявка</b>\n"
        f"Имя: {e(lead.name)}\n"
        f"Контакт: {e(lead.contact)}\n"
        f"Формат: {e(lead.service)}\n"
        f"Источник: {e(lead.get_source_display())}\n"
        f"Язык: {e(lead.language)}\n"
        f"Время: {e(lead.created_at.strftime('%Y-%m-%d %H:%M'))}\n"
        f"Сообщение: {e(lead.message)}\n"
        f"<a href=\"{html.escape(_admin_url(lead))}\">Открыть в админке</a>"
    )
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    response = requests.post(
        url,
        json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        },
        timeout=5,
    )
    response.raise_for_status()


def _send_email(lead: Lead) -> None:
    recipient = settings.DEFAULT_FROM_EMAIL
    if not recipient:
        return
    subject = f"Новая заявка: {lead.name}"
    body = (
        f"Имя: {lead.name}\n"
        f"Контакт: {lead.contact}\n"
        f"Формат: {lead.service}\n"
        f"Источник: {lead.get_source_display()}\n"
        f"Язык: {lead.language}\n"
        f"Время: {lead.created_at}\n"
        f"Сообщение:\n{lead.message}\n\n"
        f"Админка: {_admin_url(lead)}\n"
    )
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [recipient],
        fail_silently=False,
    )


def resend_pending_notifications(limit: int = 50) -> int:
    qs = Lead.objects.filter(notified_at__isnull=True).order_by("created_at")[:limit]
    count = 0
    for lead in qs:
        notify(lead)
        lead.refresh_from_db(fields=["notified_at"])
        if lead.notified_at:
            count += 1
    return count
