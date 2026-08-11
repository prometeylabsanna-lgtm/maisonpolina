from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from unfold.admin import ModelAdmin

from src.core.admin_section_styles import register_theme_styles_admin
from src.core.admin_site_content import register_site_content_section_admins
from src.core.admin_utils import image_preview
from src.core.models import SeoMeta, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    fieldsets = (
        (
            "Основне",
            {
                "fields": (
                    "brand_name",
                    "logo",
                    "get_logo_preview",
                    "copyright_name",
                )
            },
        ),
        (
            "Русский",
            {
                "classes": ["tab"],
                "fields": ("location_ru",),
            },
        ),
        (
            "English",
            {
                "classes": ["tab"],
                "fields": ("location_en",),
            },
        ),
        ("Контакти", {"fields": ("phone", "email")}),
        (
            "Соцмережі",
            {"fields": ("telegram_url", "instagram_url", "whatsapp_url")},
        ),
    )
    readonly_fields = ("get_logo_preview",)

    @admin.display(description="Превʼю логотипу")
    def get_logo_preview(self, obj):
        return image_preview(getattr(obj, "logo", None), size=96)

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj, _ = SiteSettings.objects.get_or_create(pk=1)
        return HttpResponseRedirect(
            reverse("admin:core_sitesettings_change", args=[obj.pk])
        )


@admin.register(SeoMeta)
class SeoMetaAdmin(ModelAdmin):
    """SEO title/description stay plain text (no HTML in meta tags)."""

    list_display = ("page", "title_ru", "title_en", "get_og_preview")
    search_fields = ("page", "title_ru", "title_en")
    readonly_fields = ("get_og_preview",)
    fieldsets = (
        (None, {"fields": ("page", "og_image", "get_og_preview")}),
        (
            "Русский",
            {
                "classes": ["tab"],
                "fields": ("title_ru", "description_ru"),
            },
        ),
        (
            "English",
            {
                "classes": ["tab"],
                "fields": ("title_en", "description_en"),
            },
        ),
    )

    @admin.display(description="OG")
    def get_og_preview(self, obj):
        return image_preview(getattr(obj, "og_image", None))


register_site_content_section_admins()
register_theme_styles_admin()
