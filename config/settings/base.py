from pathlib import Path

from decouple import config
from django.urls import reverse_lazy


def _resolve_base_dir() -> Path:
    """Prefer repo root (manage.py/templates), not site-packages if config was installed."""
    here = Path(__file__).resolve().parent.parent.parent
    if (here / "manage.py").exists() or (here / "templates").is_dir():
        return here
    cwd = Path.cwd()
    if (cwd / "manage.py").exists() or (cwd / "templates").is_dir():
        return cwd
    return here


BASE_DIR = _resolve_base_dir()

SECRET_KEY = config(
    "SECRET_KEY",
    default="insecure-build-placeholder-change-me",
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
        "DIRS": [BASE_DIR / "templates"],
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
        "NAME": BASE_DIR / "db.sqlite3",
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
LOCALE_PATHS = [BASE_DIR / "locale"]
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SESSION_COOKIE_AGE = 60 * 60 * 24 * 7
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True

CONTENT_SECURITY_POLICY = {
    "EXCLUDE_URL_PREFIXES": ("/admin/",),
    "DIRECTIVES": {
        "default-src": ("'self'",),
        "script-src": ("'self'",),
        "style-src": ("'self'", "'unsafe-inline'"),
        "font-src": ("'self'", "data:"),
        "img-src": ("'self'", "data:", "blob:"),
        "connect-src": ("'self'",),
        "frame-ancestors": ("'none'",),
        "base-uri": ("'self'",),
        "form-action": ("'self'",),
    },
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@example.com")
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
    "SITE_TITLE": "SelfBrand Admin",
    "SITE_HEADER": "SelfBrand",
    "SITE_SYMBOL": "person",
    "SIDEBAR": {
        "show_search": True,
        "command_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Вміст сторінок",
                "separator": True,
                "items": [
                    {
                        "title": "Hero",
                        "icon": "image",
                        "link": reverse_lazy("admin:core_homeherosettings_changelist"),
                    },
                    {
                        "title": "Про мене",
                        "icon": "person",
                        "link": reverse_lazy("admin:core_homeaboutsettings_changelist"),
                    },
                    {
                        "title": "Особистість",
                        "icon": "badge",
                        "link": reverse_lazy(
                            "admin:core_homepersonalitysettings_changelist"
                        ),
                    },
                    {
                        "title": "Галерея",
                        "icon": "photo_library",
                        "link": reverse_lazy("admin:core_homegallerysettings_changelist"),
                    },
                    {
                        "title": "Формати",
                        "icon": "view_agenda",
                        "link": reverse_lazy("admin:core_homeformatssettings_changelist"),
                    },
                    {
                        "title": "Відгуки",
                        "icon": "format_quote",
                        "link": reverse_lazy("admin:core_hometestimonialssettings_changelist"),
                    },
                    {
                        "title": "Питання",
                        "icon": "help",
                        "link": reverse_lazy("admin:core_homefaqsettings_changelist"),
                    },
                    {
                        "title": "Контакти",
                        "icon": "mail",
                        "link": reverse_lazy("admin:core_homecontactssettings_changelist"),
                    },
                    {
                        "title": "Політика",
                        "icon": "policy",
                        "link": reverse_lazy("admin:core_privacysettings_changelist"),
                    },
                ],
            },
            {
                "title": "Списки",
                "separator": True,
                "items": [
                    {
                        "title": "Формати послуг",
                        "icon": "sell",
                        "link": reverse_lazy("admin:formats_serviceformat_changelist"),
                    },
                    {
                        "title": "Відгуки",
                        "icon": "reviews",
                        "link": reverse_lazy("admin:reviews_testimonial_changelist"),
                    },
                    {
                        "title": "Питання й відповіді",
                        "icon": "quiz",
                        "link": reverse_lazy("admin:faq_faqitem_changelist"),
                    },
                ],
            },
            {
                "title": "Заявки",
                "separator": True,
                "items": [
                    {
                        "title": "Усі заявки",
                        "icon": "inbox",
                        "link": reverse_lazy("admin:leads_lead_changelist"),
                    },
                ],
            },
            {
                "title": "Налаштування",
                "separator": True,
                "items": [
                    {
                        "title": "Сайт",
                        "icon": "settings",
                        "link": reverse_lazy("admin:core_sitesettings_changelist"),
                    },
                    {
                        "title": "SEO",
                        "icon": "travel_explore",
                        "link": reverse_lazy("admin:core_seometa_changelist"),
                    },
                ],
            },
        ],
    },
}
