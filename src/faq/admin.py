from django.contrib import admin
from unfold.admin import ModelAdmin

from src.faq.models import FaqItem


@admin.register(FaqItem)
class FaqItemAdmin(ModelAdmin):
    list_display = ("question_ru", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("is_active",)
    search_fields = ("question_ru", "question_en", "answer_ru")
    ordering_field = "order"
