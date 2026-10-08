import json

import pytest
from django.urls import reverse

from src.core.models import SiteSettings
from src.faq.models import FaqItem


@pytest.mark.django_db
def test_home_has_gtm_og_and_jsonld(client, settings):
    settings.GTM_ID = "GTM-KQVSVDPQ"
    SiteSettings.get_solo()
    FaqItem.objects.create(
        question_ru="Как связаться?",
        question_en="How to contact?",
        answer_ru="<p>Через форму на сайте.</p>",
        answer_en="<p>Via the site form.</p>",
        order=1,
        is_active=True,
    )
    html = client.get(reverse("core:home")).content.decode()
    assert "GTM-KQVSVDPQ" in html
    assert 'property="og:title"' in html
    assert 'name="twitter:card"' in html
    assert "application/ld+json" in html
    assert '"@type":"Organization"' in html.replace(" ", "")
    assert '"@type":"WebSite"' in html.replace(" ", "")
    assert '"@type":"FAQPage"' in html.replace(" ", "")
    assert "googletagmanager.com" in html


@pytest.mark.django_db
def test_terms_page_and_sitemap(client):
    SiteSettings.get_solo()
    terms = reverse("core:terms")
    response = client.get(terms)
    assert response.status_code == 200
    html = response.content.decode()
    assert "Условия" in html or "Terms" in html
    sitemap = client.get("/sitemap.xml").content.decode()
    assert "terms" in sitemap


@pytest.mark.django_db
def test_faq_jsonld_strips_html(client):
    SiteSettings.get_solo()
    FaqItem.objects.create(
        question_ru="Вопрос?",
        answer_ru="<p>Ответ <strong>важный</strong>.</p>",
        is_active=True,
    )
    html = client.get(reverse("core:home")).content.decode()
    start = html.index('type="application/ld+json"')
    # Find FAQPage block
    assert "FAQPage" in html
    chunk = html[html.index("FAQPage") - 80 : html.index("FAQPage") + 400]
    assert "<p>" not in chunk
    assert "Ответ важный" in chunk or "важный" in html
