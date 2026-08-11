from pathlib import Path

from django.conf import settings
from django.urls import translate_url
from django.utils.translation import get_language

from src.core.models import SiteSettings
from src.core.section_styles import get_section_styles_css
from src.core.services import get_site_blocks


def site_context(request):
    try:
        site_settings = SiteSettings.get_solo()
        site_blocks = get_site_blocks()
        section_styles_css = get_section_styles_css()
    except Exception:
        site_settings = SiteSettings(pk=1)
        site_blocks = {}
        section_styles_css = ""
    return {
        "site_settings": site_settings,
        "site_blocks": site_blocks,
        "section_styles_css": section_styles_css,
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
