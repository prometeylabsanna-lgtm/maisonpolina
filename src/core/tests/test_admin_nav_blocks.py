import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from src.core.admin_nav import build_admin_navigation
from src.core.models import SiteSettings
from src.core.site_content_registry import CONTENT_SECTIONS, get_section
from src.faq.models import FaqItem
from src.formats.models import FormatFeature, ServiceFormat
from src.reviews.models import Testimonial


@pytest.fixture
def admin_user(db):
    User = get_user_model()
    return User.objects.create_superuser("admin", "admin@example.com", "password123456")


def _nav_titles():
    return [
        item["title"]
        for group in build_admin_navigation()
        for item in group["items"]
    ]


def test_sidebar_follows_page_blocks():
    titles = _nav_titles()
    assert titles.index("Шапка профиля") < titles.index("Баннер")
    assert "Восемь лет ярких впечатлений" in titles
    assert "Дополнительная информация" in titles
    assert "Галерея" in titles
    assert "Услуги" in titles
    assert "Отзывы" in titles
    assert "Вопросы" in titles
    assert "Заявка" in titles
    assert "Подвал" in titles
    assert "Политика конфиденциальности" in titles
    assert "Интерфейс" not in titles
    assert "Форматы услуг" not in titles
    assert "Hero" not in titles
    about_group = next(
        group for group in build_admin_navigation() if group.get("title") == "Обо мне"
    )
    assert about_group.get("title") == "Обо мне"
    child_titles = [item["title"] for item in about_group["items"]]
    assert child_titles == [
        "Восемь лет ярких впечатлений",
        "Дополнительная информация",
    ]


def test_contacts_fields_live_on_zayavka_section():
    section = get_section("home", "contacts")
    keys = {key for _page, key in section.blocks}
    assert "contacts.bg" in keys
    assert "form.name" in keys
    assert "form.submit" in keys
    assert "contacts.telegram_title" in keys
    assert section.settings_fields == ("phone", "email", "telegram_url")
    assert "ui" not in {item.slug for item in CONTENT_SECTIONS}


@pytest.mark.django_db
def test_admin_zayavka_shows_form_and_bg(client, admin_user):
    SiteSettings.get_solo()
    client.force_login(admin_user)
    url = reverse("admin:core_homecontactssettings_change", args=[1])
    html = client.get(url).content.decode()
    assert "Заявка" in html
    assert 'name="block__site__contacts.bg__image"' in html
    assert 'name="block__site__form.name__ru"' in html
    assert 'name="settings__phone"' in html


@pytest.mark.django_db
def test_admin_header_shows_logo_settings(client, admin_user):
    SiteSettings.get_solo()
    client.force_login(admin_user)
    url = reverse("admin:core_siteheadersettings_change", args=[1])
    html = client.get(url).content.decode()
    assert "Шапка профиля" in html
    assert 'name="settings__logo"' in html
    assert 'name="settings__phone"' in html


@pytest.mark.django_db
def test_admin_formats_toggles_and_features(client, admin_user):
    SiteSettings.get_solo()
    fmt = ServiceFormat.objects.create(
        title_ru="Ужин",
        title_en="Dinner",
        order=1,
        is_active=True,
    )
    FormatFeature.objects.create(service=fmt, text_ru="Встреча", text_en="Meet", order=0)
    client.force_login(admin_user)
    url = reverse("admin:core_homeformatssettings_change", args=[1])
    get_html = client.get(url).content.decode()
    assert "Карточки услуг" in get_html
    assert 'name="formats-TOTAL_FORMS"' in get_html
    assert "Добавить формат" in get_html

    response = client.post(
        url,
        {
            "section_visible": "on",
            "block__home__formats.eyebrow__ru": "Форматы",
            "block__home__formats.eyebrow__en": "Formats",
            "block__home__formats.title__ru": "Услуги",
            "block__home__formats.title__en": "Services",
            "block__home__formats.title_accent__ru": "",
            "block__home__formats.title_accent__en": "",
            "block__home__formats.note__ru": "",
            "block__home__formats.note__en": "",
            "block__site__formats.featured_badge__ru": "Выбор",
            "block__site__formats.featured_badge__en": "Pick",
            "block__site__formats.includes__ru": "Входит",
            "block__site__formats.includes__en": "Includes",
            "block__site__formats.order_cta__ru": "Заказать",
            "block__site__formats.order_cta__en": "Book",
            "formats-TOTAL_FORMS": "1",
            "formats-INITIAL_FORMS": "1",
            "formats-MIN_NUM_FORMS": "0",
            "formats-MAX_NUM_FORMS": "1000",
            "formats-0-id": str(fmt.pk),
            "formats-0-title_ru": "Ужин",
            "formats-0-title_en": "Dinner",
            "formats-0-label_ru": "I",
            "formats-0-label_en": "I",
            "formats-0-description_ru": "Вечер",
            "formats-0-description_en": "Evening",
            "formats-0-price_text_ru": "по запросу",
            "formats-0-price_text_en": "on request",
            "formats-0-features_ru": "Встреча\nУжин",
            "formats-0-features_en": "Meet\nDinner",
            "formats-0-order": "1",
            "formats-0-is_active": "on",
        },
    )
    assert response.status_code in (200, 302)
    fmt.refresh_from_db()
    assert fmt.is_active is True
    texts = list(fmt.features.order_by("order").values_list("text_ru", flat=True))
    assert texts == ["Встреча", "Ужин"]


@pytest.mark.django_db
def test_admin_faq_and_reviews_lists_on_section_pages(client, admin_user):
    SiteSettings.get_solo()
    FaqItem.objects.create(
        question_ru="Как?",
        question_en="How?",
        answer_ru="Так",
        answer_en="So",
        order=1,
        is_active=True,
    )
    Testimonial.objects.create(
        author_name_ru="Анна",
        author_name_en="Anna",
        text_ru="Хорошо",
        text_en="Good",
        order=1,
        is_active=True,
    )
    client.force_login(admin_user)
    faq_html = client.get(
        reverse("admin:core_homefaqsettings_change", args=[1])
    ).content.decode()
    assert 'name="faq-TOTAL_FORMS"' in faq_html
    assert "Добавить вопрос" in faq_html
    reviews_html = client.get(
        reverse("admin:core_hometestimonialssettings_change", args=[1])
    ).content.decode()
    assert 'name="testimonials-TOTAL_FORMS"' in reviews_html
    assert "Добавить отзыв" in reviews_html
