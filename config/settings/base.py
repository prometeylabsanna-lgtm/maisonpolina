import re
from pathlib import Path

from decouple import config
from django.core.exceptions import ImproperlyConfigured
from django.templatetags.static import static

_ADMIN_URL_RE = re.compile(r"^[A-Za-z0-9_-]{8,64}$")


def _normalize_admin_url(raw: str) -> str:
    slug = (raw or "").strip().strip("/")
    if slug.lower() == "admin" or not _ADMIN_URL_RE.fullmatch(slug):
        raise ImproperlyConfigured(
            "ADMIN_URL must be a random 8–64 character path "
            "(letters, digits, _ or -), not 'admin'."
        )
    return f"{slug}/"


def _resolve_base_dir() -> Path:
    """Prefer repo root (manage.py/templates), not site-packages if config was installed."""
    here = Path(__file__).resolve().parent.parent.parent
    if (here / "manage.py").exists() or (here / "templates").is_dir():
        return here
    cwd = Path.cwd()
    if (cwd / "manage.py").exists() or (cwd / "templates").is_dir():
        return cwd
    return here


_BASE_PATH = _resolve_base_dir()
BASE_DIR = str(_BASE_PATH)

SECRET_KEY = config(
    "SECRET_KEY",
    default="insecure-build-placeholder-change-me",
)
ADMIN_URL = _normalize_admin_url(
    config("ADMIN_URL", default="build-placeholder-admin-path")
)

DEBUG = False

ALLOWED_HOSTS: list[str] = []

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django_htmx",
    "csp",
    "tinymce",
    "src.core",
    "src.gallery",
    "src.formats",
    "src.reviews",
    "src.faq",
    "src.leads",
    "src.chat",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "src.core.middleware.AdminRussianLocaleMiddleware",
    "src.core.middleware.LanguageCookieMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "csp.middleware.CSPMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(_BASE_PATH / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "src.core.context_processors.site_context",
                "src.core.context_processors.static_version",
                "src.core.context_processors.alternate_urls",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(_BASE_PATH / "db.sqlite3"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 12},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
]

LANGUAGE_CODE = "ru"
LANGUAGES = [
    ("ru", "Русский"),
    ("en", "English"),
]
LANGUAGE_COOKIE_AGE = 60 * 60 * 24 * 365
LANGUAGE_COOKIE_SAMESITE = "Lax"
LOCALE_PATHS = [str(_BASE_PATH / "locale")]
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = str(_BASE_PATH / "staticfiles")
STATICFILES_DIRS = [str(_BASE_PATH / "static")]

MEDIA_URL = "/media/"
MEDIA_ROOT = str(_BASE_PATH / "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SESSION_COOKIE_AGE = 60 * 60 * 24 * 7
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True

CONTENT_SECURITY_POLICY = {
    "EXCLUDE_URL_PREFIXES": (f"/{ADMIN_URL}",),
    "DIRECTIVES": {
        "default-src": ["'self'"],
        "script-src": ["'self'"],
        "style-src": ["'self'", "'unsafe-inline'"],
        "font-src": ["'self'", "data:"],
        "img-src": ["'self'", "data:", "blob:"],
        "media-src": ["'self'", "blob:", "https:"],
        "connect-src": ["'self'"],
        "frame-ancestors": ["'none'"],
        "base-uri": ["'self'"],
        "form-action": ["'self'"],
    },
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@example.com")
LEADS_NOTIFY_EMAIL = config("LEADS_NOTIFY_EMAIL", default="")
EMAIL_HOST = config("EMAIL_HOST", default="")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)

TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN", default="")
TELEGRAM_CHAT_ID = config("TELEGRAM_CHAT_ID", default="")
TELEGRAM_WEBHOOK_SECRET = config("TELEGRAM_WEBHOOK_SECRET", default="")
TELEGRAM_WEBHOOK_URL = config("TELEGRAM_WEBHOOK_URL", default="")

SITE_URL = config("SITE_URL", default="http://localhost:8000")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "src": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

UNFOLD = {
    "SITE_TITLE": "MaisonPolina",
    "SITE_HEADER": "MaisonPolina",
    "SITE_SUBHEADER": "Панель сайта",
    "SITE_SYMBOL": "person",
    "SITE_ICON": lambda request: static("apple-touch-icon.png"),
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "href": lambda request: static("favicon.ico"),
            "sizes": "any",
        },
        {
            "rel": "icon",
            "type": "image/png",
            "sizes": "32x32",
            "href": lambda request: static("favicon-32x32.png"),
        },
        {
            "rel": "icon",
            "type": "image/png",
            "sizes": "16x16",
            "href": lambda request: static("favicon-16x16.png"),
        },
        {
            "rel": "apple-touch-icon",
            "sizes": "180x180",
            "href": lambda request: static("apple-touch-icon.png"),
        },
    ],
    "THEME": None,
    "STYLES": [
        lambda request: static("css/admin/changelist_filters.css"),
        lambda request: static("css/admin/brand.css"),
    ],
    "SCRIPTS": [
        lambda request: static("js/admin/theme-default.js"),
    ],
    "COLORS": {
        "primary": {
            "50": "#faf2f3",
            "100": "#f3e4e6",
            "200": "#e5c5c9",
            "300": "#c9959c",
            "400": "#9a4450",
            "500": "#8a2433",
            "600": "#4c0d13",
            "700": "#3a0a0f",
            "800": "#2a080c",
            "900": "#1a0508",
            "950": "#0f0305",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "command_search": True,
        "show_all_applications": False,
        "navigation": "src.core.admin_nav.build_admin_navigation",
    },
}

TINYMCE_DEFAULT_CONFIG = {
    "height": 360,
    "menubar": "edit insert view format",
    "plugins": (
        "advlist autolink lists link charmap preview "
        "searchreplace visualblocks code fullscreen "
        "wordcount quickbars"
    ),
    "toolbar": (
        "undo redo | blocks | bold italic underline | "
        "alignleft aligncenter alignright | bullist numlist | "
        "link | removeformat | code"
    ),
    "block_formats": "Абзац=p; Заголовок 2=h2; Заголовок 3=h3; Цитата=blockquote",
    "browser_spellcheck": True,
    "promotion": False,
    "branding": False,
    "skin": "oxide",
    "content_css": False,
    "relative_urls": False,
    "remove_script_host": False,
    "convert_urls": True,
}
TINYMCE_COMPRESSOR = False
