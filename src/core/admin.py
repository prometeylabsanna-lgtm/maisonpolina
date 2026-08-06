from django.contrib import admin
from unfold.admin import ModelAdmin

from src.core.admin_site_content import register_site_content_section_admins
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
                    "copyright_name",
                    "location_ru",
                    "location_en",
                )
            },
        ),
        ("Контакти", {"fields": ("phone", "email")}),
        (
            "Соцмережі",
            {"fields": ("telegram_url", "instagram_url", "whatsapp_url")},
        ),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        from django.shortcuts import redirect
        from django.urls import reverse

        obj = SiteSettings.get_solo()
        return redirect(reverse("admin:core_sitesettings_change", args=[obj.pk]))


@admin.register(SeoMeta)
class SeoMetaAdmin(ModelAdmin):
    list_display = ("page", "title_ru", "title_en")
    search_fields = ("page", "title_ru", "title_en")


register_site_content_section_admins()
