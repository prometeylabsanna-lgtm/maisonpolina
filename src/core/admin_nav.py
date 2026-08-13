"""Unfold SIDEBAR navigation — reverse_lazy, request-safe."""

from django.urls import reverse_lazy


def _link(name: str):
    return reverse_lazy(name)


def build_admin_navigation(_request=None):
    return [
        {
            "title": "Содержимое страниц",
            "separator": True,
            "items": [
                {
                    "title": "Шапка профиля",
                    "icon": "web_asset",
                    "link": _link("admin:core_siteheadersettings_changelist"),
                },
                {
                    "title": "Баннер",
                    "icon": "image",
                    "link": _link("admin:core_homeherosettings_changelist"),
                },
            ],
        },
        {
            "title": "Обо мне",
            "collapsible": False,
            "items": [
                {
                    "title": "Восемь лет ярких впечатлений",
                    "icon": "person",
                    "link": _link("admin:core_homeaboutsettings_changelist"),
                },
                {
                    "title": "Дополнительная информация",
                    "icon": "badge",
                    "link": _link("admin:core_homepersonalitysettings_changelist"),
                },
            ],
        },
        {
            "items": [
                {
                    "title": "Галерея",
                    "icon": "photo_library",
                    "link": _link("admin:core_homegallerysettings_changelist"),
                },
                {
                    "title": "Услуги",
                    "icon": "view_agenda",
                    "link": _link("admin:core_homeformatssettings_changelist"),
                },
                {
                    "title": "Отзывы",
                    "icon": "format_quote",
                    "link": _link("admin:core_hometestimonialssettings_changelist"),
                },
                {
                    "title": "Вопросы",
                    "icon": "help",
                    "link": _link("admin:core_homefaqsettings_changelist"),
                },
                {
                    "title": "Заявка",
                    "icon": "mail",
                    "link": _link("admin:core_homecontactssettings_changelist"),
                },
                {
                    "title": "Подвал",
                    "icon": "horizontal_rule",
                    "link": _link("admin:core_sitefootersettings_changelist"),
                },
                {
                    "title": "Политика конфиденциальности",
                    "icon": "policy",
                    "link": _link("admin:core_privacysettings_changelist"),
                },
            ],
        },
        {
            "title": "Заявки и чат",
            "separator": True,
            "items": [
                {
                    "title": "Все заявки",
                    "icon": "inbox",
                    "link": _link("admin:leads_lead_changelist"),
                },
                {
                    "title": "Чаты Telegram",
                    "icon": "forum",
                    "link": _link("admin:chat_telegramchatsession_changelist"),
                },
            ],
        },
        {
            "title": "Настройки",
            "separator": True,
            "items": [
                {
                    "title": "Сайт",
                    "icon": "settings",
                    "link": _link("admin:core_sitesettings_changelist"),
                },
                {
                    "title": "SEO",
                    "icon": "travel_explore",
                    "link": _link("admin:core_seometa_changelist"),
                },
                {
                    "title": "Цвета и кнопки",
                    "icon": "palette",
                    "link": _link("admin:core_themestylessettings_changelist"),
                },
                {
                    "title": "Чат (тексты)",
                    "icon": "chat",
                    "link": _link("admin:core_sitechatsettings_changelist"),
                },
                {
                    "title": "Ошибки",
                    "icon": "error",
                    "link": _link("admin:core_siteerrorssettings_changelist"),
                },
                {
                    "title": "Смена пароля",
                    "icon": "lock",
                    "link": _link("admin:password_change"),
                },
            ],
        },
    ]
