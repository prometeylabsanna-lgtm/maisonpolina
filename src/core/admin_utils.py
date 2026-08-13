"""Shared Unfold admin helpers."""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe


def image_preview(image_field, *, size: int = 72, fallback_url: str = "") -> str:
    url = ""
    if image_field:
        try:
            url = image_field.url
        except (ValueError, AttributeError):
            url = ""
    if not url:
        url = fallback_url
    if not url:
        return "—"
    return format_html(
        '<img src="{}" width="{}" height="{}" '
        'class="rounded-default object-contain" alt="" loading="lazy" />',
        url,
        size,
        size,
    )


class ImagePreviewAdminMixin:
    """Set preview_attr and optionally preview_size."""

    preview_attr = "image"
    preview_size = 56

    @admin.display(description="Фото")
    def get_photo_preview(self, obj):
        return image_preview(getattr(obj, self.preview_attr, None), size=self.preview_size)


def status_badge(label: str, *, tone: str = "neutral") -> str:
    """tone: neutral | info | success | warning | danger"""
    tones = {
        "neutral": "bg-base-200 text-base-700 dark:bg-base-700 dark:text-base-200",
        "info": "bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-200",
        "success": "bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-200",
        "warning": "bg-amber-100 text-amber-900 dark:bg-amber-900/40 dark:text-amber-200",
        "danger": "bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-200",
    }
    css = tones.get(tone, tones["neutral"])
    return format_html(
        '<span class="inline-flex items-center rounded-default px-2 py-0.5 text-xs font-medium {}">{}</span>',
        css,
        label,
    )


def empty_dash() -> str:
    return mark_safe("—")
