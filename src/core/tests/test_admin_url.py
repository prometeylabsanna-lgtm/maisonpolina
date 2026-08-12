import pytest
from django.conf import settings
from django.urls import reverse


@pytest.mark.django_db
def test_default_admin_path_is_404(client):
    assert client.get("/admin/").status_code == 404
    assert client.get("/admin/login/").status_code == 404


@pytest.mark.django_db
def test_secret_admin_url_serves_login(client):
    url = reverse("admin:login")
    assert url.startswith("/" + settings.ADMIN_URL.strip("/"))
    assert not url.startswith("/admin/")
    response = client.get(url)
    assert response.status_code == 200


def test_robots_txt_does_not_leak_admin_url(client):
    response = client.get("/robots.txt")
    body = response.content.decode()
    assert "Disallow: /admin/" in body
    assert settings.ADMIN_URL.strip("/") not in body
