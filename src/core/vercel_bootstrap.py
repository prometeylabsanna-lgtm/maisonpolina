"""One-shot DB bootstrap for ephemeral Vercel SQLite (/tmp).

When DATABASE_URL points to Postgres (Supabase), skip — migrate/seed separately.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)
_DONE = False


def bootstrap_vercel_db() -> None:
    global _DONE
    if _DONE:
        return
    if not os.environ.get("VERCEL"):
        _DONE = True
        return

    db_url = os.environ.get("DATABASE_URL", "").strip()
    if db_url.startswith("postgres"):
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
    _DONE = True
    logger.info("Vercel SQLite bootstrap complete")
