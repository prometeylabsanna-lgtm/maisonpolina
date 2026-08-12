import pytest
from django.urls import reverse
from django.utils import translation

from src.core.models import SiteBlock
from src.formats.models import ServiceFormat


@pytest.mark.django_db
def test_language_remembered_on_next_visit(client, settings):
    response = client.get("/en/")
    assert response.status_code == 200
    cookie_name = settings.LANGUAGE_COOKIE_NAME
    assert response.cookies[cookie_name].value == "en"

    response = client.get("/", follow=False)
    assert response.status_code in (301, 302)
    assert "/en/" in response["Location"]


@pytest.mark.django_db
def test_language_alternate_urls(client):
    response = client.get(reverse("core:home"))
    assert response.status_code == 200
    assert "alternate_urls" in response.context
    assert response.context["alternate_urls"]["ru"].startswith("/ru/")
    assert response.context["alternate_urls"]["en"].startswith("/en/")


@pytest.mark.django_db
def test_en_falls_back_to_ru():
    block = SiteBlock.objects.create(
        page="home",
        key="test.fallback",
        text_ru="Русский текст",
        text_en="",
    )
    with translation.override("en"):
        assert block.get_text("text") == "Русский текст"


@pytest.mark.django_db
def test_hidden_format_not_on_home(client):
    ServiceFormat.objects.create(
        title_ru="Hidden",
        title_en="Hidden",
        is_active=False,
        order=1,
    )
    ServiceFormat.objects.create(
        title_ru="Visible",
        title_en="Visible",
        is_active=True,
        order=2,
    )
    response = client.get(reverse("core:home"))
    titles = [f.title_ru for f in response.context["formats"]]
    assert "Visible" in titles
    assert "Hidden" not in titles


@pytest.mark.django_db
def test_format_image_on_home(client):
    from io import BytesIO

    from django.core.files.uploadedfile import SimpleUploadedFile
    from PIL import Image

    buf = BytesIO()
    Image.new("RGB", (12, 9), (90, 24, 30)).save(buf, format="JPEG")
    buf.seek(0)
    fmt = ServiceFormat.objects.create(
        title_ru="Ужин",
        title_en="Dinner",
        is_active=True,
        order=1,
    )
    fmt.image.save(
        "format.jpg",
        SimpleUploadedFile("format.jpg", buf.read(), content_type="image/jpeg"),
        save=True,
    )
    response = client.get("/ru/")
    html = response.content.decode()
    assert "card__photo" in html
    assert "format" in html


@pytest.mark.django_db
def test_format_image_on_home(client):
    from io import BytesIO

    from django.core.files.uploadedfile import SimpleUploadedFile
    from PIL import Image

    buf = BytesIO()
    Image.new("RGB", (12, 9), (90, 24, 30)).save(buf, format="JPEG")
    buf.seek(0)
    fmt = ServiceFormat.objects.create(
        title_ru="Ужин",
        title_en="Dinner",
        is_active=True,
        order=1,
    )
    fmt.image.save(
        "format.jpg",
        SimpleUploadedFile("format.jpg", buf.read(), content_type="image/jpeg"),
        save=True,
    )
    response = client.get("/ru/")
    html = response.content.decode()
    assert "card__photo" in html
    assert "format" in html
