import pytest
from django.urls import reverse

from src.reviews.models import Testimonial


@pytest.mark.django_db
def test_review_submit_pending(client):
    url = reverse("reviews:submit")
    response = client.post(
        url,
        {
            "name": "Мария",
            "text": "Очень достойный вечер, всё прошло спокойно.",
            "rating": "5",
            "language": "ru",
            "form_ts": "1",
            "website": "",
        },
    )
    assert response.status_code == 200
    assert Testimonial.objects.count() == 1
    item = Testimonial.objects.get()
    assert item.author_name == "Мария"
    assert item.rating == 5
    assert item.is_active is False
    assert item.is_public_submission is True
    assert item.text_ru == item.text_en


@pytest.mark.django_db
def test_review_invalid(client):
    url = reverse("reviews:submit")
    response = client.post(
        url,
        {"name": "", "text": "short", "rating": "0", "form_ts": "1", "website": ""},
    )
    assert response.status_code == 422
    assert Testimonial.objects.count() == 0


@pytest.mark.django_db
def test_review_honeypot(client):
    url = reverse("reviews:submit")
    response = client.post(
        url,
        {
            "name": "Bot",
            "text": "Spam message long enough here",
            "rating": "5",
            "form_ts": "1",
            "website": "http://spam.test",
        },
    )
    assert response.status_code == 200
    assert Testimonial.objects.count() == 0


@pytest.mark.django_db
def test_active_testimonials_only_on_home(client):
    Testimonial.objects.create(
        author_name="Visible",
        text_ru="Активный отзыв достаточно длинный",
        text_en="Active review text here",
        rating=5,
        is_active=True,
    )
    Testimonial.objects.create(
        author_name="Hidden",
        text_ru="Скрытый отзыв достаточно длинный",
        text_en="Hidden review text here",
        rating=4,
        is_active=False,
        is_public_submission=True,
    )
    response = client.get("/ru/")
    assert response.status_code == 200
    assert b"Visible" in response.content
    assert b"Hidden" not in response.content
