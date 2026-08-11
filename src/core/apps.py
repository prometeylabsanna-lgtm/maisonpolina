from django.apps import AppConfig
from django.contrib import admin


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.core"
    label = "core"
    verbose_name = "Сайт"

    def ready(self) -> None:
        from src.core import signals  # noqa: F401

        admin.site.site_header = "MaisonPolina"
        admin.site.site_title = "MaisonPolina"
        admin.site.index_title = "Панель управления"
