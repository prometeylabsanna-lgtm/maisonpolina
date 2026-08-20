from decouple import config

from .production import *  # noqa: F403

# TLS terminates at nginx; gunicorn stays on HTTP.
# Internal healthcheck hits http://127.0.0.1:8000/healthz/ — redirect breaks it.
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

# HTTP-first on Droplet: cookies Secure only after USE_HTTPS=true (post-certbot).
_USE_HTTPS = config("USE_HTTPS", default=False, cast=bool)
SESSION_COOKIE_SECURE = _USE_HTTPS
CSRF_COOKIE_SECURE = _USE_HTTPS
LANGUAGE_COOKIE_SECURE = _USE_HTTPS
SECURE_HSTS_SECONDS = 31536000 if _USE_HTTPS else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = _USE_HTTPS
SECURE_HSTS_PRELOAD = _USE_HTTPS
