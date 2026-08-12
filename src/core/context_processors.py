from pathlib import Path

from django.conf import settings
from django.urls import translate_url
from django.utils.translation import get_language

from src.core.models import SiteSettings
from src.core.section_styles import get_section_styles_css
from src.core.services import get_site_blocks


def _maybe_rebuild_css_bundles() -> None:
    """In DEBUG, rebuild site.css / home.css when modular sources are newer."""
    if not settings.DEBUG:
        return
    try:
        import importlib.util

        script = Path(settings.BASE_DIR) / "scripts" / "build_css.py"
        spec = importlib.util.spec_from_file_location("build_css", script)
        if spec is None or spec.loader is None:
            return
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception:
        return

    def needs(parts: list[str], out_name: str) -> bool:
        out = mod.CSS / out_name
        if not out.is_file():
            return True
        out_mtime = out.stat().st_mtime
        return any(
            (mod.CSS / rel).stat().st_mtime > out_mtime
            for rel in parts
            if (mod.CSS / rel).is_file()
        )

    try:
        if needs(mod.SITE_PARTS, "site.css"):
            mod._bundle(mod.SITE_PARTS, "site.css")
        if needs(mod.HOME_PARTS, "pages/home.css"):
            mod._bundle(mod.HOME_PARTS, "pages/home.css")
    except Exception:
        pass


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
    _maybe_rebuild_css_bundles()
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
