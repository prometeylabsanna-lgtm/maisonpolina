"""CMS section editors: Form + fieldsets (Oyra-style), bilingual RU/EN."""

from __future__ import annotations

from django import forms
from django.contrib import admin, messages
from django.forms import modelformset_factory
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from unfold.admin import ModelAdmin
from unfold.widgets import UnfoldAdminFileFieldWidget, UnfoldBooleanWidget

from src.core.admin_site_content_widgets import (
    CmsAdminTextInputWidget,
    CmsAdminTextareaWidget,
)
from src.core.admin_tinymce import (
    PLAIN_TEXTAREA_KEYS,
    RICH_TEXT_KEYS,
    cms_tinymce_widget,
)
from src.core.block_defaults import (
    BLOCK_CONTENT_TYPES,
    BLOCK_DEFAULTS,
    IMAGE_KEYS,
    get_block_field_label,
    is_visibility_key,
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
    SiteBlock,
    SiteChatSettings,
    SiteErrorsSettings,
    SiteFooterSettings,
    SiteHeaderSettings,
    SiteSettings,
    SiteUiSettings,
)
from src.core.services import invalidate_site_blocks_cache
from src.core.site_content_registry import (
    CONTENT_SECTIONS,
    ContentSection,
    get_section,
    iter_section_blocks,
)
from src.gallery.models import GalleryPhoto

SECTION_VISIBLE_FIELD = "section_visible"


