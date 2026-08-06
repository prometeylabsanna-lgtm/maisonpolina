from django.contrib import admin
from unfold.admin import ModelAdmin

from src.reviews.models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(ModelAdmin):
    list_display = ("author_name", "role_ru", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("is_active",)
    search_fields = ("author_name", "text_ru", "text_en")
    ordering_field = "order"
