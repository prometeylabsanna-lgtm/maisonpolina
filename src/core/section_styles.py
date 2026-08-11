"""Build CMS override CSS from SectionStyle rows."""

from __future__ import annotations

from django.core.cache import cache
from django.utils.html import escape

from src.core.models import SectionStyle

SECTION_STYLES_CACHE_KEY = "section_styles_css_v1"
SECTION_STYLES_CACHE_TTL = 60

# CSS selector per section slug
SECTION_SELECTORS: dict[str, str] = {
    "header": ".header",
    "hero": '[data-section="hero"]',
    "about": '[data-section="about"]',
    "personality": '[data-section="personality"]',
    "gallery": '[data-section="gallery"]',
    "formats": '[data-section="formats"]',
    "testimonials": '[data-section="testimonials"]',
    "faq": '[data-section="faq"]',
    "contacts": '[data-section="contacts"]',
    "footer": ".footer",
}


def invalidate_section_styles_cache() -> None:
    cache.delete(SECTION_STYLES_CACHE_KEY)


def _decl(prop: str, value: str) -> str:
    return f"{prop}:{escape(value)};"


def build_section_styles_css(styles: list[SectionStyle] | None = None) -> str:
    rows = styles if styles is not None else list(SectionStyle.objects.all())
    chunks: list[str] = []
    for style in rows:
        selector = SECTION_SELECTORS.get(style.section)
        if not selector:
            continue
        decls: list[str] = []
        bg = style.bg_css()
        if bg:
            decls.append(_decl("--cms-section-bg", bg))
            decls.append(_decl("background", "var(--cms-section-bg)"))
        primary = style.btn_primary_css()
        if primary:
            decls.append(_decl("--cms-btn-primary", primary))
            decls.append(_decl("--cms-btn-primary-hover", primary))
        secondary = style.btn_secondary_css()
        if secondary:
            decls.append(_decl("--cms-btn-secondary", secondary))
        header_btn = style.btn_header_css()
        if header_btn and style.section == SectionStyle.Section.HEADER:
            decls.append(_decl("--cms-btn-header", header_btn))
            decls.append(_decl("--cms-btn-header-hover", header_btn))
        if not decls:
            continue
        chunks.append(f"{selector}{{{''.join(decls)}}}")
        if primary:
            chunks.append(
                f"{selector} .btn,"
                f"{selector} .btn--solid,"
                f"{selector} .btn--gradient,"
                f"{selector} .btn--compact{{"
                f"background:var(--cms-btn-primary);"
                f"}}"
            )
            chunks.append(
                f"{selector} .btn:hover,"
                f"{selector} .btn--solid:hover,"
                f"{selector} .btn--gradient:hover,"
                f"{selector} .btn--compact:hover{{"
                f"background:var(--cms-btn-primary-hover);"
                f"}}"
            )
        if secondary:
            chunks.append(
                f"{selector} .btn--ghost,"
                f"{selector} .hero__strip-link{{"
                f"background:transparent;"
                f"border-color:var(--cms-btn-secondary);"
                f"color:var(--cms-btn-secondary);"
                f"}}"
            )
        if header_btn and style.section == SectionStyle.Section.HEADER:
            chunks.append(
                ".header .btn,"
                ".mobile-nav .btn{"
                "background:var(--cms-btn-header);"
                "}"
            )
            chunks.append(
                ".header .btn:hover,"
                ".mobile-nav .btn:hover{"
                "background:var(--cms-btn-header-hover);"
                "}"
            )
    return "".join(chunks)


def get_section_styles_css() -> str:
    css = cache.get(SECTION_STYLES_CACHE_KEY)
    if css is None:
        css = build_section_styles_css()
        cache.set(SECTION_STYLES_CACHE_KEY, css, SECTION_STYLES_CACHE_TTL)
    return css
