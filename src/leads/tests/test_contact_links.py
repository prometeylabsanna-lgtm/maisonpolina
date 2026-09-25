from src.leads.contact_links import contact_actions
from src.leads.services import _contact_actions_line


def test_ukrainian_local_phone_uses_country_code():
    actions = contact_actions("0500209814")
    assert actions[0]["url"] == "tel:+380500209814"
    assert actions[1]["url"] == "https://wa.me/380500209814"


def test_phone_opens_call_and_whatsapp():
    actions = contact_actions("353263256")
    assert actions[0]["url"] == "tel:+353263256"
    assert actions[1]["url"] == "https://wa.me/353263256"


def test_nick_opens_telegram():
    actions = contact_actions("@polina_mail")
    assert actions == [{"label": "Telegram", "url": "https://t.me/polina_mail"}]


def test_email_opens_mail():
    actions = contact_actions("hello@example.com")
    assert actions[0]["url"] == "mailto:hello@example.com"


def test_telegram_line_contains_whatsapp():
    line = str(_contact_actions_line("+380671112233"))
    assert "https://wa.me/380671112233" in line
    assert "Написать:" in line
