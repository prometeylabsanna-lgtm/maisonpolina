"""Admin mixin: convert image uploads to WebP in every ModelAdmin form."""

from __future__ import annotations

from unfold.widgets import UnfoldAdminFileFieldWidget

from src.core.fields import ADMIN_IMAGE_ACCEPT, AdminWebPImageField, WebPImageField


class WebPAdminMixin:
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if isinstance(db_field, WebPImageField):
            kwargs.setdefault("form_class", AdminWebPImageField)
            kwargs.setdefault(
                "widget",
                UnfoldAdminFileFieldWidget(attrs={"accept": ADMIN_IMAGE_ACCEPT}),
            )
        return super().formfield_for_dbfield(db_field, request, **kwargs)
