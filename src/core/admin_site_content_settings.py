"""SiteSettings fields embedded into CMS section forms."""

from __future__ import annotations

from django import forms
from django.templatetags.static import static
from unfold.widgets import UnfoldAdminFileFieldWidget, UnfoldBooleanWidget

from src.core.admin_guidelines import image_help
from src.core.admin_site_content_widgets import CmsAdminTextInputWidget
from src.core.fields import ADMIN_IMAGE_ACCEPT, AdminWebPImageField
from src.core.models import SiteSettings
from src.core.site_content_types import ContentSection

SETTINGS_PREFIX = "settings__"

SETTINGS_META: dict[str, dict] = {
    "logo": {"kind": "image", "label": "Логотип"},
    "brand_name": {"kind": "text", "label": "Название бренда"},
    "phone": {"kind": "text", "label": "Телефон"},
    "email": {"kind": "text", "label": "Email"},
    "telegram_url": {"kind": "text", "label": "Telegram"},
    "instagram_url": {"kind": "text", "label": "Instagram"},
    "whatsapp_url": {"kind": "text", "label": "WhatsApp"},
    "copyright_name": {"kind": "text", "label": "Имя в копирайте"},
    "location_ru": {"kind": "text", "label": "Адрес / локация (RU)", "lang": "ru"},
    "location_en": {"kind": "text", "label": "Адрес / локация (EN)", "lang": "en"},
}


def settings_field_name(name: str) -> str:
    return f"{SETTINGS_PREFIX}{name}"


def add_settings_fields(form: forms.Form, section: ContentSection) -> None:
    if not section.settings_fields:
        return
    solo = SiteSettings.get_solo()
    form._cms_settings = solo
    for name in section.settings_fields:
        meta = SETTINGS_META.get(name)
        if meta is None:
            continue
        field_name = settings_field_name(name)
        if meta["kind"] == "image":
            form.fields[field_name] = AdminWebPImageField(
                label=meta["label"],
                required=False,
                widget=UnfoldAdminFileFieldWidget(
                    attrs={"accept": ADMIN_IMAGE_ACCEPT}
                ),
                help_text=image_help("settings.logo"),
            )
            form.fields[f"{field_name}__clear"] = forms.BooleanField(
                label="Удалить логотип",
                required=False,
                widget=UnfoldBooleanWidget(),
            )
            continue
        form.fields[field_name] = forms.CharField(
            label=meta["label"],
            required=False,
            initial=getattr(solo, name, "") or "",
            widget=CmsAdminTextInputWidget(),
        )


def save_settings_fields(form: forms.Form, section: ContentSection) -> None:
    if not section.settings_fields:
        return
    solo = getattr(form, "_cms_settings", None) or SiteSettings.get_solo()
    changed = False
    for name in section.settings_fields:
        meta = SETTINGS_META.get(name)
        if meta is None:
            continue
        field_name = settings_field_name(name)
        if meta["kind"] == "image":
            if form.cleaned_data.get(f"{field_name}__clear"):
                if solo.logo:
                    try:
                        solo.logo.delete(save=False)
                    except OSError:
                        pass
                solo.logo = ""
                changed = True
            uploaded = form.cleaned_data.get(field_name)
            if uploaded:
                solo.logo = uploaded
                changed = True
            continue
        if field_name not in form.cleaned_data:
            continue
        value = (form.cleaned_data.get(field_name) or "").strip()
        if getattr(solo, name, "") != value:
            setattr(solo, name, value)
            changed = True
    if changed:
        solo.save()


def build_settings_rows(form: forms.Form, section: ContentSection) -> list[dict]:
    rows: list[dict] = []
    solo = getattr(form, "_cms_settings", None)
    for name in section.settings_fields:
        meta = SETTINGS_META.get(name)
        if meta is None:
            continue
        field_name = settings_field_name(name)
        if field_name not in form.fields:
            continue
        if meta["kind"] == "image":
            preview_url = ""
            caption = ""
            if solo and solo.logo:
                try:
                    preview_url = solo.logo.url
                    caption = f"Текущее: {solo.logo.name}"
                except ValueError:
                    preview_url = ""
            if not preview_url:
                preview_url = static("images/brand-monogram-header.png")
                caption = "Сейчас на сайте (стандартный знак). Загрузите новый, чтобы заменить."
            rows.append(
                {
                    "kind": "settings_image",
                    "label": meta["label"],
                    "help_text": image_help("settings.logo"),
                    "field": form[field_name],
                    "clear": form[f"{field_name}__clear"],
                    "preview_url": preview_url,
                    "preview_caption": caption,
                    "has_upload": bool(solo and solo.logo),
                }
            )
            continue
        rows.append(
            {
                "kind": "settings_text",
                "label": meta["label"],
                "lang": meta.get("lang", ""),
                "field": form[field_name],
            }
        )
    return rows
