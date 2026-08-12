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
from src.core.models import (
    HomeAboutSettings,
    HomeContactsSettings,
    HomeFaqSettings,
    HomeFormatsSettings,
    HomeGallerySettings,
    HomeHeroSettings,
    HomePersonalitySettings,
    HomeTestimonialsSettings,
    PersonalityItem,
    PrivacySettings,
    SiteChatSettings,
    SiteErrorsSettings,
    SiteFooterSettings,
    SiteHeaderSettings,
    SiteSettings,
    SiteUiSettings,
)
from src.core.personality_forms import (
    PersonalityExtraFormSet,
    PersonalityFactFormSet,
    personality_item_queryset,
    save_personality_formset,
)
from src.core.site_content_registry import CONTENT_SECTIONS, get_section
from src.gallery.forms import GalleryPhotoFormSet
from src.gallery.models import GalleryPhoto


def _bind_gallery_formset(request: HttpRequest, *, post: bool):
    qs = GalleryPhoto.objects.all().order_by("order", "pk")
    if post:
        return GalleryPhotoFormSet(
            request.POST, request.FILES, queryset=qs, prefix="gallery"
        )
    return GalleryPhotoFormSet(queryset=qs, prefix="gallery")


def _bind_personality_formsets(request: HttpRequest, *, post: bool):
    facts_qs = personality_item_queryset(PersonalityItem.Group.FACTS)
    extras_qs = personality_item_queryset(PersonalityItem.Group.EXTRAS)
    if post:
        facts = PersonalityFactFormSet(
            request.POST, queryset=facts_qs, prefix="personality_facts"
        )
        extras = PersonalityExtraFormSet(
            request.POST, queryset=extras_qs, prefix="personality_extras"
        )
    else:
        facts = PersonalityFactFormSet(queryset=facts_qs, prefix="personality_facts")
        extras = PersonalityExtraFormSet(queryset=extras_qs, prefix="personality_extras")
    return facts, extras


def _save_gallery_formset(gallery_formset) -> None:
    instances = gallery_formset.save(commit=False)
    for obj in gallery_formset.deleted_objects:
        obj.delete()
    for idx, obj in enumerate(instances):
        if not obj.image and not obj.pk and not getattr(obj, "static_image", ""):
            continue
        if obj.order == 0:
            obj.order = idx
        obj.save()
    gallery_formset.save_m2m()


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
    gallery_formset = None
    personality_facts_formset = None
    personality_extras_formset = None

    if request.method == "POST":
        form = SitePageContentForm(section, blocks, request.POST, request.FILES)
        forms_ok = form.is_valid()
        if section.has_gallery:
            gallery_formset = _bind_gallery_formset(request, post=True)
            forms_ok = forms_ok and gallery_formset.is_valid()
        if section.has_personality_items:
            personality_facts_formset, personality_extras_formset = (
                _bind_personality_formsets(request, post=True)
            )
            forms_ok = (
                forms_ok
                and personality_facts_formset.is_valid()
                and personality_extras_formset.is_valid()
            )

        if forms_ok:
            form.save()
            if gallery_formset is not None:
                _save_gallery_formset(gallery_formset)
            if personality_facts_formset is not None:
                save_personality_formset(
                    personality_facts_formset, PersonalityItem.Group.FACTS
                )
            if personality_extras_formset is not None:
                save_personality_formset(
                    personality_extras_formset, PersonalityItem.Group.EXTRAS
                )
            title = section.sidebar_title or section.title
            messages.success(request, f"«{title}» сохранено.")
            return HttpResponseRedirect(request.path)

        messages.error(request, "Проверьте форму — есть ошибки.")
    else:
        form = SitePageContentForm(section, blocks)
        if section.has_gallery:
            gallery_formset = _bind_gallery_formset(request, post=False)
        if section.has_personality_items:
            personality_facts_formset, personality_extras_formset = (
                _bind_personality_formsets(request, post=False)
            )

    media = form.media
    if gallery_formset is not None:
        media = media + gallery_formset.media
    if personality_facts_formset is not None:
        media = media + personality_facts_formset.media
    if personality_extras_formset is not None:
        media = media + personality_extras_formset.media

    context = {
        **(model_admin.admin_site.each_context(request) if model_admin else {}),
        "title": section.sidebar_title or section.title,
        "section": section,
        "form": form,
        "fieldsets": build_section_fieldsets(form, section),
        "gallery_formset": gallery_formset,
        "personality_facts_formset": personality_facts_formset,
        "personality_extras_formset": personality_extras_formset,
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
        (SiteUiSettings, "site", "ui"),
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
