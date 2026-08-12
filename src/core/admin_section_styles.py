"""Admin screen for per-section styles (sidebar «Стили»)."""

from __future__ import annotations

from django import forms
from django.contrib import admin, messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from unfold.admin import ModelAdmin

from src.core.fill_style import FillType, fill_field_names
from src.core.models import SectionStyle, SiteSettings, ThemeStylesSettings
from src.core.section_styles import invalidate_section_styles_cache
from src.core.style_defaults import (
    SECTION_STYLE_DEFAULTS,
    ensure_section_styles,
    reset_section_style,
)


HEX_WIDGET = forms.TextInput(
    attrs={
        "placeholder": "#4c0d13",
        "class": "cms-hex-input",
        "pattern": "#[0-9A-Fa-f]{3}([0-9A-Fa-f]{3})?",
        "autocomplete": "off",
    }
)
FILL_TYPE_CHOICES = [("", "— как на сайте сейчас —"), *FillType.choices]

# Group titles on the styles page (non-technical Russian)
FILL_GROUP_META = {
    "bg": {
        "title": "Фон блока",
        "hint": "Цвет или градиент фона этой секции на сайте.",
    },
    "btn_primary": {
        "title": "Главная кнопка",
        "hint": "Основная кнопка действия в секции (яркая).",
    },
    "btn_secondary": {
        "title": "Вторая кнопка",
        "hint": "Дополнительная кнопка рядом с главной.",
    },
    "btn_header": {
        "title": "Кнопка в шапке",
        "hint": "Кнопка заявки в верхнем меню. Только для блока «Шапка».",
    },
}


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
            "bg_fill_type": forms.Select(choices=FILL_TYPE_CHOICES),
            "btn_primary_fill_type": forms.Select(choices=FILL_TYPE_CHOICES),
            "btn_secondary_fill_type": forms.Select(choices=FILL_TYPE_CHOICES),
            "btn_header_fill_type": forms.Select(choices=FILL_TYPE_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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


def _section_forms(request: HttpRequest) -> list[tuple[SectionStyle, SectionStyleForm]]:
    ensure_section_styles()
    order = list(SECTION_STYLE_DEFAULTS.keys())
    styles = {
        s.section: s
        for s in SectionStyle.objects.filter(section__in=order)
    }
    result = []
    for section in order:
        obj = styles[section]
        prefix = f"style_{section}"
        if request.method == "POST":
            form = SectionStyleForm(request.POST, instance=obj, prefix=prefix)
        else:
            form = SectionStyleForm(instance=obj, prefix=prefix)
        result.append((obj, form))
    return result


def site_styles_view(
    request: HttpRequest,
    model_admin: ModelAdmin | None = None,
) -> HttpResponse:
    ensure_section_styles()

    if request.method == "POST":
        reset_key = (request.POST.get("reset_section") or "").strip()
        if reset_key:
            obj = reset_section_style(reset_key)
            if obj is None:
                messages.error(request, "Секция не найдена")
            else:
                invalidate_section_styles_cache()
                messages.success(
                    request,
                    f"«{obj.get_section_display()}» — возвращены цвета по умолчанию.",
                )
            return HttpResponseRedirect(request.path)

    pairs = _section_forms(request)
    if request.method == "POST":
        if all(form.is_valid() for _, form in pairs):
            for _, form in pairs:
                form.save()
            invalidate_section_styles_cache()
            messages.success(request, "Стили сохранены")
            return HttpResponseRedirect(request.path)
        messages.error(request, "Проверьте поля — есть ошибки")

    context = {
        **(model_admin.admin_site.each_context(request) if model_admin else {}),
        "title": "Цвета и кнопки на сайте",
        "page_hint": (
            "Пустые поля оставляют обычный вид сайта. "
            "«Вернуть дефолт» в секции восстанавливает фирменные цвета. "
            "Кнопку в верхнем меню настраивайте только в блоке «Шапка»."
        ),
        "pairs": pairs,
        "fill_groups": FILL_GROUP_META,
        "header_section": SectionStyle.Section.HEADER,
        "opts": model_admin.model._meta if model_admin else None,
    }
    return render(request, "admin/site_styles_page.html", context)


class ThemeStylesAdmin(ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        SiteSettings.objects.get_or_create(pk=1)
        return HttpResponseRedirect(
            reverse("admin:core_themestylessettings_change", args=[1])
        )

    def change_view(self, request, object_id, form_url="", extra_context=None):
        return site_styles_view(request, model_admin=self)


def register_theme_styles_admin():
    try:
        admin.site.register(ThemeStylesSettings, ThemeStylesAdmin)
    except admin.sites.AlreadyRegistered:
        pass
