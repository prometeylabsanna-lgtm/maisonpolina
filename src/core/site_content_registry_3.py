"""CMS sections part 3 — UI chrome, chat, errors."""

from src.core.site_content_types import ContentSection, FieldGroup

UI_CONTENT_SECTIONS: tuple[ContentSection, ...] = (
    ContentSection(
        slug="chat",
        page_slug="site",
        title="Чат",
        sidebar_title="Чат",
        sidebar_icon="chat",
        preview_url="/",
        admin_model_name="sitechatsettings",
        blocks=(
            ("site", "chat.title"),
            ("site", "chat.subtitle"),
            ("site", "chat.open"),
            ("site", "chat.close"),
            ("site", "chat.panel_aria"),
            ("site", "chat.input_label"),
            ("site", "chat.placeholder"),
            ("site", "chat.send"),
            ("site", "chat.empty"),
            ("site", "chat.error_rate"),
            ("site", "chat.error_session"),
            ("site", "chat.error_send"),
        ),
        field_groups=(
            FieldGroup(
                "Заголовок и кнопки",
                (
                    "chat.title",
                    "chat.subtitle",
                    "chat.open",
                    "chat.close",
                    "chat.panel_aria",
                ),
            ),
            FieldGroup(
                "Поле ввода",
                ("chat.input_label", "chat.placeholder", "chat.send", "chat.empty"),
            ),
            FieldGroup(
                "Ошибки",
                ("chat.error_rate", "chat.error_session", "chat.error_send"),
            ),
        ),
    ),
    ContentSection(
        slug="errors",
        page_slug="site",
        title="Страницы ошибок",
        sidebar_title="Ошибки",
        sidebar_icon="error",
        preview_url="/",
        admin_model_name="siteerrorssettings",
        blocks=(
            ("site", "error.404_text"),
            ("site", "error.404_cta"),
            ("site", "error.500_text"),
            ("site", "error.500_cta"),
        ),
        field_groups=(
            FieldGroup("404", ("error.404_text", "error.404_cta")),
            FieldGroup("500", ("error.500_text", "error.500_cta")),
        ),
    ),
)
