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
