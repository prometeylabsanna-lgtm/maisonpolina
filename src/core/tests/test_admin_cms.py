import pytest
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from src.core.fields import _IMAGE_TYPE_ERROR
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
    assert "Баннер" in response.content.decode()

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
            "block__home__hero.media_layout__choice": "full",
            "block__home__hero.media__video_url": "",
        },
    )
    assert response.status_code in (200, 302)
    block = SiteBlock.objects.get(page="home", key="hero.title")
    assert block.text_ru == "Новое имя"
    assert block.content_type == SiteBlock.ContentType.TEXT
    assert block.is_active is True
    assert cache.get(SITE_BLOCKS_CACHE_KEY) is None
    assert is_section_visible("home", "hero_section_visible") is True
    layout = SiteBlock.objects.get(page="home", key="hero.media_layout")
    assert layout.text_ru == "full"


@pytest.mark.django_db
def test_admin_hero_media_fields(client, admin_user):
    SiteSettings.get_solo()
    client.force_login(admin_user)
    url = reverse("admin:core_homeherosettings_change", args=[1])
    response = client.get(url)
    assert response.status_code == 200
    html = response.content.decode()
    assert 'name="block__home__hero.media_layout__choice"' in html
    assert 'name="block__home__hero.media__video_file"' in html
    assert 'name="block__home__hero.media__video_url"' in html
    assert "Половина секции" in html
    assert "На весь фон" in html


@pytest.mark.django_db
def test_admin_section_inputs_visible(client, admin_user):
    SiteSettings.get_solo()
    client.force_login(admin_user)
    url = reverse("admin:core_homegallerysettings_change", args=[1])
    response = client.get(url)
    assert response.status_code == 200
    html = response.content.decode()
    assert 'name="block__home__gallery.title__ru"' in html
    assert 'name="block__home__gallery.title__en"' in html
    assert "cms-lang-pane--ru" in html
    assert 'x-show="$store.cmsLang' not in html
    assert "Заголовок секции" in html
    assert "Фото галереи" in html
    assert "Видимость" in html
    assert "Добавить фото" in html
    assert "MaisonPolina" in html


@pytest.mark.django_db
def test_admin_image_preview_shown(client, admin_user):
    from django.core.files.uploadedfile import SimpleUploadedFile

    SiteSettings.get_solo()
    SiteBlock.objects.update_or_create(
        page="home",
        key="about.portrait",
        defaults={
            "content_type": SiteBlock.ContentType.IMAGE,
            "label": "portrait",
            "is_active": True,
        },
    )
    block = SiteBlock.objects.get(page="home", key="about.portrait")
    block.image.save(
        "test-portrait.jpg",
        SimpleUploadedFile(
            "test-portrait.jpg",
            b"\xff\xd8\xff\xd9",
            content_type="image/jpeg",
        ),
        save=True,
    )

    client.force_login(admin_user)
    url = reverse("admin:core_homeaboutsettings_change", args=[1])
    response = client.get(url)
    assert response.status_code == 200
    html = response.content.decode()
    assert "cms-image-preview" in html
    assert "test-portrait" in html


@pytest.mark.django_db
def test_admin_image_static_fallback_preview(client, admin_user):
    SiteSettings.get_solo()
    SiteBlock.objects.update_or_create(
        page="home",
        key="about.portrait",
        defaults={
            "content_type": SiteBlock.ContentType.IMAGE,
            "label": "portrait",
            "is_active": True,
            "image": "",
        },
    )
    client.force_login(admin_user)
    url = reverse("admin:core_homeaboutsettings_change", args=[1])
    response = client.get(url)
    html = response.content.decode()
    assert "cms-image-preview" in html
    assert "about-portrait" in html
    assert ".heic" in html
    assert "HEIC" in html


