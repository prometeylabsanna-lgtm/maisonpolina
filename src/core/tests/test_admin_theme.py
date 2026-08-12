import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse


@pytest.fixture
def admin_user(db):
    User = get_user_model()
    return User.objects.create_superuser("admin", "admin@example.com", "password123456")


def test_unfold_theme_is_unlocked():
    assert not settings.UNFOLD.get("THEME")


def test_unfold_primary_is_burgundy():
    primary = settings.UNFOLD["COLORS"]["primary"]
    assert primary["600"] == "#4c0d13"
    assert primary["500"] == "#8a2433"


@pytest.mark.django_db
def test_admin_theme_switcher_visible(client, admin_user):
    client.force_login(admin_user)
    html = client.get(reverse("admin:index")).content.decode()
    assert "switchTheme('light')" in html
    assert "switchTheme('dark')" in html
    assert "Светлая" in html
    assert "Темная" in html
    assert "favicon-32x32.png" in html
    assert "apple-touch-icon.png" in html
    assert "admin-brand__mark" in html
    assert "MaisonPolina" in html
