from pathlib import Path

from django.conf import settings
from django.urls import translate_url
from django.utils.translation import get_language

from src.core.models import SiteSettings
from src.core.services import get_site_blocks


def site_context(request):
    return {
        "site_settings": SiteSettings.get_solo(),
        "site_blocks": get_site_blocks(),
        "current_language": get_language() or "ru",
    }


def static_version(request):
    static_root = Path(settings.BASE_DIR) / "static"
    mtimes = [
        int(p.stat().st_mtime)
        for pattern in ("css/**/*.css", "js/**/*.js")
        for p in static_root.glob(pattern)
    ]
    return {"static_version": max(mtimes) if mtimes else 0}


def alternate_urls(request):
    path = request.get_full_path()
    urls = {}
    for code, _name in settings.LANGUAGES:
        try:
            urls[code] = translate_url(path, code)
        except Exception:
            urls[code] = f"/{code}/"
    return {"alternate_urls": urls}
