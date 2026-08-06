from unittest.mock import patch

import pytest
from django.urls import reverse

from src.leads.models import Lead, LeadSource


@pytest.mark.django_db
def test_lead_create_valid(client):
    url = reverse("leads:submit")
    response = client.post(
        url,
        {
            "name": "Иван",
            "contact": "+79991234567",
            "message": "Здравствуйте",
            "consent": "on",
            "service": "Знакомство",
            "source": LeadSource.HERO,
            "language": "ru",
            "form_ts": "1",
            "website": "",
        },
    )
    assert response.status_code == 200
    assert Lead.objects.count() == 1
    lead = Lead.objects.get()
    assert lead.service == "Знакомство"
    assert lead.source == LeadSource.HERO


@pytest.mark.django_db
def test_lead_invalid(client):
    url = reverse("leads:submit")
    response = client.post(
        url,
        {"name": "", "contact": "", "consent": "", "form_ts": "1", "website": ""},
    )
    assert response.status_code == 422
    assert Lead.objects.count() == 0


@pytest.mark.django_db
def test_lead_honeypot(client):
    url = reverse("leads:submit")
    response = client.post(
        url,
        {
            "name": "Bot",
            "contact": "bot@example.com",
            "consent": "on",
            "form_ts": "1",
            "website": "http://spam.test",
        },
    )
    assert response.status_code == 200
    assert Lead.objects.count() == 0


@pytest.mark.django_db
def test_lead_saved_when_notify_fails(client):
    url = reverse("leads:submit")
    with patch("src.leads.views.notify", side_effect=RuntimeError("down")):
        response = client.post(
            url,
            {
                "name": "Иван",
                "contact": "ivan@example.com",
                "consent": "on",
                "service": "Test",
                "source": LeadSource.CONTACTS,
                "language": "ru",
                "form_ts": "1",
                "website": "",
            },
        )
    assert response.status_code == 200
    assert Lead.objects.count() == 1
    assert Lead.objects.get().notified_at is None
