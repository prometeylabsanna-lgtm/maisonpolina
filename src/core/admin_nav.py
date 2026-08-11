"""Unfold SIDEBAR navigation — reverse_lazy, request-safe."""

from django.urls import reverse_lazy


def build_admin_navigation(_request=None):
    return [
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
                    "link": reverse_lazy("admin:core_homepersonalitysettings_changelist"),
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
                    "link": reverse_lazy(
                        "admin:core_hometestimonialssettings_changelist"
                    ),
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
                    "title": "Шапка",
                    "icon": "web_asset",
                    "link": reverse_lazy("admin:core_siteheadersettings_changelist"),
                },
                {
                    "title": "Підвал",
                    "icon": "horizontal_rule",
                    "link": reverse_lazy("admin:core_sitefootersettings_changelist"),
                },
                {
                    "title": "Інтерфейс",
                    "icon": "tune",
                    "link": reverse_lazy("admin:core_siteuisettings_changelist"),
                },
                {
                    "title": "Чат (тексти)",
                    "icon": "chat",
                    "link": reverse_lazy("admin:core_sitechatsettings_changelist"),
                },
                {
                    "title": "Помилки",
                    "icon": "error",
                    "link": reverse_lazy("admin:core_siteerrorssettings_changelist"),
                },
                {
                    "title": "Політика",
                    "icon": "policy",
                    "link": reverse_lazy("admin:core_privacysettings_changelist"),
                },
                {
                    "title": "Стилі",
                    "icon": "palette",
                    "link": reverse_lazy("admin:core_themestylessettings_changelist"),
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
            "title": "Заявки та чат",
            "separator": True,
            "items": [
                {
                    "title": "Усі заявки",
                    "icon": "inbox",
                    "link": reverse_lazy("admin:leads_lead_changelist"),
                },
                {
                    "title": "Чати Telegram",
                    "icon": "forum",
                    "link": reverse_lazy(
                        "admin:chat_telegramchatsession_changelist"
                    ),
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
    ]
