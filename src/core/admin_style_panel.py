"""Compact style panel form + helpers for CMS section pages."""

from __future__ import annotations

from django import forms
from django.http import HttpRequest

from src.core.fill_style import FillType, fill_field_names
from src.core.models import SectionStyle
from src.core.section_styles import invalidate_section_styles_cache
from src.core.site_content_types import ContentSection
from src.core.style_defaults import ensure_section_styles, reset_section_style

HEX_WIDGET = forms.TextInput(
    attrs={
        "placeholder": "#4c0d13",
        "class": "cms-hex-input",
        "pattern": "#[0-9A-Fa-f]{3}([0-9A-Fa-f]{3})?",
        "autocomplete": "off",
        "spellcheck": "false",
    }
)
FILL_TYPE_CHOICES = [("", "Сайт"), *FillType.choices]
ANGLE_WIDGET = forms.NumberInput(
    attrs={
        "class": "cms-style-angle",
        "min": "0",
        "max": "360",
        "inputmode": "numeric",
    }
)


class SectionStyleForm(forms.ModelForm):
    class Meta:
        model = SectionStyle
        fields = (
            "label",
            *fill_field_names("bg"),
            *fill_field_names("btn_primary"),
            *fill_field_names("btn_secondary"),
            *fill_field_names("btn_header"),
        )
        widgets = {
            "bg_solid_color": HEX_WIDGET,
            "bg_gradient_start": HEX_WIDGET,
            "bg_gradient_end": HEX_WIDGET,
            "btn_primary_solid_color": HEX_WIDGET,
            "btn_primary_gradient_start": HEX_WIDGET,
            "btn_primary_gradient_end": HEX_WIDGET,
            "btn_secondary_solid_color": HEX_WIDGET,
            "btn_secondary_gradient_start": HEX_WIDGET,
            "btn_secondary_gradient_end": HEX_WIDGET,
            "btn_header_solid_color": HEX_WIDGET,
            "btn_header_gradient_start": HEX_WIDGET,
            "btn_header_gradient_end": HEX_WIDGET,
            "bg_fill_type": forms.Select(
                choices=FILL_TYPE_CHOICES, attrs={"class": "cms-style-select"}
            ),
            "btn_primary_fill_type": forms.Select(
                choices=FILL_TYPE_CHOICES, attrs={"class": "cms-style-select"}
            ),
            "btn_secondary_fill_type": forms.Select(
                choices=FILL_TYPE_CHOICES, attrs={"class": "cms-style-select"}
            ),
            "btn_header_fill_type": forms.Select(
                choices=FILL_TYPE_CHOICES, attrs={"class": "cms-style-select"}
            ),
            "bg_gradient_angle": ANGLE_WIDGET,
            "btn_primary_gradient_angle": ANGLE_WIDGET,
            "btn_secondary_gradient_angle": ANGLE_WIDGET,
            "btn_header_gradient_angle": ANGLE_WIDGET,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
        section = getattr(self.instance, "section", "")
        if section == SectionStyle.Section.HEADER:
            for name in (
                *fill_field_names("btn_primary"),
                *fill_field_names("btn_secondary"),
            ):
                self.fields.pop(name, None)
        else:
            for name in fill_field_names("btn_header"):
                self.fields.pop(name, None)

    def clean(self):
        cleaned = super().clean()
        for prefix in ("bg", "btn_primary", "btn_secondary", "btn_header"):
            fill_name = f"{prefix}_fill_type"
            if fill_name not in self.fields:
                continue
            fill = (cleaned.get(fill_name) or "").strip()
            if fill:
                continue
            cleaned[f"{prefix}_solid_color"] = ""
            cleaned[f"{prefix}_gradient_start"] = ""
            cleaned[f"{prefix}_gradient_end"] = ""
        return cleaned


STYLE_PREFIX = "style"
STYLEABLE_SLUGS = frozenset(SectionStyle.Section.values)

_GROUP_SPEC = (
    ("bg", "Фон", "#4c0d13", "#4c0d13", "#3a0a0f"),
    ("btn_primary", "Кнопка", "#cab695", "#dfccb7", "#b09572"),
    ("btn_secondary", "Вторая кнопка", "#cab695", "#dfccb7", "#b09572"),
    ("btn_header", "Кнопка шапки", "#cab695", "#dfccb7", "#b09572"),
)


def _picker_hex(value: str, fallback: str) -> str:
    raw = (value or "").strip()
    if len(raw) == 7 and raw.startswith("#"):
        return raw
    if len(raw) == 4 and raw.startswith("#"):
        return f"#{raw[1] * 2}{raw[2] * 2}{raw[3] * 2}"
    return fallback


def style_key_for(section: ContentSection) -> str:
    return section.slug if section.slug in STYLEABLE_SLUGS else ""


def _style_posted(request: HttpRequest, prefix: str) -> bool:
    marker = f"{prefix}-"
    return any(key.startswith(marker) for key in request.POST)


def bind_style_form(
    request: HttpRequest,
    section: ContentSection,
    *,
    post: bool,
    prefix: str = STYLE_PREFIX,
):
    key = style_key_for(section)
    if not key:
        return None
    ensure_section_styles()
    obj = SectionStyle.objects.filter(section=key).first()
    if obj is None:
        return None
    if post:
        if not _style_posted(request, prefix):
            return None
        return SectionStyleForm(request.POST, instance=obj, prefix=prefix)
    return SectionStyleForm(instance=obj, prefix=prefix)


def save_style_form(form) -> None:
    if form is None:
        return
    form.save()
    invalidate_section_styles_cache()


def reset_posted_style(request: HttpRequest, section: ContentSection) -> bool:
    key = (request.POST.get("reset_section") or "").strip()
    expected = style_key_for(section)
    if not key or key != expected:
        return False
    obj = reset_section_style(key)
    if obj is not None:
        invalidate_section_styles_cache()
    return obj is not None


def build_style_groups(form) -> list[dict]:
    groups: list[dict] = []
    if form is None:
        return groups
    for key, title, d_solid, d_start, d_end in _GROUP_SPEC:
        fill_name = f"{key}_fill_type"
        if fill_name not in form.fields:
            continue
        fill_bound = form[fill_name]
        current = (fill_bound.value() or "").strip()
        solid = form[f"{key}_solid_color"]
        start = form[f"{key}_gradient_start"]
        end = form[f"{key}_gradient_end"]
        groups.append(
            {
                "key": key,
                "title": title,
                "mode": current,
                "fill_type": fill_bound,
                "solid": solid,
                "grad_start": start,
                "grad_end": end,
                "angle": form[f"{key}_gradient_angle"],
                "picker_solid": _picker_hex(solid.value(), d_solid),
                "picker_start": _picker_hex(start.value(), d_start),
                "picker_end": _picker_hex(end.value(), d_end),
                "default_solid": d_solid,
                "default_start": d_start,
                "default_end": d_end,
                "default_angle": "180",
            }
        )
    return groups
