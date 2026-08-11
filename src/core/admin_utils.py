"""Shared Unfold admin helpers."""

from django.utils.html import format_html
from django.utils.safestring import mark_safe


def image_preview(image_field, *, size: int = 72) -> str:
    if not image_field:
        return "—"
    try:
        url = image_field.url
    except (ValueError, AttributeError):
        return "—"
    return format_html(
        '<img src="{}" width="{}" height="{}" '
        'class="rounded-default object-cover" alt="" loading="lazy" />',
        url,
        size,
        size,
    )


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
