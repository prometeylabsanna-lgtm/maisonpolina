from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from src.core.admin_tinymce import TinyMCEAdminMixin
from src.formats.models import FormatFeature, ServiceFormat


class FormatFeatureInline(TabularInline):
    model = FormatFeature
    extra = 1
    ordering_field = "order"
    hide_ordering_field = True
    fields = ("text_ru", "text_en", "order")
    tab = True


@admin.register(ServiceFormat)
class ServiceFormatAdmin(TinyMCEAdminMixin, ModelAdmin):
    list_display = ("title_ru", "price_text_ru", "is_featured", "is_active", "order")
    list_editable = ("is_active", "order", "is_featured")
    list_filter = ("is_active", "is_featured")
    search_fields = ("title_ru", "title_en")
    inlines = [FormatFeatureInline]
    ordering_field = "order"
    tinymce_fields = ("description_ru", "description_en")
    fieldsets = (
        (
            "Общее",
            {
                "fields": ("is_featured", "is_active", "order"),
                "description": "Показ на сайте и порядок в списке форматов.",
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
