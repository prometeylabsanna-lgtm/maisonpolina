from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from src.formats.models import FormatFeature, ServiceFormat


class FormatFeatureInline(TabularInline):
    model = FormatFeature
    extra = 1
    ordering_field = "order"
    hide_ordering_field = True


@admin.register(ServiceFormat)
class ServiceFormatAdmin(ModelAdmin):
    list_display = ("title_ru", "price_text_ru", "is_featured", "is_active", "order")
    list_editable = ("is_active", "order", "is_featured")
    list_filter = ("is_active", "is_featured")
    search_fields = ("title_ru", "title_en")
    inlines = [FormatFeatureInline]
    ordering_field = "order"
