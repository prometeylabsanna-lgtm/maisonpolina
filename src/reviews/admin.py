from django.contrib import admin
from unfold.admin import ModelAdmin

from src.core.admin_tinymce import TinyMCEAdminMixin
from src.core.admin_utils import image_preview
from src.reviews.models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(TinyMCEAdminMixin, ModelAdmin):
    list_display = (
        "get_photo_preview",
        "author_name_ru",
        "author_name_en",
        "rating",
        "is_active",
        "is_public_submission",
        "order",
        "created_at",
    )
    list_editable = ("is_active", "order", "rating")
    list_filter = ("is_active", "is_public_submission", "rating")
    search_fields = ("author_name_ru", "author_name_en", "text_ru", "text_en")
    ordering_field = "order"
    readonly_fields = ("created_at", "is_public_submission", "get_photo_preview")
    tinymce_fields = ("text_ru", "text_en")
    fieldsets = (
        (
            "Загальне",
            {
                "fields": (
                    "photo",
                    "get_photo_preview",
                    "rating",
                    "order",
                    "is_active",
                )
            },
        ),
        (
            "Русский",
            {
                "classes": ["tab"],
                "fields": ("author_name_ru", "role_ru", "text_ru"),
            },
        ),
        (
            "English",
            {
                "classes": ["tab"],
                "fields": ("author_name_en", "role_en", "text_en"),
            },
        ),
        (
            "Службове",
            {
                "classes": ("collapse",),
                "fields": ("is_public_submission", "created_at"),
            },
        ),
    )

    @admin.display(description="Фото")
    def get_photo_preview(self, obj):
        return image_preview(getattr(obj, "photo", None), size=56)
