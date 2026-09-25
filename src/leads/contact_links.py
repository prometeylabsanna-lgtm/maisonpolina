"""Turn a free-text lead contact into call, mail, and messenger links."""

from __future__ import annotations

import re

from django.utils.html import format_html_join

_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_NICK = re.compile(r"^@[A-Za-z][A-Za-z0-9_]{4,31}$")
_TME = re.compile(
    r"(?:https?://)?(?:t\.me|telegram\.me)/([A-Za-z][A-Za-z0-9_]{4,31})/?$",
    re.IGNORECASE,
)


def contact_actions(raw: str) -> list[dict[str, str]]:
    text = (raw or "").strip()
    if not text:
        return []
    if _EMAIL.match(text):
        return [{"label": "Лист", "url": f"mailto:{text}"}]
    if _NICK.match(text):
        return [{"label": "Telegram", "url": f"https://t.me/{text[1:]}"}]
    tme = _TME.match(text)
    if tme:
        return [{"label": "Telegram", "url": f"https://t.me/{tme.group(1)}"}]
    if re.search(r"[A-Za-z]", text):
        return []
    digits = re.sub(r"\D", "", text)
    if not 7 <= len(digits) <= 15:
        return []
    if len(digits) == 10 and digits.startswith("0"):
        intl = f"380{digits[1:]}"
    else:
        intl = digits.lstrip("0") or digits
    actions = [{"label": "Дзвінок", "url": f"tel:+{intl}"}]
    if 8 <= len(intl) <= 15:
        actions.append({"label": "WhatsApp", "url": f"https://wa.me/{intl}"})
    return actions


def contact_links_html(raw: str) -> str:
    actions = contact_actions(raw)
    if not actions:
        return ""
    return format_html_join(
        " · ",
        '<a href="{}" target="_blank" rel="noopener noreferrer">{}</a>',
        ((item["url"], item["label"]) for item in actions),
    )


def contact_links_telegram(raw: str) -> str:
    return format_html_join(
        " · ",
        '<a href="{}">{}</a>',
        ((item["url"], item["label"]) for item in contact_actions(raw)),
    )
