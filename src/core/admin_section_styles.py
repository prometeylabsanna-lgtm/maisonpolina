"""Admin screen for per-section styles (sidebar «Цвета и кнопки»)."""

from __future__ import annotations

from django.contrib import admin, messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from unfold.admin import ModelAdmin

from src.core.admin_style_panel import SectionStyleForm, build_style_groups
from src.core.models import SectionStyle, SiteSettings, ThemeStylesSettings
from src.core.section_styles import invalidate_section_styles_cache
from src.core.style_defaults import (
    SECTION_STYLE_DEFAULTS,
    ensure_section_styles,
    reset_section_style,
)


def _section_forms(request: HttpRequest) -> list[tuple[SectionStyle, SectionStyleForm, list]]:
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
        result.append((obj, form, build_style_groups(form)))
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

    triples = _section_forms(request)
    if request.method == "POST":
        if all(form.is_valid() for _, form, _ in triples):
            for _, form, _ in triples:
                form.save()
            invalidate_section_styles_cache()
            messages.success(request, "Стили сохранены")
            return HttpResponseRedirect(request.path)
        messages.error(request, "Проверьте поля — есть ошибки")

    context = {
        **(model_admin.admin_site.each_context(request) if model_admin else {}),
        "title": "Цвета и кнопки на сайте",
        "page_hint": (
            "Цвета также можно менять внутри каждого блока. "
            "Пустые поля оставляют обычный вид сайта."
        ),
        "triples": triples,
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
