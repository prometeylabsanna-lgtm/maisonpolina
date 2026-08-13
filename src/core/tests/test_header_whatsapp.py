import pytest
from django.urls import reverse

from src.core.models import PersonalityItem, SiteSettings


@pytest.mark.django_db
def test_whatsapp_placeholder_is_hidden(client):
    settings = SiteSettings.get_solo()
    settings.whatsapp_url = "https://wa.me/"
    settings.save()
    html = client.get(reverse("core:home")).content.decode()
    assert "header__whatsapp" not in html
    assert settings.get_whatsapp_url() == ""


@pytest.mark.django_db
def test_whatsapp_button_in_header(client):
    settings = SiteSettings.get_solo()
    settings.whatsapp_url = "https://wa.me/380954722029"
    settings.save()
    html = client.get(reverse("core:home")).content.decode()
    assert "header__whatsapp" in html
    assert "https://wa.me/380954722029" in html
    assert settings.get_whatsapp_url() == "https://wa.me/380954722029"
    assert 'aria-label="WhatsApp"' in html


@pytest.mark.django_db
def test_whatsapp_qr_link_in_header(client):
    settings = SiteSettings.get_solo()
    settings.whatsapp_url = "https://wa.me/qr/ZPQAL5UEFCQIN1"
    settings.save()
    html = client.get(reverse("core:home")).content.decode()
    assert "header__whatsapp" in html
    assert "https://wa.me/qr/ZPQAL5UEFCQIN1" in html
    assert settings.get_whatsapp_url() == "https://wa.me/qr/ZPQAL5UEFCQIN1"


@pytest.mark.django_db
def test_privacy_link_in_footer_and_mobile_nav(client):
    html = client.get(reverse("core:home")).content.decode()
    privacy = reverse("core:privacy")
    assert "footer__legal-link" in html
    assert "mobile-nav__privacy" in html
    assert privacy in html


@pytest.mark.django_db
def test_phone_in_header_and_footer(client):
    settings = SiteSettings.get_solo()
    settings.phone = "+380 95 472 7859"
    settings.save()
    html = client.get(reverse("core:home")).content.decode()
    assert "+380 95 472 7859" in html
    assert "tel:+380954727859" in html


@pytest.mark.django_db
def test_hidden_personality_facts_not_on_home(client):
    SiteSettings.get_solo()
    PersonalityItem.objects.create(
        group=PersonalityItem.Group.FACTS,
        label_ru="Обувь",
        label_en="Shoes",
        value_ru="39",
        value_en="39",
        order=1,
        is_active=False,
    )
    PersonalityItem.objects.create(
        group=PersonalityItem.Group.FACTS,
        label_ru="Возраст",
        label_en="Age",
        value_ru="32",
        value_en="32",
        order=2,
        is_active=True,
    )
    html = client.get(reverse("core:home")).content.decode()
    assert "Обувь" not in html
    assert "Возраст" in html
