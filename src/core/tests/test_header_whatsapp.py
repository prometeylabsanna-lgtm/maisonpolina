import pytest
from django.urls import reverse

from src.core.models import SiteSettings


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
def test_privacy_link_in_footer_and_mobile_nav(client):
    html = client.get(reverse("core:home")).content.decode()
    privacy = reverse("core:privacy")
    assert "footer__legal-link" in html
    assert "mobile-nav__privacy" in html
    assert privacy in html
