from .production import *  # noqa: F403

# TLS terminates at nginx; gunicorn stays on HTTP.
# Internal healthcheck hits http://127.0.0.1:8000/healthz/ — redirect breaks it.
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