@pytest.mark.django_db
def test_admin_invalid_portrait_shows_field_error(client, admin_user):
    SiteSettings.get_solo()
    client.force_login(admin_user)
    url = reverse("admin:core_homeaboutsettings_change", args=[1])
    response = client.post(
        url,
        {
            "section_visible": "on",
            "block__home__about.portrait__image": SimpleUploadedFile(
                "photo.jpg",
                b"not-an-image",
                content_type="image/jpeg",
            ),
        },
    )
    assert response.status_code == 200
    html = response.content.decode()
    assert "cms-form-errors" in html
    assert "cms-field-error" in html
    assert _IMAGE_TYPE_ERROR in html
    assert "is-invalid" in html


@pytest.mark.django_db
def test_admin_styles_russian_labels(client, admin_user):
    SiteSettings.get_solo()
    client.force_login(admin_user)
    url = reverse("admin:core_themestylessettings_change", args=[1])
    response = client.get(url)
    assert response.status_code == 200
    html = response.content.decode()
    assert "Цвета и кнопки на сайте" in html
    assert "Кнопка" in html
    assert "Вторая кнопка" in html
    assert "Угол" in html
    assert "Градиент" in html
    assert "Primary" not in html
    assert "Secondary" not in html
    assert "tokens.css" not in html


def _tiny_jpeg(name="photo.jpg"):
    from io import BytesIO

    from django.core.files.uploadedfile import SimpleUploadedFile
    from PIL import Image

    buf = BytesIO()
    Image.new("RGB", (8, 8), (20, 4, 8)).save(buf, format="JPEG")
    buf.seek(0)
    return SimpleUploadedFile(name, buf.read(), content_type="image/jpeg")


@pytest.mark.django_db
def test_admin_gallery_adds_photo_to_existing(client, admin_user):
    from src.gallery.models import GalleryPhoto

    SiteSettings.get_solo()
    existing = GalleryPhoto.objects.create(
        alt_ru="Кадр",
        alt_en="Frame",
        caption_ru="Кадр",
        caption_en="Frame",
        static_image="images/gallery/gallery-01.webp",
        order=1,
        is_active=True,
    )
    client.force_login(admin_user)
    url = reverse("admin:core_homegallerysettings_change", args=[1])
    response = client.post(
        url,
        {
            "section_visible": "on",
            "block__home__gallery.eyebrow__ru": "Галерея",
            "block__home__gallery.eyebrow__en": "Gallery",
            "block__home__gallery.title__ru": "Кадры",
            "block__home__gallery.title__en": "Frames",
            "block__home__gallery.title_accent__ru": "",
            "block__home__gallery.title_accent__en": "",
            "gallery-TOTAL_FORMS": "2",
            "gallery-INITIAL_FORMS": "1",
            "gallery-MIN_NUM_FORMS": "0",
            "gallery-MAX_NUM_FORMS": "1000",
            "gallery-0-id": str(existing.pk),
            "gallery-0-alt_ru": existing.alt_ru,
            "gallery-0-alt_en": existing.alt_en,
            "gallery-0-caption_ru": existing.caption_ru,
            "gallery-0-caption_en": existing.caption_en,
            "gallery-0-col_span": "1",
            "gallery-0-row_span": "2",
            "gallery-0-order": "1",
            "gallery-0-is_active": "on",
            "gallery-1-alt_ru": "Новый кадр",
            "gallery-1-alt_en": "New frame",
            "gallery-1-caption_ru": "Новый",
            "gallery-1-caption_en": "New",
            "gallery-1-col_span": "1",
            "gallery-1-row_span": "2",
            "gallery-1-order": "2",
            "gallery-1-is_active": "on",
            "gallery-1-image": _tiny_jpeg("gallery-new.jpg"),
        },
    )
    assert response.status_code in (200, 302)
    assert GalleryPhoto.objects.count() == 2
    added = GalleryPhoto.objects.exclude(pk=existing.pk).get()
    assert added.alt_ru == "Новый кадр"
    assert added.image


