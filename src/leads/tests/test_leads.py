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
            "contact": "+79991234567",
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
                "contact": "+79991234567",
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


def _lead_payload(**overrides):
    data = {
        "name": "Иван",
        "contact": "+38 (099) 123-45-67",
        "message": "Здравствуйте",
        "consent": "on",
        "service": "Знакомство",
        "source": LeadSource.HERO,
        "language": "ru",
        "form_ts": "1",
        "website": "",
    }
    data.update(overrides)
    return data


@pytest.mark.django_db
def test_lead_name_rejects_digits(client):
    url = reverse("leads:submit")
    response = client.post(url, _lead_payload(name="Иван2"))
    assert response.status_code == 422
    assert Lead.objects.count() == 0
    assert "не повинно містити цифр" in response.content.decode()


@pytest.mark.django_db
def test_lead_phone_rejects_letters(client):
    url = reverse("leads:submit")
    response = client.post(url, _lead_payload(contact="abc123"))
    assert response.status_code == 422
    assert Lead.objects.count() == 0
    assert (
        "Номер телефону не може містити літер та має бути не довшим за 14 цифр."
        in response.content.decode()
    )


@pytest.mark.django_db
def test_lead_phone_rejects_too_many_digits(client):
    url = reverse("leads:submit")
    response = client.post(url, _lead_payload(contact="123456789012345"))
    assert response.status_code == 422
    assert Lead.objects.count() == 0


@pytest.mark.django_db
def test_lead_phone_allows_formatted_number(client):
    url = reverse("leads:submit")
    response = client.post(url, _lead_payload(contact="+38 (099) 123-45-67"))
    assert response.status_code == 200
    assert Lead.objects.count() == 1


@pytest.mark.django_db
def test_lead_message_rejects_one_character(client):
    url = reverse("leads:submit")
    response = client.post(url, _lead_payload(message="а"))
    assert response.status_code == 422
    assert Lead.objects.count() == 0
    assert "Текст відгуку повинен містити мінімум 2 символи." in response.content.decode()
