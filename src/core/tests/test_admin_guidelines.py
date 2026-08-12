import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from src.core.admin_guidelines import (
    field_guideline_key,
    guideline_help,
    image_help,
    text_help,
)
from src.core.models import SiteSettings
from src.formats.models import ServiceFormat


@pytest.fixture
def admin_user(db):
    User = get_user_model()
    return User.objects.create_superuser("admin", "admin@example.com", "password123456")


def test_image_help_hero():
    hint = image_help("hero.media")
    assert "1200×1600" in hint
    assert "1920×1080" in hint
    assert "450 КБ" in hint


def test_text_help_nav_nowrap():
    hint = text_help("nav.about")
    assert "14" in hint
    assert "меню" in hint


def test_text_help_privacy_unlimited():
    hint = text_help("privacy.body")
    assert "лимита" in hint
    assert "Удобно до" not in hint


def test_guideline_help_prefers_image():
    assert "px" in guideline_help("about.portrait")
    assert "символов" in guideline_help("hero.title")


def test_field_guideline_key_strips_lang():
    assert field_guideline_key("title_ru", prefix="formats") == "formats.title"
    assert field_guideline_key("photo", prefix="reviews") == "reviews.photo"
    assert (
        field_guideline_key("text_ru", mapping={"text_ru": "formats.feature"})
        == "formats.feature"
    )


def test_unknown_key_empty():
    assert guideline_help("missing.key") == ""


@pytest.mark.django_db
def test_admin_hero_shows_layout_hints(client, admin_user):
    SiteSettings.get_solo()
    client.force_login(admin_user)
    response = client.get(reverse("admin:core_homeherosettings_change", args=[1]))
    html = response.content.decode()
    assert response.status_code == 200
    assert "Удобно до 24 символов" in html
    assert "1200×1600" in html
    assert "Половина — вертикальный портрет" in html


@pytest.mark.django_db
def test_admin_gallery_shows_image_hint(client, admin_user):
    SiteSettings.get_solo()
    client.force_login(admin_user)
    response = client.get(reverse("admin:core_homegallerysettings_change", args=[1]))
    html = response.content.decode()
    assert response.status_code == 200
    assert "1200×1600" in html
    assert "3:4" in html


@pytest.mark.django_db
def test_admin_format_change_shows_image_hint(client, admin_user):
    obj = ServiceFormat.objects.create(title_ru="Ужин", title_en="Dinner", order=1)
    client.force_login(admin_user)
    response = client.get(reverse("admin:formats_serviceformat_change", args=[obj.pk]))
    html = response.content.decode()
    assert response.status_code == 200
    assert "1200×900" in html
    assert "4:3" in html
    assert "Удобно до 36 символов" in html
    assert "Title ru" not in html
    assert ">Название<" in html or "Название" in html
    assert "Метка" in html
    assert "Описание" in html
    assert "Цена" in html
