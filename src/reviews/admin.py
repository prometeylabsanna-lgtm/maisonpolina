from django.contrib import admin
from unfold.admin import ModelAdmin

from src.reviews.models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(ModelAdmin):
    list_display = (
        "author_name",
        "rating",
        "is_active",
        "is_public_submission",
        "order",
        "created_at",
    )
    list_editable = ("is_active", "order", "rating")
    list_filter = ("is_active", "is_public_submission", "rating")
    search_fields = ("author_name", "text_ru", "text_en")
    ordering_field = "order"
    readonly_fields = ("created_at", "is_public_submission")
