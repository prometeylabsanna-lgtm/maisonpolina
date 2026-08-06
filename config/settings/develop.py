from decouple import config

from .base import *  # noqa: F403

SECRET_KEY = config("SECRET_KEY", default="dev-only-insecure-key-do-not-use-in-prod")
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]", "web", "testserver"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
