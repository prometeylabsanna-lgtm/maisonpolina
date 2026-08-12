from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from src.core.admin_changelist import TopDropdownFilterMixin
from src.core.admin_guidelines import AdminGuidelinesMixin
from src.core.admin_tinymce import TinyMCEAdminMixin
from src.core.admin_utils import ImagePreviewAdminMixin
from src.core.admin_webp import WebPAdminMixin
from src.formats.models import FormatFeature, ServiceFormat


class FormatFeatureInline(AdminGuidelinesMixin, TabularInline):
    model = FormatFeature
    extra = 1
    ordering_field = "order"
    hide_ordering_field = True
    fields = ("text_ru", "text_en", "order")
    tab = True
    guidelines_field_map = {
        "text_ru": "formats.feature",
        "text_en": "formats.feature",
    }


@admin.register(ServiceFormat)
class ServiceFormatAdmin(
    ImagePreviewAdminMixin,
    WebPAdminMixin,
    TopDropdownFilterMixin,
    AdminGuidelinesMixin,
    TinyMCEAdminMixin,
    ModelAdmin,
):
    guidelines_prefix = "formats"
    preview_attr = "image"
    list_display = (
        "get_photo_preview",
        "title_ru",
        "price_text_ru",
        "is_featured",
        "is_active",
        "order",
    )
    list_editable = ("is_active", "order", "is_featured")
    list_filter = ("is_active", "is_featured")
    search_fields = ("title_ru", "title_en")
    inlines = [FormatFeatureInline]
    ordering_field = "order"
    readonly_fields = ("get_photo_preview",)
    tinymce_fields = ("description_ru", "description_en")
    fieldsets = (
        (
            "Общее",
            {
                "fields": (
                    "image",
                    "get_photo_preview",
                    "is_featured",
                    "is_active",
                    "order",
                ),
                "description": (
                    "Фото карточки 1200×900 px (4:3, JPEG/WebP до 250 КБ), "
                    "показ на сайте и порядок в списке форматов."
                ),
            },
        ),
        (
            "Русский",
            {
                "classes": ["tab"],
                "fields": (
                    "title_ru",
                    "label_ru",
                    "description_ru",
                    "price_text_ru",
                ),
                "description": "Тексты формата на русском.",
            },
        ),
        (
            "English",
            {
                "classes": ["tab"],
                "fields": (
                    "title_en",
                    "label_en",
                    "description_en",
                    "price_text_en",
                ),
                "description": "Тексты формата на английском.",
            },
        ),
    )