class GalleryPhotoForm(forms.ModelForm):
    class Meta:
        model = GalleryPhoto
        fields = (
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
        labels = {
            "image": "Изображение",
            "alt_ru": "Alt (RU)",
            "alt_en": "Alt (EN)",
            "caption_ru": "Подпись (RU)",
            "caption_en": "Подпись (EN)",
            "col_span": "Ширина (col)",
            "row_span": "Высота (row)",
            "order": "Порядок",
            "is_active": "Активно",
        }
        widgets = {
            "alt_ru": CmsAdminTextInputWidget(),
            "alt_en": CmsAdminTextInputWidget(),
            "caption_ru": CmsAdminTextInputWidget(),
            "caption_en": CmsAdminTextInputWidget(),
            "col_span": forms.NumberInput(attrs={"class": "cms-admin-input"}),
            "row_span": forms.NumberInput(attrs={"class": "cms-admin-input"}),
            "order": forms.NumberInput(attrs={"class": "cms-admin-input"}),
            "is_active": UnfoldBooleanWidget(),
            "image": UnfoldAdminFileFieldWidget(),
        }


GalleryPhotoFormSet = modelformset_factory(
    GalleryPhoto,
    form=GalleryPhotoForm,
    extra=1,
    can_delete=True,
)


def block_field_name(page: str, key: str, suffix: str) -> str:
    return f"block__{page}__{key}__{suffix}"


def _content_type(page: str, key: str) -> str:
    return BLOCK_CONTENT_TYPES.get((page, key), SiteBlock.ContentType.TEXT)


def load_section_blocks(section: ContentSection) -> dict[tuple[str, str], SiteBlock]:
    blocks: dict[tuple[str, str], SiteBlock] = {}
    for page, key in iter_section_blocks(section):
        defaults = BLOCK_DEFAULTS.get((page, key), {})
        block, _created = SiteBlock.objects.get_or_create(
            page=page,
            key=key,
            defaults={
                "label": get_block_field_label(page, key),
                "content_type": _content_type(page, key),
                "text_ru": defaults.get("text_ru", "1" if is_visibility_key(key) else ""),
                "text_en": defaults.get("text_en", "1" if is_visibility_key(key) else ""),
                "sort_order": 0,
                "is_active": True,
            },
        )
        blocks[(page, key)] = block
    return blocks


class SitePageContentForm(forms.Form):
    def __init__(
        self,
        section: ContentSection,
        blocks: dict[tuple[str, str], SiteBlock],
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.section = section
        self.blocks = blocks

        if section.visibility_key:
            page, key = self._visibility_page_key(section)
            block = blocks[(page, key)]
            self.fields[SECTION_VISIBLE_FIELD] = forms.BooleanField(
                label="Показывать секцию на сайте",
                required=False,
                initial=block.visibility_on(),
                widget=UnfoldBooleanWidget(),
            )

        for page, key in section.blocks:
            self._add_block_fields(blocks[(page, key)])

    def _visibility_page_key(self, section: ContentSection) -> tuple[str, str]:
        for page, key in iter_section_blocks(section):
            if key == section.visibility_key:
                return page, key
        raise KeyError(section.visibility_key)

    def _add_block_fields(self, block: SiteBlock) -> None:
        page, key = block.page, block.key
        label = block.label or get_block_field_label(page, key)

        if block.content_type == SiteBlock.ContentType.IMAGE or key in IMAGE_KEYS:
            self.fields[block_field_name(page, key, "image")] = forms.ImageField(
                label=label,
                required=False,
                widget=UnfoldAdminFileFieldWidget(),
                help_text=f"Текущее: {block.image.name}" if block.image else "",
            )
            self.fields[block_field_name(page, key, "clear_image")] = forms.BooleanField(
                label="Удалить изображение",
                required=False,
                widget=UnfoldBooleanWidget(),
            )
            return

        if key in RICH_TEXT_KEYS:
            widget_ru = cms_tinymce_widget(height=420 if key == "privacy.body" else 280)
            widget_en = cms_tinymce_widget(height=420 if key == "privacy.body" else 280)
        elif key in PLAIN_TEXTAREA_KEYS:
            widget_ru = CmsAdminTextareaWidget(attrs={"rows": 4})
            widget_en = CmsAdminTextareaWidget(attrs={"rows": 4})
        else:
            widget_ru = CmsAdminTextInputWidget()
            widget_en = CmsAdminTextInputWidget()

        self.fields[block_field_name(page, key, "ru")] = forms.CharField(
            label=f"{label} (RU)",
            initial=block.text_ru,
            required=False,
            widget=widget_ru,
        )
        self.fields[block_field_name(page, key, "en")] = forms.CharField(
            label=f"{label} (EN)",
            initial=block.text_en,
            required=False,
            widget=widget_en,
        )

    def save(self) -> None:
        if SECTION_VISIBLE_FIELD in self.fields:
            page, key = self._visibility_page_key(self.section)
            block = self.blocks[(page, key)]
            on = bool(self.cleaned_data.get(SECTION_VISIBLE_FIELD))
            block.text_ru = "1" if on else "0"
            block.text_en = block.text_ru
            block.is_active = True
            block.content_type = SiteBlock.ContentType.TEXT
            block.save()

        for block in self.blocks.values():
            page, key = block.page, block.key
            if key == self.section.visibility_key:
                continue

            block.is_active = True
            if block.content_type == SiteBlock.ContentType.IMAGE or key in IMAGE_KEYS:
                block.content_type = SiteBlock.ContentType.IMAGE
                if self.cleaned_data.get(block_field_name(page, key, "clear_image")):
                    block.image = ""
                uploaded = self.cleaned_data.get(block_field_name(page, key, "image"))
                if uploaded:
                    block.image = uploaded
            else:
                block.content_type = SiteBlock.ContentType.TEXT
                block.text_ru = (
                    self.cleaned_data.get(block_field_name(page, key, "ru"), "") or ""
                ).strip()
                block.text_en = (
                    self.cleaned_data.get(block_field_name(page, key, "en"), "") or ""
                ).strip()
            block.save()

        invalidate_site_blocks_cache()


def _block_rows_for_keys(
    form: SitePageContentForm,
    section: ContentSection,
    keys: tuple[str, ...],
) -> list[dict]:
    page_keys = {key: page for page, key in section.blocks}
    rows: list[dict] = []
    for key in keys:
        page = page_keys.get(key)
        if page is None:
            continue
        block = form.blocks.get((page, key))
        if block is None:
            continue
        is_image = (
            block.content_type == SiteBlock.ContentType.IMAGE or key in IMAGE_KEYS
        )
        if is_image:
            image_name = block_field_name(page, key, "image")
            clear_name = block_field_name(page, key, "clear_image")
            rows.append(
                {
                    "key": key,
                    "label": block.label or key,
                    "is_image": True,
                    "image": form[image_name] if image_name in form.fields else None,
                    "clear_image": (
                        form[clear_name] if clear_name in form.fields else None
                    ),
                    "block": block,
                }
            )
            continue
        ru_name = block_field_name(page, key, "ru")
        en_name = block_field_name(page, key, "en")
        rows.append(
            {
                "key": key,
                "label": block.label or key,
                "is_image": False,
                "ru": form[ru_name] if ru_name in form.fields else None,
                "en": form[en_name] if en_name in form.fields else None,
            }
        )
    return rows


def build_section_fieldsets(
    form: SitePageContentForm,
    section: ContentSection,
) -> list[tuple[str, list]]:
    fieldsets: list[tuple[str, list]] = []
    if SECTION_VISIBLE_FIELD in form.fields:
        fieldsets.append(
            (
                "Видимость",
                [{"kind": "visibility", "field": form[SECTION_VISIBLE_FIELD]}],
            )
        )
    if section.field_groups:
        for group in section.field_groups:
            rows = _block_rows_for_keys(form, section, group.keys)
            if rows:
                fieldsets.append((group.title, rows))
    elif section.blocks:
        keys = tuple(key for _page, key in section.blocks)
        rows = _block_rows_for_keys(form, section, keys)
        if rows:
            fieldsets.append(("", rows))
    return fieldsets


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

    if request.method == "POST":
        form = SitePageContentForm(section, blocks, request.POST, request.FILES)
        forms_ok = form.is_valid()
        if section.has_gallery:
            gallery_formset = GalleryPhotoFormSet(
                request.POST,
                request.FILES,
                queryset=GalleryPhoto.objects.all().order_by("order", "pk"),
                prefix="gallery",
            )
            forms_ok = forms_ok and gallery_formset.is_valid()

        if forms_ok:
            form.save()
            if gallery_formset is not None:
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
            title = section.sidebar_title or section.title
            messages.success(request, f"«{title}» сохранено.")
            return HttpResponseRedirect(request.path)

        messages.error(request, "Проверьте форму — есть ошибки.")
    else:
        form = SitePageContentForm(section, blocks)
        if section.has_gallery:
            gallery_formset = GalleryPhotoFormSet(
                queryset=GalleryPhoto.objects.all().order_by("order", "pk"),
                prefix="gallery",
            )

    media = form.media
    if gallery_formset is not None:
        media = media + gallery_formset.media

    context = {
        **(model_admin.admin_site.each_context(request) if model_admin else {}),
        "title": section.sidebar_title or section.title,
        "section": section,
        "form": form,
        "fieldsets": build_section_fieldsets(form, section),
        "gallery_formset": gallery_formset,
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
