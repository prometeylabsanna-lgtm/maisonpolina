"""Tests for SectionStyle CSS generation and admin screen."""

import pytest
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.urls import reverse

from src.core.fill_style import FillType, resolve_fill
from src.core.models import SectionStyle, SiteSettings
from src.core.section_styles import (
    SECTION_STYLES_CACHE_KEY,
    build_section_styles_css,
    get_section_styles_css,
)
from src.core.style_defaults import ensure_section_styles


@pytest.fixture
def admin_user(db):
    User = get_user_model()
    return User.objects.create_superuser("admin", "admin@example.com", "password123456")


@pytest.mark.django_db
def test_resolve_fill_solid_and_gradient():
    assert resolve_fill(
        fill_type=FillType.SOLID,
        solid_color="#4c0d13",
        gradient_start="",
        gradient_end="",
        gradient_angle=180,
    ) == "#4c0d13"
    assert resolve_fill(
        fill_type=FillType.GRADIENT,
        solid_color="",
        gradient_start="#dfccb7",
        gradient_end="#b09572",
        gradient_angle=90,
    ) == "linear-gradient(90deg, #dfccb7, #b09572)"
    assert (
        resolve_fill(
            fill_type="",
            solid_color="",
            gradient_start="",
            gradient_end="",
            gradient_angle=180,
        )
        is None
    )
    assert (
        resolve_fill(
            fill_type="",
            solid_color="#111111",
            gradient_start="#222222",
            gradient_end="#333333",
            gradient_angle=90,
        )
        is None
    )


@pytest.mark.django_db
def test_section_styles_css_empty_keeps_tokens():
    ensure_section_styles()
    assert build_section_styles_css() == ""


@pytest.mark.django_db
def test_section_styles_css_with_primary():
    ensure_section_styles()
    style = SectionStyle.objects.get(section=SectionStyle.Section.HERO)
    style.btn_primary_fill_type = FillType.SOLID
    style.btn_primary_solid_color = "#cab695"
    style.save()
    css = build_section_styles_css()
    assert '[data-section="hero"]' in css
    assert "--cms-btn-primary:#cab695" in css


@pytest.mark.django_db
def test_styles_admin_get_post(client, admin_user):
    SiteSettings.get_solo()
    ensure_section_styles()
    client.force_login(admin_user)
    url = reverse("admin:core_themestylessettings_change", args=[1])
    response = client.get(url)
    assert response.status_code == 200
    html = response.content.decode()
    assert "Дефолт" in html
    assert "cms-color-picker" in html
    assert "cms-style-panel" in html

    get_section_styles_css()
    assert cache.get(SECTION_STYLES_CACHE_KEY) is not None

    post = {}
    for section in (
        "header",
        "hero",
        "about",
        "personality",
        "gallery",
        "formats",
        "testimonials",
        "faq",
        "contacts",
        "footer",
    ):
        prefix = f"style_{section}"
        post[f"{prefix}-label"] = section
        post[f"{prefix}-bg_fill_type"] = ""
        post[f"{prefix}-bg_solid_color"] = ""
        post[f"{prefix}-bg_gradient_start"] = ""
        post[f"{prefix}-bg_gradient_end"] = ""
        post[f"{prefix}-bg_gradient_angle"] = "180"
        if section == "header":
            post[f"{prefix}-btn_header_fill_type"] = FillType.SOLID
            post[f"{prefix}-btn_header_solid_color"] = "#cab695"
            post[f"{prefix}-btn_header_gradient_start"] = ""
            post[f"{prefix}-btn_header_gradient_end"] = ""
            post[f"{prefix}-btn_header_gradient_angle"] = "180"
        else:
            post[f"{prefix}-btn_primary_fill_type"] = ""
            post[f"{prefix}-btn_primary_solid_color"] = ""
            post[f"{prefix}-btn_primary_gradient_start"] = ""
            post[f"{prefix}-btn_primary_gradient_end"] = ""
            post[f"{prefix}-btn_primary_gradient_angle"] = "180"
            post[f"{prefix}-btn_secondary_fill_type"] = ""
            post[f"{prefix}-btn_secondary_solid_color"] = ""
            post[f"{prefix}-btn_secondary_gradient_start"] = ""
            post[f"{prefix}-btn_secondary_gradient_end"] = ""
            post[f"{prefix}-btn_secondary_gradient_angle"] = "180"

    response = client.post(url, post)
    assert response.status_code in (200, 302)
    header = SectionStyle.objects.get(section=SectionStyle.Section.HEADER)
    assert header.btn_header_solid_color == "#cab695"
    assert cache.get(SECTION_STYLES_CACHE_KEY) is None


