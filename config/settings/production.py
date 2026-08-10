from urllib.parse import urlparse
import os

from decouple import Csv, config

from .base import *  # noqa: F403

DEBUG = False

SECRET_KEY = config("SECRET_KEY", default="insecure-build-placeholder-change-me")

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default=".vercel.app,localhost,127.0.0.1",
    cast=Csv(),
)
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default="https://*.vercel.app",
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
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

_database_url = config("DATABASE_URL", default="")
_postgres_db = config("POSTGRES_DB", default="")

if _database_url:
    _db = urlparse(_database_url)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": (_db.path or "").lstrip("/"),
            "USER": _db.username or "",
            "PASSWORD": _db.password or "",
            "HOST": _db.hostname or "",
            "PORT": str(_db.port or 5432),
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
elif os.environ.get("VERCEL"):
    # Serverless FS is read-only except /tmp — local sqlite path would 500.
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "/tmp/maisonpolina.sqlite3",
        }
    }
    MEDIA_ROOT = "/tmp/maisonpolina-media"
# else: keep SQLite from base (local collectstatic / build without DB)

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
