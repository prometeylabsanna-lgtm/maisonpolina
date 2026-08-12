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
    assert item.author_name_ru == "Мария"
    assert item.author_name_en == "Мария"
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
        author_name_ru="Visible",
        author_name_en="Visible",
        text_ru="Активный отзыв достаточно длинный",
        text_en="Active review text here",
        rating=5,
        is_active=True,
    )
    Testimonial.objects.create(
        author_name_ru="Hidden",
        author_name_en="Hidden",
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


@pytest.mark.django_db
def test_testimonial_author_name_by_locale(client):
    Testimonial.objects.create(
        author_name_ru="Александр Г.",
        author_name_en="Alexander G.",
        role_ru="Дирижёр",
        role_en="Conductor",
        text_ru="Тихая работа.",
        text_en="Quiet work.",
        rating=5,
        is_active=True,
    )
    ru = client.get("/ru/")
    assert ru.status_code == 200
    assert "Александр Г.".encode() in ru.content
    assert b"Alexander G." not in ru.content

    en = client.get("/en/")
    assert en.status_code == 200
    assert b"Alexander G." in en.content
    assert "Александр Г.".encode() not in en.content


@pytest.mark.django_db
def test_testimonial_photo_on_home(client):
    from io import BytesIO

    from django.core.files.uploadedfile import SimpleUploadedFile
    from PIL import Image

    buf = BytesIO()
    Image.new("RGB", (8, 8), (80, 20, 24)).save(buf, format="JPEG")
    buf.seek(0)
    item = Testimonial.objects.create(
        author_name_ru="Анна",
        author_name_en="Anna",
        text_ru="Длинный отзыв о встрече, который должен появиться на главной.",
        text_en="A long review that should appear on the home page.",
        rating=5,
        is_active=True,
    )
    item.photo.save(
        "reviewer.jpg",
        SimpleUploadedFile("reviewer.jpg", buf.read(), content_type="image/jpeg"),
        save=True,
    )
    response = client.get("/ru/")
    html = response.content.decode()
    assert "carousel__photo" in html
    assert "reviewer" in html
