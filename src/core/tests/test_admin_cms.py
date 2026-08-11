import pytest
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.urls import reverse

from src.core.models import SiteBlock, SiteSettings
from src.core.services import SITE_BLOCKS_CACHE_KEY, get_site_blocks, is_section_visible


@pytest.fixture
def admin_user(db):
    User = get_user_model()
    return User.objects.create_superuser("admin", "admin@example.com", "password123456")


@pytest.mark.django_db
def test_admin_section_get_post(client, admin_user):
    SiteSettings.get_solo()
    client.force_login(admin_user)
    url = reverse("admin:core_homeherosettings_change", args=[1])
    response = client.get(url)
    assert response.status_code == 200
    assert b"Hero" in response.content

    get_site_blocks()
    assert cache.get(SITE_BLOCKS_CACHE_KEY) is not None

    response = client.post(
        url,
        {
            "section_visible": "on",
            "block__home__hero.title__ru": "Новое имя",
            "block__home__hero.title__en": "New name",
            "block__home__hero.subtitle__ru": "ПОЛИНА",
            "block__home__hero.subtitle__en": "ПОЛИНА",
            "block__home__hero.lead__ru": "Lead RU",
            "block__home__hero.lead__en": "Lead EN",
            "block__home__hero.cta_primary__ru": "CTA",
            "block__home__hero.cta_primary__en": "CTA",
            "block__home__hero.cta_secondary__ru": "Sec",
            "block__home__hero.cta_secondary__en": "Sec",
            "block__home__hero.tagline__ru": "Tag",
            "block__home__hero.tagline__en": "Tag",
        },
    )
    assert response.status_code in (200, 302)
    block = SiteBlock.objects.get(page="home", key="hero.title")
    assert block.text_ru == "Новое имя"
    assert block.content_type == SiteBlock.ContentType.TEXT
    assert block.is_active is True
    assert cache.get(SITE_BLOCKS_CACHE_KEY) is None
    assert is_section_visible("home", "hero_section_visible") is True


@pytest.mark.django_db
def test_admin_gallery_fieldsets(client, admin_user):
    SiteSettings.get_solo()
    client.force_login(admin_user)
    url = reverse("admin:core_homegallerysettings_change", args=[1])
    response = client.get(url)
    assert response.status_code == 200
    html = response.content.decode()
    assert "Заголовок секции" in html
    assert "Фото галереи" in html
    assert "Видимость" in html
