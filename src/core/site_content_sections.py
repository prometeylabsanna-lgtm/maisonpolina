"""All CMS ContentSection definitions (split from helpers for file size)."""

from src.core.site_content_types import ContentSection, FieldGroup
from src.core.site_content_registry_2 import MORE_CONTENT_SECTIONS
from src.core.site_content_registry_3 import UI_CONTENT_SECTIONS

_HOME_SECTIONS: tuple[ContentSection, ...] = (
    ContentSection(
        slug="hero",
        page_slug="home",
        title="Hero",
        sidebar_title="Hero",
        sidebar_icon="image",
        preview_url="/",
        description="Имя, текст, кнопки и медиа первого экрана.",
        visibility_key="hero_section_visible",
        admin_model_name="homeherosettings",
        blocks=(
            ("home", "hero.title"),
            ("home", "hero.subtitle"),
            ("home", "hero.lead"),
            ("home", "hero.cta_primary"),
            ("home", "hero.cta_secondary"),
            ("home", "hero.tagline"),
            ("home", "hero.media"),
            ("home", "hero.media_layout"),
        ),
        field_groups=(
            FieldGroup("Тексты", ("hero.title", "hero.subtitle", "hero.lead", "hero.tagline")),
            FieldGroup("Кнопки", ("hero.cta_primary", "hero.cta_secondary")),
            FieldGroup("Медиа", ("hero.media_layout", "hero.media")),
        ),
    ),
    ContentSection(
        slug="about",
        page_slug="home",
        title="Обо мне",
        sidebar_title="Обо мне",
        sidebar_icon="person",
        preview_url="/#about",
        description="Заголовок, текст, статистика и портрет.",
        visibility_key="about_section_visible",
        admin_model_name="homeaboutsettings",
        blocks=(
            ("home", "about.eyebrow"),
            ("home", "about.title"),
            ("home", "about.title_accent"),
            ("home", "about.body_1"),
            ("home", "about.body_2"),
            ("home", "about.body_3"),
            ("home", "about.quote"),
            ("home", "about.stat_1_value"),
            ("home", "about.stat_1_label"),
            ("home", "about.stat_2_value"),
            ("home", "about.stat_2_label"),
            ("home", "about.stat_3_value"),
            ("home", "about.stat_3_label"),
            ("home", "about.cta"),
            ("home", "about.portrait"),
        ),
        field_groups=(
            FieldGroup("Заголовок", ("about.eyebrow", "about.title", "about.title_accent")),
            FieldGroup("Текст", ("about.body_1", "about.body_2", "about.body_3", "about.quote")),
            FieldGroup(
                "Статистика",
                (
                    "about.stat_1_value",
                    "about.stat_1_label",
                    "about.stat_2_value",
                    "about.stat_2_label",
                    "about.stat_3_value",
                    "about.stat_3_label",
                ),
            ),
            FieldGroup("Медиа и CTA", ("about.portrait", "about.cta")),
        ),
    ),
    ContentSection(
        slug="personality",
        page_slug="home",
        title="Личность",
        sidebar_title="Личность",
        sidebar_icon="badge",
        preview_url="/#personality",
        visibility_key="personality_section_visible",
        admin_model_name="homepersonalitysettings",
        has_personality_items=True,
        blocks=(
            ("home", "personality.eyebrow"),
            ("home", "personality.title"),
            ("home", "personality.title_accent"),
            ("home", "personality.facts_title"),
            ("home", "personality.languages"),
            ("home", "personality.respect"),
            ("home", "personality.education"),
            ("home", "personality.travel"),
            ("home", "personality.portrait"),
        ),
        field_groups=(
            FieldGroup(
                "Заголовок",
                ("personality.eyebrow", "personality.title", "personality.title_accent"),
            ),
            FieldGroup(
                "Внешность",
                ("personality.facts_title",),
            ),
            FieldGroup(
                "Дополнительно",
                (
                    "personality.portrait",
                    "personality.languages",
                    "personality.respect",
                    "personality.education",
                    "personality.travel",
                ),
            ),
        ),
    ),
)

CONTENT_SECTIONS: tuple[ContentSection, ...] = (
    _HOME_SECTIONS + MORE_CONTENT_SECTIONS + UI_CONTENT_SECTIONS
)
