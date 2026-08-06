import pytest
from django.urls import reverse
from django.utils import translation

from src.core.models import SiteBlock
from src.formats.models import ServiceFormat


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
