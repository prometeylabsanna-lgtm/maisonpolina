"""CMS section editors: proxy admins + section view."""

from __future__ import annotations

from django.contrib import admin, messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from unfold.admin import ModelAdmin

from src.core.admin_site_content_form import (
    SitePageContentForm,
    build_section_fieldsets,
    load_section_blocks,
)
from src.core.admin_site_content_lists import (
    bind_section_formsets,
    formsets_valid,
    save_section_formsets,
)
from src.core.admin_site_content_settings import build_settings_rows
from src.core.admin_style_panel import (
    bind_style_form,
    build_style_groups,
    reset_posted_style,
    save_style_form,
    style_key_for,
)
from src.core.models import (
    HomeAboutSettings,
    HomeContactsSettings,
    HomeFaqSettings,
    HomeFormatsSettings,
    HomeGallerySettings,
    HomeHeroSettings,
    HomePersonalitySettings,
    HomeTestimonialsSettings,
    PrivacySettings,
    SiteChatSettings,
    SiteErrorsSettings,
    SiteFooterSettings,
    SiteHeaderSettings,
    SiteSettings,
)
from src.core.site_content_registry import CONTENT_SECTIONS, get_section


def site_content_section_view(
    request: HttpRequest,
    page_slug: str,
    section_slug: str,
    model_admin: ModelAdmin | None = None,
) -> HttpResponse:
    section = get_section(page_slug, section_slug)
    if section is None:
        messages.error(request, "Секция не найдена")
        return HttpResponseRedirect(reverse("admin:index"))

    blocks = load_section_blocks(section)

    if request.method == "POST" and reset_posted_style(request, section):
        messages.success(request, "Цвета блока возвращены к фирменным.")
        return HttpResponseRedirect(request.path)

    if request.method == "POST":
        form = SitePageContentForm(section, blocks, request.POST, request.FILES)
        formsets = bind_section_formsets(request, section, post=True)
        style_form = bind_style_form(request, section, post=True)
        style_ok = style_form is None or style_form.is_valid()
        if form.is_valid() and formsets_valid(formsets) and style_ok:
            form.save()
            save_section_formsets(formsets)
            save_style_form(style_form)
            title = section.sidebar_title or section.title
            messages.success(request, f"«{title}» сохранено.")
            return HttpResponseRedirect(request.path)
        messages.error(request, "Проверьте форму — есть ошибки.")
    else:
        form = SitePageContentForm(section, blocks)
        formsets = bind_section_formsets(request, section, post=False)
        style_form = bind_style_form(request, section, post=False)

    media = form.media
    for formset in formsets.values():
        if formset is not None:
            media = media + formset.media

    context = {
        **(model_admin.admin_site.each_context(request) if model_admin else {}),
        "title": section.sidebar_title or section.title,
        "section": section,
        "form": form,
        "fieldsets": build_section_fieldsets(form, section),
        "settings_rows": build_settings_rows(form, section),
        "gallery_formset": formsets["gallery"],
        "personality_facts_formset": formsets["personality_facts"],
        "personality_extras_formset": formsets["personality_extras"],
        "formats_formset": formsets["formats"],
        "testimonials_formset": formsets["testimonials"],
        "faq_formset": formsets["faq"],
        "style_form": style_form,
        "style_groups": build_style_groups(style_form),
        "style_key": style_key_for(section),
        "preview_url": section.preview_url,
        "tinymce_media": media,
        "opts": model_admin.model._meta if model_admin else None,
        "has_view_permission": True,
        "add": False,
        "change": True,
        "is_popup": False,
        "save_as": False,
        "show_save": True,
        "show_save_and_continue": False,
        "show_save_and_add_another": False,
        "show_delete": False,
    }
    return render(request, "admin/site_content_page.html", context)


class SingletonSettingsAdmin(ModelAdmin):
    page_slug: str = ""
    section_slug: str = ""

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        SiteSettings.objects.get_or_create(pk=1)
        return HttpResponseRedirect(
            reverse(
                f"admin:core_{self.model._meta.model_name}_change",
                args=[1],
            )
        )

    def change_view(self, request, object_id, form_url="", extra_context=None):
        return site_content_section_view(
            request,
            self.page_slug,
            self.section_slug,
            model_admin=self,
        )


def register_site_content_section_admins():
    mapping = (
        (HomeHeroSettings, "home", "hero"),
        (HomeAboutSettings, "home", "about"),
        (HomePersonalitySettings, "home", "personality"),
        (HomeGallerySettings, "home", "gallery"),
        (HomeFormatsSettings, "home", "formats"),
        (HomeTestimonialsSettings, "home", "testimonials"),
        (HomeFaqSettings, "home", "faq"),
        (HomeContactsSettings, "home", "contacts"),
        (PrivacySettings, "privacy", "privacy"),
        (SiteHeaderSettings, "site", "header"),
        (SiteFooterSettings, "site", "footer"),
        (SiteChatSettings, "site", "chat"),
        (SiteErrorsSettings, "site", "errors"),
    )
    for model, page, slug in mapping:
        admin_cls = type(
            f"{model.__name__}Admin",
            (SingletonSettingsAdmin,),
            {"page_slug": page, "section_slug": slug},
        )
        try:
            admin.site.register(model, admin_cls)
        except admin.sites.AlreadyRegistered:
            pass


CONTENT_SECTIONS  # noqa: B018
