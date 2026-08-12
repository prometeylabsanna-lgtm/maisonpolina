"""ImageField that stores uploads as WebP."""

from __future__ import annotations

from django import forms
from django.core.files.base import ContentFile
from django.db.models.fields.files import ImageField, ImageFieldFile

from src.core.webp import convert_bytes_to_webp


def to_webp_file(name: str, content) -> tuple[str, ContentFile] | None:
    orig_name = name or getattr(content, "name", "") or "image"
    position = content.tell() if hasattr(content, "tell") else None
    try:
        data = content.read()
    finally:
        if hasattr(content, "seek"):
            try:
                content.seek(0 if position is None else position)
            except OSError:
                pass
    converted = convert_bytes_to_webp(data, orig_name)
    if converted is None:
        return None
    payload, webp_name = converted
    return webp_name, ContentFile(payload, name=webp_name)


def prepare_admin_image_upload(uploaded):
    """Convert a new admin upload to WebP. Leave existing files untouched."""
    if not uploaded or uploaded is False:
        return uploaded
    if getattr(uploaded, "_committed", False):
        return uploaded
    converted = to_webp_file(getattr(uploaded, "name", "") or "image", uploaded)
    if converted is None:
        return uploaded
    _name, content = converted
    content.content_type = "image/webp"
    return content


class WebPFieldFile(ImageFieldFile):
    def save(self, name, content, save=True):
        converted = to_webp_file(name, content)
        if converted is not None:
            name, content = converted
        super().save(name, content, save=save)


class WebPImageField(ImageField):
    attr_class = WebPFieldFile


class AdminWebPImageField(forms.ImageField):
    """Form field used in admin: JPG/PNG/GIF become WebP on upload."""

    def clean(self, data, initial=None):
        uploaded = super().clean(data, initial)
        return prepare_admin_image_upload(uploaded)
