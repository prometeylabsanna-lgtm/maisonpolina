from django import forms
from django.contrib import admin, messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.forms import modelformset_factory
from django.shortcuts import render
from django.urls import reverse
from unfold.admin import ModelAdmin

from src.core.admin_tinymce import (
    PLAIN_TEXTAREA_KEYS,
    RICH_TEXT_KEYS,
    cms_tinymce_widget,
)
from src.core.block_defaults import BLOCK_DEFAULTS
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
    SiteBlock,
    SiteChatSettings,
    SiteErrorsSettings,
    SiteFooterSettings,
    SiteHeaderSettings,
    SiteSettings,
    SiteUiSettings,
)
from src.core.services import invalidate_site_blocks_cache
from src.core.site_content_registry import CONTENT_SECTIONS, get_section
from src.gallery.models import GalleryPhoto

IMAGE_KEYS = {"hero.media", "about.portrait", "personality.portrait", "contacts.bg"}
MULTILINE_KEYS = RICH_TEXT_KEYS | PLAIN_TEXTAREA_KEYS


class GalleryPhotoForm(forms.ModelForm):
    class Meta:
        model = GalleryPhoto
        fields = (
            "static_image",
            "image",
            "alt_ru",
            "alt_en",
            "caption_ru",
            "caption_en",
            "col_span",
            "row_span",
            "order",
            "is_active",
        )
        widgets = {
            "static_image": forms.TextInput(attrs={"class": "cms-admin-input"}),
            "alt_ru": forms.TextInput(attrs={"class": "cms-admin-input"}),
            "alt_en": forms.TextInput(attrs={"class": "cms-admin-input"}),
            "caption_ru": forms.TextInput(attrs={"class": "cms-admin-input"}),
            "caption_en": forms.TextInput(attrs={"class": "cms-admin-input"}),
            "col_span": forms.NumberInput(attrs={"class": "cms-admin-input"}),
            "row_span": forms.NumberInput(attrs={"class": "cms-admin-input"}),
            "order": forms.NumberInput(attrs={"class": "cms-admin-input"}),
        }


GalleryPhotoFormSet = modelformset_factory(
    GalleryPhoto,
    form=GalleryPhotoForm,
    extra=1,
    can_delete=True,
)


def _ensure_blocks(section) -> dict[str, SiteBlock]:
    result = {}
    for page, key in section.blocks:
        defaults = BLOCK_DEFAULTS.get((page, key), {})
        block, _ = SiteBlock.objects.get_or_create(
            page=page,
            key=key,
            defaults={
                "label": defaults.get("label", key),
                "text_ru": defaults.get("text_ru", ""),
                "text_en": defaults.get("text_en", ""),
                "is_visible": defaults.get("is_visible", True),
            },
        )
        result[key] = block
    if section.visibility_key:
        page = section.page_slug
        defaults = BLOCK_DEFAULTS.get((page, section.visibility_key), {})
        block, _ = SiteBlock.objects.get_or_create(
            page=page,
            key=section.visibility_key,
            defaults={
                "label": defaults.get("label", section.visibility_key),
                "text_ru": "1",
                "text_en": "1",
                "is_visible": True,
            },
        )
        result[section.visibility_key] = block
    return result


def site_content_section_view(
    request: HttpRequest,
    page_slug: str,
    section_slug: str,
    model_admin: ModelAdmin | None = None,
) -> HttpResponse:
    section = get_section(page_slug, section_slug)
    if section is None:
        messages.error(request, "Секцію не знайдено")
        return HttpResponseRedirect(reverse("admin:index"))

    blocks = _ensure_blocks(section)
    gallery_formset = None

    if request.method == "POST":
        if section.visibility_key:
            vis = blocks[section.visibility_key]
            vis.is_visible = request.POST.get(f"block__{page_slug}__{section.visibility_key}__visible") == "on"
            vis.save(update_fields=["is_visible", "updated_at"])

        for page, key in section.blocks:
            block = blocks[key]
            prefix = f"block__{page}__{key}"
            if key in IMAGE_KEYS:
                if f"{prefix}__image" in request.FILES:
                    block.image = request.FILES[f"{prefix}__image"]
                if request.POST.get(f"{prefix}__clear_image") == "on":
                    block.image = ""
            else:
                block.text_ru = request.POST.get(f"{prefix}__ru", block.text_ru)
                block.text_en = request.POST.get(f"{prefix}__en", block.text_en)
            block.save()

        if section.has_gallery:
            gallery_formset = GalleryPhotoFormSet(
                request.POST,
                request.FILES,
                queryset=GalleryPhoto.objects.all().order_by("order", "pk"),
                prefix="gallery",
            )
            if gallery_formset.is_valid():
                instances = gallery_formset.save(commit=False)
                for obj in gallery_formset.deleted_objects:
                    obj.delete()
                for idx, obj in enumerate(instances):
                    if not obj.image and not obj.pk:
                        continue
                    if obj.order == 0:
                        obj.order = idx
                    obj.save()
                gallery_formset.save_m2m()
            else:
                messages.error(request, "Помилка у формі галереї")
                return _render_section(request, section, blocks, gallery_formset, model_admin)

        invalidate_site_blocks_cache()
        messages.success(request, "Збережено")
        return HttpResponseRedirect(request.path)

    if section.has_gallery:
        gallery_formset = GalleryPhotoFormSet(
            queryset=GalleryPhoto.objects.all().order_by("order", "pk"),
            prefix="gallery",
        )

    return _render_section(request, section, blocks, gallery_formset, model_admin)


def _render_section(request, section, blocks, gallery_formset, model_admin):
    rich_widgets: dict[str, dict[str, object]] = {}
    media = None
    for page, key in section.blocks:
        if key not in RICH_TEXT_KEYS:
            continue
        block = blocks.get(key)
        if not block:
            continue
        rich_widgets[key] = {}
        for lang in ("ru", "en"):
            name = f"block__{page}__{key}__{lang}"
            field_id = f"id_cms_{page}_{key}_{lang}".replace(".", "_")
            widget = cms_tinymce_widget(height=420 if key == "privacy.body" else 280)
            value = getattr(block, f"text_{lang}", "") or ""
            html = widget.render(name, value, attrs={"id": field_id})
            rich_widgets[key][lang] = html
            media = widget.media if media is None else media + widget.media

    context = {
        **(model_admin.admin_site.each_context(request) if model_admin else {}),
        "title": section.title,
        "section": section,
        "blocks": blocks,
        "image_keys": IMAGE_KEYS,
        "multiline_keys": MULTILINE_KEYS,
        "rich_text_keys": RICH_TEXT_KEYS,
        "rich_widgets": rich_widgets,
        "tinymce_media": media,
        "gallery_formset": gallery_formset,
        "opts": model_admin.model._meta if model_admin else None,
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


# Ensure registry is imported for side effects in admin.py
CONTENT_SECTIONS  # noqa: B018
