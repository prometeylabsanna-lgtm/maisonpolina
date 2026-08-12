"""Locale helpers: admin UI in Russian, remember public language in a cookie."""

from __future__ import annotations

from django.conf import settings
from django.utils import translation


def _is_admin_path(path: str) -> bool:
    prefix = "/" + settings.ADMIN_URL.strip("/")
    return path == prefix or path.startswith(prefix + "/")


class AdminRussianLocaleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if _is_admin_path(request.path):
            translation.activate("ru")
            request.LANGUAGE_CODE = "ru"
        response = self.get_response(request)
        return response


class LanguageCookieMiddleware:
    """Persist the URL language so the next visit opens the same version."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if _is_admin_path(request.path):
            return response
        lang = (getattr(request, "LANGUAGE_CODE", None) or translation.get_language() or "")[:2]
        allowed = {code for code, _name in settings.LANGUAGES}
        if lang not in allowed:
            return response
        cookie_name = settings.LANGUAGE_COOKIE_NAME
        if request.COOKIES.get(cookie_name) == lang:
            return response
        response.set_cookie(
            cookie_name,
            lang,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=getattr(settings, "LANGUAGE_COOKIE_PATH", "/"),
            domain=getattr(settings, "LANGUAGE_COOKIE_DOMAIN", None),
            secure=getattr(settings, "LANGUAGE_COOKIE_SECURE", False),
            httponly=getattr(settings, "LANGUAGE_COOKIE_HTTPONLY", False),
            samesite=getattr(settings, "LANGUAGE_COOKIE_SAMESITE", "Lax"),
        )
        return response
