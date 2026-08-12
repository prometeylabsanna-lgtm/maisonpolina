from django.core.exceptions import ValidationError

from src.core.form_validators import (
    MSG_MESSAGE_MIN,
    MSG_NAME_DIGITS,
    MSG_PHONE,
    validate_message_text,
    validate_person_name,
    validate_phone,
)


def test_name_rejects_digits():
    try:
        validate_person_name("Анна2")
    except ValidationError as exc:
        assert MSG_NAME_DIGITS in exc.messages
    else:
        raise AssertionError("expected ValidationError")


def test_name_allows_letters():
    assert validate_person_name("  Анна  ") == "Анна"


def test_phone_rejects_letters_and_extra_digits():
    try:
        validate_phone("abc123")
    except ValidationError as exc:
        assert MSG_PHONE in exc.messages
    else:
        raise AssertionError("expected ValidationError")

    try:
        validate_phone("123456789012345")
    except ValidationError as exc:
        assert MSG_PHONE in exc.messages
    else:
        raise AssertionError("expected ValidationError")

    try:
        validate_phone("+++")
    except ValidationError as exc:
        assert MSG_PHONE in exc.messages
    else:
        raise AssertionError("expected ValidationError")

    try:
        validate_phone("123")
    except ValidationError as exc:
        assert MSG_PHONE in exc.messages
    else:
        raise AssertionError("expected ValidationError")


def test_phone_allows_formatted_value():
    assert validate_phone("+38 (099) 123-45-67") == "+38 (099) 123-45-67"
    assert validate_phone("0991234567") == "0991234567"


def test_message_min_length():
    try:
        validate_message_text("а")
    except ValidationError as exc:
        assert MSG_MESSAGE_MIN in exc.messages
    else:
        raise AssertionError("expected ValidationError")

    assert validate_message_text("") == ""
    assert validate_message_text("ок") == "ок"

    try:
        validate_message_text("", required=True)
    except ValidationError as exc:
        assert MSG_MESSAGE_MIN in exc.messages
    else:
        raise AssertionError("expected ValidationError")
