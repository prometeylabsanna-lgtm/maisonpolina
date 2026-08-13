from pathlib import Path

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse

from src.core.models import SiteSettings


@pytest.fixture
def admin_user(db):
    User = get_user_model()
    return User.objects.create_superuser("admin", "admin@example.com", "password123456")


def test_admin_brand_sub_contrasts_on_light_theme():
    css = (Path(settings.BASE_DIR) / "static/css/admin/brand.css").read_text()
    sub_block = css.split(".admin-brand__sub {", 1)[1].split("}", 1)[0]
    assert "var(--admin-burgundy)" in sub_block
    assert "var(--admin-gold-soft)" not in sub_block


def test_admin_lang_toggles_have_no_shared_block():
    brand = (Path(settings.BASE_DIR) / "static/css/admin/brand.css").read_text()
    cms = (Path(settings.BASE_DIR) / "static/css/admin/site_content.css").read_text()
    wrap = brand.split(".admin-fieldset-tabs-wrap {", 1)[1].split("}", 1)[0]
    fieldset = brand.split(".admin-fieldset-tabs {", 1)[1].split("}", 1)[0]
    tabs = cms.split(".cms-lang-tabs {", 1)[1].split("}", 1)[0]
    assert "background: transparent" in wrap
    assert "border: 0" in wrap
    assert "background: #fffaf7" not in wrap
    assert "background: transparent" in fieldset
    assert "border: 0" in fieldset
    assert "background: #fff" not in fieldset
    assert "background: transparent" in tabs
    assert "border: 0" in tabs
    assert "background: #1a1214" not in cms.split(".dark .cms-lang-tabs {", 1)[1].split("}", 1)[0]
    assert "rgb(76 13 19 / 0.22)" not in brand.split(".dark .admin-fieldset-tabs-wrap {", 1)[1].split("}", 1)[0]


def test_unfold_theme_is_unlocked():
    assert not settings.UNFOLD.get("THEME")


def test_unfold_primary_is_burgundy():
    primary = settings.UNFOLD["COLORS"]["primary"]
    assert primary["600"] == "#4c0d13"
    assert primary["500"] == "#8a2433"


def test_tinymce_extra_media_includes_theme_sync():
    extra = settings.TINYMCE_EXTRA_MEDIA
    assert "js/admin/tinymce-theme.js" in extra["js"]
    assert "css/admin/tinymce-theme.css" in extra["css"]["all"]


@pytest.mark.django_db
def test_admin_theme_switcher_visible(client, admin_user):
    client.force_login(admin_user)
    html = client.get(reverse("admin:index")).content.decode()
    assert "switchTheme('light')" in html
    assert "switchTheme('dark')" in html
    assert "Светлая" in html
    assert "Темная" in html
    assert "favicon-32x32.png" in html
    assert "apple-touch-icon.png" in html
    assert "brand-monogram.png" in html
    assert "admin-brand__mark" in html
    assert "admin-brand__sub" in html
    assert "Панель сайта" in html
    assert "MaisonPolina" in html


@pytest.mark.django_db
def test_admin_empty_results_are_russian(client, admin_user):
    client.force_login(admin_user)
    url = reverse("admin:reviews_testimonial_changelist")
    html = client.get(f"{url}?q=zzzz-no-such-review", follow=True).content.decode()
    assert "Ничего не найдено" in html
    assert "На этой странице нет записей" in html
    assert "No results found" not in html
    assert "This page yielded into no results" not in html


@pytest.mark.django_db
def test_admin_logo_preview_shows_site_fallback(client, admin_user):
    SiteSettings.get_solo()
    client.force_login(admin_user)
    html = client.get(reverse("admin:core_sitesettings_change", args=[1])).content.decode()
    assert "brand-monogram-header" in html
    assert "get_logo_preview" in html or "Превью логотипа" in html