@pytest.mark.django_db
def test_styles_admin_reset_section_to_brand_preset(client, admin_user):
    SiteSettings.get_solo()
    ensure_section_styles()
    hero = SectionStyle.objects.get(section=SectionStyle.Section.HERO)
    hero.bg_fill_type = FillType.GRADIENT
    hero.bg_solid_color = "#111111"
    hero.btn_primary_solid_color = "#222222"
    hero.save()

    client.force_login(admin_user)
    url = reverse("admin:core_themestylessettings_change", args=[1])
    response = client.post(url, {"reset_section": "hero"})
    assert response.status_code in (200, 302)

    hero.refresh_from_db()
    assert hero.bg_fill_type == FillType.SOLID
    assert hero.bg_solid_color == "#4c0d13"
    assert hero.btn_primary_solid_color == "#cab695"
    assert cache.get(SECTION_STYLES_CACHE_KEY) is None


@pytest.mark.django_db
def test_site_mode_clears_custom_colors_on_save(client, admin_user):
    SiteSettings.get_solo()
    ensure_section_styles()
    hero = SectionStyle.objects.get(section=SectionStyle.Section.HERO)
    hero.bg_fill_type = FillType.SOLID
    hero.bg_solid_color = "#111111"
    hero.btn_primary_fill_type = FillType.SOLID
    hero.btn_primary_solid_color = "#222222"
    hero.save()

    client.force_login(admin_user)
    url = reverse("admin:core_homeherosettings_change", args=[1])
    response = client.post(
        url,
        {
            "section_visible": "on",
            "block__home__hero.title__ru": "Имя",
            "block__home__hero.title__en": "Name",
            "block__home__hero.subtitle__ru": "",
            "block__home__hero.subtitle__en": "",
            "block__home__hero.lead__ru": "Lead",
            "block__home__hero.lead__en": "Lead",
            "block__home__hero.cta_primary__ru": "CTA",
            "block__home__hero.cta_primary__en": "CTA",
            "block__home__hero.cta_secondary__ru": "Sec",
            "block__home__hero.cta_secondary__en": "Sec",
            "block__home__hero.tagline__ru": "Tag",
            "block__home__hero.tagline__en": "Tag",
            "block__home__hero.media_layout__choice": "full",
            "style-label": "Баннер",
            "style-bg_fill_type": "",
            "style-bg_solid_color": "#111111",
            "style-bg_gradient_start": "#4c0d13",
            "style-bg_gradient_end": "#3a0a0f",
            "style-bg_gradient_angle": "180",
            "style-btn_primary_fill_type": "",
            "style-btn_primary_solid_color": "#222222",
            "style-btn_primary_gradient_start": "#dfccb7",
            "style-btn_primary_gradient_end": "#b09572",
            "style-btn_primary_gradient_angle": "180",
            "style-btn_secondary_fill_type": "",
            "style-btn_secondary_solid_color": "",
            "style-btn_secondary_gradient_start": "",
            "style-btn_secondary_gradient_end": "",
            "style-btn_secondary_gradient_angle": "180",
        },
    )
    assert response.status_code in (200, 302)
    hero.refresh_from_db()
    assert hero.bg_fill_type == ""
    assert hero.bg_solid_color == ""
    assert hero.btn_primary_fill_type == ""
    assert hero.btn_primary_solid_color == ""
    assert hero.bg_css() is None
    assert hero.btn_primary_css() is None


