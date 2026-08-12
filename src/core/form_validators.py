from __future__ import annotations

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

MSG_NAME_DIGITS = _("Ім'я не повинно містити цифр.")
MSG_PHONE = _(
    "Номер телефону не може містити літер та має бути не довшим за 14 цифр."
)
MSG_MESSAGE_MIN = _("Текст відгуку повинен містити мінімум 2 символи.")

_NAME_DIGIT = re.compile(r"[0-9]")
_PHONE_ALLOWED = re.compile(r"^[0-9+\-()\s]*$")
_MAX_PHONE_DIGITS = 14
_MIN_MESSAGE = 2


def validate_person_name(value: str) -> str:
    name = (value or "").strip()
    if _NAME_DIGIT.search(name):
        raise ValidationError(MSG_NAME_DIGITS)
    return name


def validate_phone(value: str) -> str:
    contact = (value or "").strip()
    digits = sum(ch.isdigit() for ch in contact)
    if not _PHONE_ALLOWED.fullmatch(contact) or digits > _MAX_PHONE_DIGITS:
        raise ValidationError(MSG_PHONE)
    return contact


def validate_message_text(value: str, *, required: bool = False) -> str:
    text = (value or "").strip()
    if not text:
        if required:
            raise ValidationError(MSG_MESSAGE_MIN)
        return ""
    if len(text) < _MIN_MESSAGE:
        raise ValidationError(MSG_MESSAGE_MIN)
    return text
