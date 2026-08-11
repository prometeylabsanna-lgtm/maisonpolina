"""Default SectionStyle rows. Empty colors → tokens.css fallback."""

from src.core.models import SectionStyle

SECTION_STYLE_DEFAULTS: dict[str, str] = {
    SectionStyle.Section.HEADER: "Шапка",
    SectionStyle.Section.HERO: "Hero",
    SectionStyle.Section.ABOUT: "Про мене",
    SectionStyle.Section.PERSONALITY: "Особистість",
    SectionStyle.Section.GALLERY: "Галерея",
    SectionStyle.Section.FORMATS: "Формати",
    SectionStyle.Section.TESTIMONIALS: "Відгуки",
    SectionStyle.Section.FAQ: "Питання",
    SectionStyle.Section.CONTACTS: "Контакти",
    SectionStyle.Section.FOOTER: "Підвал",
}


def ensure_section_styles() -> int:
    created = 0
    for section, label in SECTION_STYLE_DEFAULTS.items():
        _, was_created = SectionStyle.objects.get_or_create(
            section=section,
            defaults={"label": label},
        )
        if was_created:
            created += 1
    return created
