from unittest.mock import MagicMock, patch

import pytest
import requests

from src.chat.services.telegram_bot import (
    TelegramNetworkError,
    TelegramRateLimitError,
    call_telegram_api,
)


def test_call_telegram_api_timeout(settings):
    settings.TELEGRAM_BOT_TOKEN = "token"
    with patch("src.chat.services.telegram_bot.requests.post", side_effect=requests.Timeout):
        with pytest.raises(TelegramNetworkError):
            call_telegram_api("getMe")


def test_call_telegram_api_rate_limit(settings):
    settings.TELEGRAM_BOT_TOKEN = "token"
    mock_resp = MagicMock()
    mock_resp.status_code = 429
    mock_resp.headers = {"Retry-After": "3"}
    mock_resp.json.return_value = {"ok": False, "parameters": {"retry_after": 3}}
    with patch("src.chat.services.telegram_bot.requests.post", return_value=mock_resp):
        with pytest.raises(TelegramRateLimitError) as exc:
            call_telegram_api("sendMessage", {"chat_id": 1, "text": "x"})
    assert exc.value.retry_after == 3


def test_call_telegram_api_invalid_json(settings):
    settings.TELEGRAM_BOT_TOKEN = "token"
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.side_effect = ValueError("bad json")
    with patch("src.chat.services.telegram_bot.requests.post", return_value=mock_resp):
        from src.chat.services.telegram_bot import TelegramBotError

        with pytest.raises(TelegramBotError):
            call_telegram_api("getMe")
