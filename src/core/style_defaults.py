"""Default SectionStyle rows. Empty colors → site defaults."""

from src.core.models import SectionStyle

SECTION_STYLE_DEFAULTS: dict[str, str] = {
    SectionStyle.Section.HEADER: "Шапка",
    SectionStyle.Section.HERO: "Первый экран (Hero)",
    SectionStyle.Section.ABOUT: "Обо мне",
    SectionStyle.Section.PERSONALITY: "Личность",
    SectionStyle.Section.GALLERY: "Галерея",
    SectionStyle.Section.FORMATS: "Форматы",
    SectionStyle.Section.TESTIMONIALS: "Отзывы",
    SectionStyle.Section.FAQ: "Вопросы",
    SectionStyle.Section.CONTACTS: "Контакты",
    SectionStyle.Section.FOOTER: "Подвал",
}


def ensure_section_styles() -> int:
    created = 0
    for section, label in SECTION_STYLE_DEFAULTS.items():
        obj, was_created = SectionStyle.objects.get_or_create(
            section=section,
            defaults={"label": label},
        )
        if was_created:
            created += 1
        elif obj.label != label:
            obj.label = label
            obj.save(update_fields=["label"])
    return created
