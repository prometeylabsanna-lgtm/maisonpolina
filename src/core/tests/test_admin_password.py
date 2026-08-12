import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from src.core.admin_nav import build_admin_navigation
from src.core.vercel_bootstrap import ensure_admin_superuser


@pytest.fixture
def admin_user(db):
    User = get_user_model()
    return User.objects.create_superuser("admin", "admin@example.com", "password123456")


def test_password_change_in_sidebar():
    links = [
        str(item["link"])
        for group in build_admin_navigation()
        for item in group["items"]
    ]
    assert reverse("admin:password_change") in links
    titles = [
        item["title"]
        for group in build_admin_navigation()
        for item in group["items"]
    ]
    assert "Смена пароля" in titles


@pytest.mark.django_db
def test_admin_password_change_form(client, admin_user):
    client.force_login(admin_user)
    url = reverse("admin:password_change")
    response = client.get(url)
    assert response.status_code == 200
    assert b"old_password" in response.content

    response = client.post(
        url,
        {
            "old_password": "password123456",
            "new_password1": "NewOwnerPass99",
            "new_password2": "NewOwnerPass99",
        },
    )
    assert response.status_code in (200, 302)
    admin_user.refresh_from_db()
    assert admin_user.check_password("NewOwnerPass99")


@pytest.mark.django_db
def test_bootstrap_does_not_overwrite_admin_password(monkeypatch):
    User = get_user_model()
    user = User.objects.create_superuser(
        "owner", "owner@example.com", "OwnerPass1234"
    )
    monkeypatch.setenv("DJANGO_SUPERUSER_USERNAME", "owner")
    monkeypatch.setenv("DJANGO_SUPERUSER_PASSWORD", "env-password-xx")
    monkeypatch.setenv("DJANGO_SUPERUSER_EMAIL", "owner@example.com")

    ensure_admin_superuser()
    user.refresh_from_db()
    assert user.check_password("OwnerPass1234")
    assert not user.check_password("env-password-xx")