@pytest.mark.django_db
def test_admin_personality_adds_and_deletes_items(client, admin_user):
    from src.core.models import PersonalityItem

    SiteSettings.get_solo()
    fact = PersonalityItem.objects.create(
        group=PersonalityItem.Group.FACTS,
        label_ru="Возраст",
        label_en="Age",
        value_ru="32",
        value_en="32",
        order=1,
        is_active=True,
    )
    extra = PersonalityItem.objects.create(
        group=PersonalityItem.Group.EXTRAS,
        label_ru="",
        label_en="",
        value_ru="мастер спорта",
        value_en="Master of Sport",
        order=1,
        is_active=True,
    )
    client.force_login(admin_user)
    url = reverse("admin:core_homepersonalitysettings_change", args=[1])
    get_resp = client.get(url)
    assert get_resp.status_code == 200
    html = get_resp.content.decode()
    assert "Добавить пункт" in html
    assert 'name="personality_facts-TOTAL_FORMS"' in html
    assert 'name="personality_extras-TOTAL_FORMS"' in html
    assert 'data-cms-lang="ru"' in html
    assert 'data-cms-lang="en"' in html
    assert "cms-lang-pane--ru" in html
    assert "cms-lang-pane--en" in html
    assert "cms_lang_tabs.js" in html

    response = client.post(
        url,
        {
            "section_visible": "on",
            "block__home__personality.eyebrow__ru": "Личность",
            "block__home__personality.eyebrow__en": "Personality",
            "block__home__personality.title__ru": "Дополнительная",
            "block__home__personality.title__en": "Additional",
            "block__home__personality.title_accent__ru": "информация",
            "block__home__personality.title_accent__en": "information",
            "block__home__personality.facts_title__ru": "Внешность",
            "block__home__personality.facts_title__en": "Appearance",
            "block__home__personality.languages__ru": "Языки",
            "block__home__personality.languages__en": "Languages",
            "block__home__personality.respect__ru": "Уважаю",
            "block__home__personality.respect__en": "Respect",
            "block__home__personality.education__ru": "Образование",
            "block__home__personality.education__en": "Education",
            "block__home__personality.travel__ru": "Путешествия",
            "block__home__personality.travel__en": "Travel",
            "personality_facts-TOTAL_FORMS": "2",
            "personality_facts-INITIAL_FORMS": "1",
            "personality_facts-MIN_NUM_FORMS": "0",
            "personality_facts-MAX_NUM_FORMS": "1000",
            "personality_facts-0-id": str(fact.pk),
            "personality_facts-0-label_ru": "Возраст",
            "personality_facts-0-label_en": "Age",
            "personality_facts-0-value_ru": "33",
            "personality_facts-0-value_en": "33",
            "personality_facts-0-order": "1",
            "personality_facts-0-is_active": "on",
            "personality_facts-1-label_ru": "Хобби",
            "personality_facts-1-label_en": "Hobby",
            "personality_facts-1-value_ru": "йога",
            "personality_facts-1-value_en": "yoga",
            "personality_facts-1-order": "2",
            "personality_facts-1-is_active": "on",
            "personality_extras-TOTAL_FORMS": "1",
            "personality_extras-INITIAL_FORMS": "1",
            "personality_extras-MIN_NUM_FORMS": "0",
            "personality_extras-MAX_NUM_FORMS": "1000",
            "personality_extras-0-id": str(extra.pk),
            "personality_extras-0-label_ru": "",
            "personality_extras-0-label_en": "",
            "personality_extras-0-value_ru": "мастер спорта",
            "personality_extras-0-value_en": "Master of Sport",
            "personality_extras-0-order": "1",
            "personality_extras-0-is_active": "on",
            "personality_extras-0-DELETE": "on",
        },
    )
    assert response.status_code in (200, 302)
    fact.refresh_from_db()
    assert fact.value_ru == "33"
    assert PersonalityItem.objects.filter(group=PersonalityItem.Group.FACTS).count() == 2
    added = PersonalityItem.objects.filter(label_ru="Хобби").get()
    assert added.value_en == "yoga"
    assert not PersonalityItem.objects.filter(pk=extra.pk).exists()
