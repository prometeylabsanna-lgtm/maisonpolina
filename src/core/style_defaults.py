"""Default SectionStyle rows and brand color presets for «Вернуть дефолт»."""

from __future__ import annotations

from src.core.fill_style import FillType
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

# Brand colors from tokens.css — shipped look before client edits.
_BG = {
    "bg_fill_type": FillType.SOLID,
    "bg_solid_color": "#4c0d13",
    "bg_gradient_start": "#4c0d13",
    "bg_gradient_end": "#3a0a0f",
    "bg_gradient_angle": 180,
}
_BTN_PRIMARY = {
    "btn_primary_fill_type": FillType.SOLID,
    "btn_primary_solid_color": "#cab695",
    "btn_primary_gradient_start": "#dfccb7",
    "btn_primary_gradient_end": "#b09572",
    "btn_primary_gradient_angle": 180,
}
_BTN_SECONDARY = {
    "btn_secondary_fill_type": FillType.SOLID,
    "btn_secondary_solid_color": "#cab695",
    "btn_secondary_gradient_start": "#dfccb7",
    "btn_secondary_gradient_end": "#b09572",
    "btn_secondary_gradient_angle": 180,
}
_BTN_HEADER = {
    "btn_header_fill_type": FillType.SOLID,
    "btn_header_solid_color": "#cab695",
    "btn_header_gradient_start": "#dfccb7",
    "btn_header_gradient_end": "#b09572",
    "btn_header_gradient_angle": 180,
}
_BTN_PRIMARY_EMPTY = {
    "btn_primary_fill_type": "",
    "btn_primary_solid_color": "",
    "btn_primary_gradient_start": "",
    "btn_primary_gradient_end": "",
    "btn_primary_gradient_angle": 180,
}
_BTN_SECONDARY_EMPTY = {
    "btn_secondary_fill_type": "",
    "btn_secondary_solid_color": "",
    "btn_secondary_gradient_start": "",
    "btn_secondary_gradient_end": "",
    "btn_secondary_gradient_angle": 180,
}
_BTN_HEADER_EMPTY = {
    "btn_header_fill_type": "",
    "btn_header_solid_color": "",
    "btn_header_gradient_start": "",
    "btn_header_gradient_end": "",
    "btn_header_gradient_angle": 180,
}


def _preset(*, header: bool) -> dict:
    data = {**_BG}
    if header:
        data.update(_BTN_HEADER)
        data.update(_BTN_PRIMARY_EMPTY)
        data.update(_BTN_SECONDARY_EMPTY)
    else:
        data.update(_BTN_PRIMARY)
        data.update(_BTN_SECONDARY)
        data.update(_BTN_HEADER_EMPTY)
    return data


SECTION_STYLE_PRESETS: dict[str, dict] = {
    section: _preset(header=(section == SectionStyle.Section.HEADER))
    for section in SECTION_STYLE_DEFAULTS
}

STYLE_COLOR_FIELDS: tuple[str, ...] = (
    "bg_fill_type",
    "bg_solid_color",
    "bg_gradient_start",
    "bg_gradient_end",
    "bg_gradient_angle",
    "btn_primary_fill_type",
    "btn_primary_solid_color",
    "btn_primary_gradient_start",
    "btn_primary_gradient_end",
    "btn_primary_gradient_angle",
    "btn_secondary_fill_type",
    "btn_secondary_solid_color",
    "btn_secondary_gradient_start",
    "btn_secondary_gradient_end",
    "btn_secondary_gradient_angle",
    "btn_header_fill_type",
    "btn_header_solid_color",
    "btn_header_gradient_start",
    "btn_header_gradient_end",
    "btn_header_gradient_angle",
)


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


def reset_section_style(section: str) -> SectionStyle | None:
    """Apply brand preset colors for one section. Returns updated row or None."""
    preset = SECTION_STYLE_PRESETS.get(section)
    if preset is None:
        return None
    ensure_section_styles()
    obj = SectionStyle.objects.filter(section=section).first()
    if obj is None:
        return None
    for field in STYLE_COLOR_FIELDS:
        setattr(obj, field, preset[field])
    obj.label = SECTION_STYLE_DEFAULTS[section]
    obj.save()
    return obj
