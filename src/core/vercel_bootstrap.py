"""One-shot DB bootstrap for ephemeral Vercel SQLite (/tmp)."""

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)
_DONE = False


def bootstrap_vercel_db() -> None:
    global _DONE
    if _DONE or not os.environ.get("VERCEL"):
        return
    _DONE = True

    from django.conf import settings
    from django.core.management import call_command

    engine = settings.DATABASES["default"]["ENGINE"]
    if "sqlite" not in engine:
        return

    try:
        call_command("migrate", interactive=False, run_syncdb=True, verbosity=0)
        from src.core.models import SiteSettings

        SiteSettings.get_solo()
    except Exception:
        logger.exception("Vercel SQLite bootstrap failed")
        _DONE = False
        raise
