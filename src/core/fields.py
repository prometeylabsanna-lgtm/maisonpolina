"""ImageField that stores uploads as WebP."""

from __future__ import annotations

from pathlib import Path

from django import forms
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db.models.fields.files import ImageField, ImageFieldFile

from src.core.webp import convert_bytes_to_webp

_MAX_ADMIN_IMAGE_BYTES = 12 * 1024 * 1024
ADMIN_IMAGE_ACCEPT = (
    "image/jpeg,image/png,image/webp,image/gif,image/heic,image/heif,.heic,.heif"
)
_IMAGE_TYPE_ERROR = (
    "Нужен файл JPEG, PNG, WebP, GIF или HEIC (фото с iPhone)."
)
_HEIC_SUFFIXES = {".heic", ".heif"}
_HEIC_TYPES = {"image/heic", "image/heif"}
_HEIC_ERROR = (
    "Не удалось прочитать фото с iPhone (HEIC). "
    "В «Фото» экспортируйте кадр как JPEG и загрузите снова."
)


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


def _is_heic_upload(uploaded) -> bool:
    name = (getattr(uploaded, "name", "") or "").lower()
    ctype = (getattr(uploaded, "content_type", "") or "").lower()
    return Path(name).suffix in _HEIC_SUFFIXES or ctype in _HEIC_TYPES


def prepare_admin_image_upload(uploaded):
    """Convert a new admin upload to WebP. Leave existing files untouched."""
    if not uploaded or uploaded is False:
        return uploaded
    if getattr(uploaded, "_committed", False):
        return uploaded
    converted = to_webp_file(getattr(uploaded, "name", "") or "image", uploaded)
    if converted is not None:
        _name, content = converted
        content.content_type = "image/webp"
        return content
    if _is_heic_upload(uploaded):
        raise ValidationError(_HEIC_ERROR, code="heic")
    return uploaded


class WebPFieldFile(ImageFieldFile):
    def save(self, name, content, save=True):
        converted = to_webp_file(name, content)
        if converted is not None:
            name, content = converted
        super().save(name, content, save=save)


class WebPImageField(ImageField):
    attr_class = WebPFieldFile


class AdminWebPImageField(forms.ImageField):
    """Form field used in admin: JPG/PNG/GIF/HEIC become WebP on upload."""

    default_error_messages = {
        **forms.ImageField.default_error_messages,
        "invalid_image": _IMAGE_TYPE_ERROR,
        "invalid": _IMAGE_TYPE_ERROR,
        "empty": "Выберите файл фото.",
        "missing": "Выберите файл фото.",
        "max_size": "Файл больше 12 МБ. Сожмите фото или выберите меньший файл.",
        "heic": _HEIC_ERROR,
    }

    def clean(self, data, initial=None):
        if data and data is not False and not getattr(data, "_committed", False):
            size = getattr(data, "size", 0) or 0
            if size > _MAX_ADMIN_IMAGE_BYTES:
                raise ValidationError(
                    self.error_messages["max_size"],
                    code="max_size",
                )
            if _is_heic_upload(data):
                converted = to_webp_file(
                    getattr(data, "name", "") or "image.heic", data
                )
                if converted is None:
                    raise ValidationError(
                        self.error_messages["heic"],
                        code="heic",
                    )
                _name, data = converted
                data.content_type = "image/webp"
        uploaded = super().clean(data, initial)
        return prepare_admin_image_upload(uploaded)