@pytest.mark.django_db
def test_privacy_body_uses_tinymce(client, admin_user):
    SiteSettings.get_solo()
    client.force_login(admin_user)
    url = reverse("admin:core_privacysettings_change", args=[1])
    response = client.get(url)
    assert response.status_code == 200
    html = response.content.decode()
    assert 'name="block__privacy__body__ru"' in html
    assert "tinymce" in html.lower()
    assert 'class="cms-admin-input tinymce"' in html or "TinyMCE" in html
    assert "Цвета блока" not in html


@pytest.mark.django_db
def test_cms_block_has_compact_style_panel(client, admin_user):
    SiteSettings.get_solo()
    ensure_section_styles()
    client.force_login(admin_user)
    url = reverse("admin:core_homeherosettings_change", args=[1])
    html = client.get(url).content.decode()
    assert "Цвета блока" in html
    assert "cms-color-picker" in html
    assert 'name="style-bg_fill_type"' in html
    assert 'name="style-btn_primary_solid_color"' in html
    assert "Градиент" in html

    response = client.post(
        url,
        {
            "section_visible": "on",
            "block__home__hero.title__ru": "Имя",
            "block__home__hero.title__en": "Name",
            "block__home__hero.subtitle__ru": "",
            "block__home__hero.subtitle__en": "",
            "block__home__hero.lead__ru": "Lead",
            "block__home__hero.lead__en": "Lead",
            "block__home__hero.cta_primary__ru": "CTA",
            "block__home__hero.cta_primary__en": "CTA",
            "block__home__hero.cta_secondary__ru": "Sec",
            "block__home__hero.cta_secondary__en": "Sec",
            "block__home__hero.tagline__ru": "Tag",
            "block__home__hero.tagline__en": "Tag",
            "block__home__hero.media_layout__choice": "full",
            "style-label": "Баннер",
            "style-bg_fill_type": FillType.SOLID,
            "style-bg_solid_color": "#1a0508",
            "style-bg_gradient_start": "#4c0d13",
            "style-bg_gradient_end": "#3a0a0f",
            "style-bg_gradient_angle": "180",
            "style-btn_primary_fill_type": FillType.GRADIENT,
            "style-btn_primary_solid_color": "#cab695",
            "style-btn_primary_gradient_start": "#dfccb7",
            "style-btn_primary_gradient_end": "#b09572",
            "style-btn_primary_gradient_angle": "90",
            "style-btn_secondary_fill_type": FillType.SOLID,
            "style-btn_secondary_solid_color": "#cab695",
            "style-btn_secondary_gradient_start": "",
            "style-btn_secondary_gradient_end": "",
            "style-btn_secondary_gradient_angle": "180",
        },
    )
    assert response.status_code in (200, 302)
    hero = SectionStyle.objects.get(section=SectionStyle.Section.HERO)
    assert hero.bg_fill_type == FillType.SOLID
    assert hero.bg_solid_color == "#1a0508"
    assert hero.btn_primary_fill_type == FillType.GRADIENT


@pytest.mark.django_db
def test_footer_style_panel_has_solid_and_gradient(client, admin_user):
    SiteSettings.get_solo()
    ensure_section_styles()
    client.force_login(admin_user)
    html = client.get(
        reverse("admin:core_sitefootersettings_change", args=[1])
    ).content.decode()
    assert "Цвета блока" in html
    assert "Фон" in html
    assert "Цвет" in html
    assert "Градиент" in html
    assert 'name="style-bg_solid_color"' in html
    assert 'name="style-bg_gradient_start"' in html
    assert 'name="style-btn_primary_solid_color"' in html
