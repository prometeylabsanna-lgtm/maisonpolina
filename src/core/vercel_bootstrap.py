"""One-shot DB bootstrap for ephemeral Vercel SQLite (/tmp).

When DATABASE_URL points to Postgres (Supabase), migrate/seed separately;
still ensures the admin superuser exists.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)
_DONE = False


def ensure_admin_superuser() -> None:
    """Create admin from env if missing. Never overwrite a password set in admin."""
    from django.contrib.auth import get_user_model

    username = (os.environ.get("DJANGO_SUPERUSER_USERNAME") or "admin").strip()
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD") or "admin"
    email = (os.environ.get("DJANGO_SUPERUSER_EMAIL") or "admin@example.com").strip()

    User = get_user_model()
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": email,
            "is_staff": True,
            "is_superuser": True,
        },
    )
    changed = created
    if user.email != email:
        user.email = email
        changed = True
    if not user.is_staff or not user.is_superuser:
        user.is_staff = True
        user.is_superuser = True
        changed = True
    if created or not user.has_usable_password():
        user.set_password(password)
        changed = True
    if changed:
        user.save()
        logger.info("Vercel admin superuser %s", "created" if created else "updated")


def bootstrap_vercel_db() -> None:
    global _DONE
    if _DONE:
        return
    if not os.environ.get("VERCEL"):
        _DONE = True
        return

    db_url = os.environ.get("DATABASE_URL", "").strip()
    if db_url.startswith("postgres"):
        try:
            ensure_admin_superuser()
        except Exception:
            logger.exception("Vercel Postgres admin bootstrap failed")
        _DONE = True
        return

    from django.conf import settings
    from django.core.management import call_command

    engine = settings.DATABASES["default"]["ENGINE"]
    if "sqlite" not in engine:
        _DONE = True
        return

    db_path = Path("/tmp/maisonpolina.sqlite3")
    marker = Path("/tmp/maisonpolina.bootstrapped")
    media = Path("/tmp/maisonpolina-media")
    media.mkdir(parents=True, exist_ok=True)

    needs_migrate = not (
        marker.exists() and db_path.exists() and db_path.stat().st_size > 0
    )
    if needs_migrate:
        call_command("migrate", interactive=False, verbosity=0)
        marker.write_text("ok", encoding="utf-8")

    call_command("seed_content", verbosity=0)
    ensure_admin_superuser()
    _DONE = True
    logger.info("Vercel SQLite bootstrap complete")
