"""Force Russian UI language for /admin/ (content stays bilingual via RU/EN tabs)."""

from __future__ import annotations

from django.utils import translation


class AdminRussianLocaleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/admin"):
            translation.activate("ru")
            request.LANGUAGE_CODE = "ru"
        response = self.get_response(request)
        return response
