from dataclasses import dataclass, field


@dataclass(frozen=True)
class FieldGroup:
    title: str
    keys: tuple[str, ...]


@dataclass(frozen=True)
class ContentSection:
    slug: str
    page_slug: str
    title: str
    blocks: tuple[tuple[str, str], ...]
    sidebar_title: str = ""
    sidebar_icon: str = "edit_note"
    preview_url: str = "/"
    description: str = ""
    visibility_key: str = ""
    field_groups: tuple[FieldGroup, ...] = field(default_factory=tuple)
    admin_model_name: str = ""
    has_gallery: bool = False


CONTENT_SECTIONS: tuple[ContentSection, ...] = (
    ContentSection(
        slug="hero",
        page_slug="home",
        title="Hero",
        sidebar_title="Hero",
        sidebar_icon="image",
        preview_url="/",
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
        ),
        field_groups=(
            FieldGroup("Тексти", ("hero.title", "hero.subtitle", "hero.lead", "hero.tagline")),
            FieldGroup("Кнопки", ("hero.cta_primary", "hero.cta_secondary")),
            FieldGroup("Медіа", ("hero.media",)),
        ),
    ),
    ContentSection(
        slug="about",
        page_slug="home",
        title="Про мене",
        sidebar_title="Про мене",
        sidebar_icon="person",
        preview_url="/#about",
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
    ),
    ContentSection(
        slug="gallery",
        page_slug="home",
        title="Галерея",
        sidebar_title="Галерея",
        sidebar_icon="photo_library",
        preview_url="/#gallery",
        visibility_key="gallery_section_visible",
        admin_model_name="homegallerysettings",
        has_gallery=True,
        blocks=(
            ("home", "gallery.eyebrow"),
            ("home", "gallery.title"),
            ("home", "gallery.title_accent"),
        ),
    ),
    ContentSection(
        slug="formats",
        page_slug="home",
        title="Формати",
        sidebar_title="Формати",
        sidebar_icon="view_agenda",
        preview_url="/#services",
        visibility_key="formats_section_visible",
        admin_model_name="homeformatssettings",
        blocks=(
            ("home", "formats.eyebrow"),
            ("home", "formats.title"),
            ("home", "formats.title_accent"),
            ("home", "formats.note"),
        ),
    ),
    ContentSection(
        slug="testimonials",
        page_slug="home",
        title="Відгуки",
        sidebar_title="Відгуки",
        sidebar_icon="format_quote",
        preview_url="/#reviews",
        visibility_key="testimonials_section_visible",
        admin_model_name="hometestimonialssettings",
        blocks=(("home", "testimonials.eyebrow"),),
    ),
    ContentSection(
        slug="faq",
        page_slug="home",
        title="Питання",
        sidebar_title="Питання",
        sidebar_icon="help",
        preview_url="/#faq",
        visibility_key="faq_section_visible",
        admin_model_name="homefaqsettings",
        blocks=(
            ("home", "faq.eyebrow"),
            ("home", "faq.title"),
            ("home", "faq.title_accent"),
            ("home", "faq.cta"),
        ),
    ),
    ContentSection(
        slug="contacts",
        page_slug="home",
        title="Контакти",
        sidebar_title="Контакти",
        sidebar_icon="mail",
        preview_url="/#contact",
        visibility_key="contacts_section_visible",
        admin_model_name="homecontactssettings",
        blocks=(
            ("home", "contacts.eyebrow"),
            ("home", "contacts.title"),
            ("home", "contacts.title_accent"),
            ("home", "contacts.lead"),
            ("home", "contacts.privacy_note"),
        ),
    ),
    ContentSection(
        slug="privacy",
        page_slug="privacy",
        title="Політика конфіденційності",
        sidebar_title="Політика",
        sidebar_icon="policy",
        preview_url="/privacy/",
        admin_model_name="privacysettings",
        blocks=(
            ("privacy", "title"),
            ("privacy", "body"),
        ),
    ),
)


def get_section(page_slug: str, section_slug: str) -> ContentSection | None:
    for section in CONTENT_SECTIONS:
        if section.page_slug == page_slug and section.slug == section_slug:
            return section
    return None
