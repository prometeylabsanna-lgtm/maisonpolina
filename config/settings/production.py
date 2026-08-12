from urllib.parse import unquote, urlparse
import os

from decouple import Csv, config
from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403

DEBUG = False

SECRET_KEY = config("SECRET_KEY", default="insecure-build-placeholder-change-me")

IS_VERCEL = bool(os.environ.get("VERCEL"))

# Hostiq / shared hosting: set ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS explicitly.
# Vercel defaults apply only when VERCEL=1.
_default_hosts = (
    ".vercel.app,localhost,127.0.0.1"
    if IS_VERCEL
    else "localhost,127.0.0.1"
)
_default_csrf = "https://*.vercel.app" if IS_VERCEL else ""

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default=_default_hosts,
    cast=Csv(),
)
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default=_default_csrf,
    cast=lambda v: [s.strip() for s in v.split(",") if s.strip()],
)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
SECURE_SSL_REDIRECT = config(
    "SECURE_SSL_REDIRECT",
    default=not bool(os.environ.get("VERCEL")),
    cast=bool,
)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
LANGUAGE_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

DATABASE_URL = config("DATABASE_URL", default="").strip()
_postgres_db = config("POSTGRES_DB", default="")

if DATABASE_URL.startswith("postgres"):
    # Managed Postgres (Supabase / Neon / DigitalOcean / Hostiq) — same pattern as AJERES
    _db = urlparse(DATABASE_URL)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": (_db.path or "/").lstrip("/") or "postgres",
            "USER": unquote(_db.username or ""),
            "PASSWORD": unquote(_db.password or ""),
            "HOST": _db.hostname or "",
            "PORT": str(_db.port or 5432),
            "OPTIONS": {
                "sslmode": config("DB_SSLMODE", default="require"),
            },
        }
    }
elif _postgres_db:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": _postgres_db,
            "USER": config("POSTGRES_USER"),
            "PASSWORD": config("POSTGRES_PASSWORD"),
            "HOST": config("DB_HOST", default="db"),
            "PORT": config("DB_PORT", default="5432"),
        }
    }
elif IS_VERCEL:
    # Serverless FS is read-only except /tmp — demo SQLite (ephemeral).
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "/tmp/maisonpolina.sqlite3",
        }
    }
else:
    # Hostiq / bare metal: refuse silent SQLite under multiple gunicorn workers.
    raise ImproperlyConfigured(
        "Production requires DATABASE_URL (postgres://...) or POSTGRES_DB. "
        "SQLite fallback is disabled outside Vercel."
    )

if IS_VERCEL:
    MEDIA_ROOT = "/tmp/maisonpolina-media"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
