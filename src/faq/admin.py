from django.contrib import admin
from unfold.admin import ModelAdmin

from src.core.admin_changelist import TopDropdownFilterMixin
from src.core.admin_guidelines import AdminGuidelinesMixin
from src.core.admin_tinymce import TinyMCEAdminMixin
from src.faq.models import FaqItem


@admin.register(FaqItem)
class FaqItemAdmin(
    TopDropdownFilterMixin, AdminGuidelinesMixin, TinyMCEAdminMixin, ModelAdmin
):
    guidelines_prefix = "faq"
    list_display = ("question_ru", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("is_active",)
    search_fields = ("question_ru", "question_en", "answer_ru")
    ordering_field = "order"
    tinymce_fields = ("answer_ru", "answer_en")
    fieldsets = (
        (
            "Общее",
            {
                "fields": ("is_active", "order"),
                "description": "Показ вопроса на сайте и порядок в списке.",
            },
        ),
        (
            "Русский",
            {
                "classes": ["tab"],
                "fields": ("question_ru", "answer_ru"),
                "description": "Вопрос до 90 символов, ответ до 400.",
            },
        ),
        (
            "English",
            {
                "classes": ["tab"],
                "fields": ("question_en", "answer_en"),
                "description": "Вопрос до 90 символов, ответ до 400.",
            },
        ),
    )
