"""Vercel / WSGI entrypoint at repository root."""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

from config.wsgi import application  # noqa: E402

try:
    from src.core.vercel_bootstrap import bootstrap_vercel_db

    bootstrap_vercel_db()
except Exception:
    pass
