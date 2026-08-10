import os

from decouple import config
from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    config("DJANGO_SETTINGS_MODULE", default="config.settings.production"),
)

application = get_wsgi_application()

try:
    from src.core.vercel_bootstrap import bootstrap_vercel_db

    bootstrap_vercel_db()
except Exception:
    # HomeView retries bootstrap; avoid crashing cold start on probe.
    pass
