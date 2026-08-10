import os

from decouple import config
from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    config("DJANGO_SETTINGS_MODULE", default="config.settings.production"),
)

application = get_wsgi_application()

# Ephemeral SQLite on Vercel: create tables before first request.
try:
    from src.core.vercel_bootstrap import bootstrap_vercel_db

    bootstrap_vercel_db()
except Exception:
    # Request path will surface errors; avoid crashing import if build probes WSGI.
    pass
