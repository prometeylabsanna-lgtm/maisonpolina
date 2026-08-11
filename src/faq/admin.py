from django.contrib import admin
from unfold.admin import ModelAdmin

from src.core.admin_tinymce import TinyMCEAdminMixin
from src.faq.models import FaqItem


@admin.register(FaqItem)
class FaqItemAdmin(TinyMCEAdminMixin, ModelAdmin):
    list_display = ("question_ru", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("is_active",)
    search_fields = ("question_ru", "question_en", "answer_ru")
    ordering_field = "order"
    tinymce_fields = ("answer_ru", "answer_en")
    fieldsets = (
        (
            "Загальне",
            {"fields": ("is_active", "order")},
        ),
        (
            "Русский",
            {
                "classes": ["tab"],
                "fields": ("question_ru", "answer_ru"),
            },
        ),
        (
            "English",
            {
                "classes": ["tab"],
                "fields": ("question_en", "answer_en"),
            },
        ),
    )
