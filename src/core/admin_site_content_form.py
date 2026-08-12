"""CMS section form + fieldsets (choice, image, video)."""

from __future__ import annotations

from django import forms
from unfold.widgets import UnfoldAdminFileFieldWidget, UnfoldBooleanWidget

from src.core.admin_site_content_widgets import (
    CmsAdminTextInputWidget,
    CmsAdminTextareaWidget,
)
from src.core.admin_tinymce import (
    PLAIN_TEXTAREA_KEYS,
    RICH_TEXT_KEYS,
    cms_tinymce_widget,
)
from src.core.block_defaults import (
    BLOCK_CONTENT_TYPES,
    BLOCK_DEFAULTS,
    CHOICE_KEYS,
    IMAGE_KEYS,
    IMAGE_STATIC_FALLBACKS,
    VIDEO_KEYS,
    get_block_field_label,
    is_visibility_key,
)
from src.core.models import SiteBlock
from src.core.services import invalidate_site_blocks_cache
from src.core.site_content_registry import (
    ContentSection,
    iter_section_blocks,
)

SECTION_VISIBLE_FIELD = "section_visible"
VIDEO_HELP = (
    "MP4 или WebM. На продакшене файл с админки не сохраняется (Vercel) — "
    "укажите URL на CDN или положите ролик в static."
)


def _block_image_preview(block: SiteBlock) -> dict[str, str]:
    """Return preview URL for admin: uploaded media first, else site static fallback."""
    if block.image:
        try:
            return {
                "url": block.image.url,
                "source": "upload",
                "caption": f"Текущее фото: {block.image.name}",
            }
        except ValueError:
            pass
    static_path = IMAGE_STATIC_FALLBACKS.get(block.key, "")
    if static_path:
        from django.templatetags.static import static

        return {
            "url": static(static_path),
            "source": "static",
            "caption": "Сейчас на сайте (стандартное фото). Загрузите новое, чтобы заменить.",
        }
    return {"url": "", "source": "", "caption": ""}


def block_field_name(page: str, key: str, suffix: str) -> str:
    return f"block__{page}__{key}__{suffix}"


def _content_type(page: str, key: str) -> str:
    return BLOCK_CONTENT_TYPES.get((page, key), SiteBlock.ContentType.TEXT)


def load_section_blocks(section: ContentSection) -> dict[tuple[str, str], SiteBlock]:
    blocks: dict[tuple[str, str], SiteBlock] = {}
    for page, key in iter_section_blocks(section):
        defaults = BLOCK_DEFAULTS.get((page, key), {})
        block, _created = SiteBlock.objects.get_or_create(
            page=page,
            key=key,
            defaults={
                "label": get_block_field_label(page, key),
                "content_type": _content_type(page, key),
                "text_ru": defaults.get("text_ru", "1" if is_visibility_key(key) else ""),
                "text_en": defaults.get("text_en", "1" if is_visibility_key(key) else ""),
                "sort_order": 0,
                "is_active": True,
            },
        )
        blocks[(page, key)] = block
    return blocks


class SitePageContentForm(forms.Form):
    def __init__(
        self,
        section: ContentSection,
        blocks: dict[tuple[str, str], SiteBlock],
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.section = section
        self.blocks = blocks

        if section.visibility_key:
            page, key = self._visibility_page_key(section)
            block = blocks[(page, key)]
            self.fields[SECTION_VISIBLE_FIELD] = forms.BooleanField(
                label="Показывать секцию на сайте",
                required=False,
                initial=block.visibility_on(),
                widget=UnfoldBooleanWidget(),
            )

        for page, key in section.blocks:
            self._add_block_fields(blocks[(page, key)])

    def _visibility_page_key(self, section: ContentSection) -> tuple[str, str]:
        for page, key in iter_section_blocks(section):
            if key == section.visibility_key:
                return page, key
        raise KeyError(section.visibility_key)

    def _add_block_fields(self, block: SiteBlock) -> None:
        page, key = block.page, block.key
        label = get_block_field_label(page, key)

        if key in CHOICE_KEYS:
            current = (block.text_ru or "").strip() or CHOICE_KEYS[key][0][0]
            self.fields[block_field_name(page, key, "choice")] = forms.ChoiceField(
                label=label,
                choices=CHOICE_KEYS[key],
                initial=current,
                required=True,
                widget=forms.Select(attrs={"class": "cms-admin-input"}),
            )
            return

        if block.content_type == SiteBlock.ContentType.IMAGE or key in IMAGE_KEYS:
            self.fields[block_field_name(page, key, "image")] = forms.ImageField(
                label=label,
                required=False,
                widget=UnfoldAdminFileFieldWidget(),
                help_text=f"Текущее: {block.image.name}" if block.image else "",
            )
            self.fields[block_field_name(page, key, "clear_image")] = forms.BooleanField(
                label="Удалить изображение",
                required=False,
                widget=UnfoldBooleanWidget(),
            )
            if key in VIDEO_KEYS:
                self._add_video_fields(block, page, key)
            return

        if key in RICH_TEXT_KEYS:
            widget_ru = cms_tinymce_widget(height=420 if key == "privacy.body" else 280)
            widget_en = cms_tinymce_widget(height=420 if key == "privacy.body" else 280)
        elif key in PLAIN_TEXTAREA_KEYS:
            widget_ru = CmsAdminTextareaWidget(attrs={"rows": 4})
            widget_en = CmsAdminTextareaWidget(attrs={"rows": 4})
        else:
            widget_ru = CmsAdminTextInputWidget()
            widget_en = CmsAdminTextInputWidget()

        self.fields[block_field_name(page, key, "ru")] = forms.CharField(
            label=f"{label} (RU)",
            initial=block.text_ru,
            required=False,
            widget=widget_ru,
        )
        self.fields[block_field_name(page, key, "en")] = forms.CharField(
            label=f"{label} (EN)",
            initial=block.text_en,
            required=False,
            widget=widget_en,
        )

    def _add_video_fields(self, block: SiteBlock, page: str, key: str) -> None:
        self.fields[block_field_name(page, key, "video_file")] = forms.FileField(
            label="Видео (файл)",
            required=False,
            widget=UnfoldAdminFileFieldWidget(),
            help_text=VIDEO_HELP,
        )
        self.fields[block_field_name(page, key, "video_url")] = forms.URLField(
            label="Видео (URL)",
            required=False,
            initial=block.video_url or "",
            widget=CmsAdminTextInputWidget(),
            help_text="Прямая ссылка на mp4/webm. YouTube и Vimeo не поддерживаются.",
            assume_scheme="https",
        )
        self.fields[block_field_name(page, key, "clear_video")] = forms.BooleanField(
            label="Удалить видео",
            required=False,
            widget=UnfoldBooleanWidget(),
        )

    def save(self) -> None:
        if SECTION_VISIBLE_FIELD in self.fields:
            page, key = self._visibility_page_key(self.section)
            block = self.blocks[(page, key)]
            on = bool(self.cleaned_data.get(SECTION_VISIBLE_FIELD))
            block.text_ru = "1" if on else "0"
            block.text_en = block.text_ru
            block.is_active = True
            block.content_type = SiteBlock.ContentType.TEXT
            block.save()

        for block in self.blocks.values():
            page, key = block.page, block.key
            if key == self.section.visibility_key:
                continue

            block.is_active = True
            if key in CHOICE_KEYS:
                value = (self.cleaned_data.get(block_field_name(page, key, "choice")) or "").strip()
                allowed = {choice[0] for choice in CHOICE_KEYS[key]}
                if value not in allowed:
                    value = CHOICE_KEYS[key][0][0]
                block.content_type = SiteBlock.ContentType.TEXT
                block.text_ru = value
                block.text_en = value
            elif block.content_type == SiteBlock.ContentType.IMAGE or key in IMAGE_KEYS:
                self._save_media_block(block, page, key)
            else:
                block.content_type = SiteBlock.ContentType.TEXT
                block.text_ru = (
                    self.cleaned_data.get(block_field_name(page, key, "ru"), "") or ""
                ).strip()
                block.text_en = (
                    self.cleaned_data.get(block_field_name(page, key, "en"), "") or ""
                ).strip()
            block.save()

        invalidate_site_blocks_cache()

    def _save_media_block(self, block: SiteBlock, page: str, key: str) -> None:
        block.content_type = SiteBlock.ContentType.IMAGE
        if self.cleaned_data.get(block_field_name(page, key, "clear_image")):
            block.image = ""
        uploaded = self.cleaned_data.get(block_field_name(page, key, "image"))
        if uploaded:
            block.image = uploaded
        if key not in VIDEO_KEYS:
            return
        if self.cleaned_data.get(block_field_name(page, key, "clear_video")):
            block.video_file = ""
            block.video_url = ""
        video_file = self.cleaned_data.get(block_field_name(page, key, "video_file"))
        if video_file:
            block.video_file = video_file
        url_name = block_field_name(page, key, "video_url")
        if url_name in self.cleaned_data:
            block.video_url = (self.cleaned_data.get(url_name) or "").strip()


def _block_rows_for_keys(
    form: SitePageContentForm,
    section: ContentSection,
    keys: tuple[str, ...],
) -> list[dict]:
    page_keys = {key: page for page, key in section.blocks}
    rows: list[dict] = []
    for key in keys:
        page = page_keys.get(key)
        if page is None:
            continue
        block = form.blocks.get((page, key))
        if block is None:
            continue
        if key in CHOICE_KEYS:
            choice_name = block_field_name(page, key, "choice")
            rows.append(
                {
                    "key": key,
                    "label": get_block_field_label(page, key),
                    "kind": "choice",
                    "is_image": False,
                    "choice": form[choice_name] if choice_name in form.fields else None,
                }
            )
            continue
        is_image = (
            block.content_type == SiteBlock.ContentType.IMAGE or key in IMAGE_KEYS
        )
        if is_image:
            rows.append(_image_row(form, block, page, key))
            continue
        ru_name = block_field_name(page, key, "ru")
        en_name = block_field_name(page, key, "en")
        rows.append(
            {
                "key": key,
                "label": get_block_field_label(page, key),
                "kind": "text",
                "is_image": False,
                "ru": form[ru_name] if ru_name in form.fields else None,
                "en": form[en_name] if en_name in form.fields else None,
            }
        )
    return rows


def _image_row(form: SitePageContentForm, block: SiteBlock, page: str, key: str) -> dict:
    image_name = block_field_name(page, key, "image")
    clear_name = block_field_name(page, key, "clear_image")
    preview = _block_image_preview(block)
    video_file_name = block_field_name(page, key, "video_file")
    video_url_name = block_field_name(page, key, "video_url")
    clear_video_name = block_field_name(page, key, "clear_video")
    has_video = bool(block.video_file or block.video_url)
    return {
        "key": key,
        "label": get_block_field_label(page, key),
        "kind": "image",
        "is_image": True,
        "image": form[image_name] if image_name in form.fields else None,
        "clear_image": form[clear_name] if clear_name in form.fields else None,
        "block": block,
        "preview_url": preview["url"],
        "preview_caption": preview["caption"],
        "has_upload": bool(block.image),
        "has_video_fields": key in VIDEO_KEYS,
        "video_file": form[video_file_name] if video_file_name in form.fields else None,
        "video_url": form[video_url_name] if video_url_name in form.fields else None,
        "clear_video": (
            form[clear_video_name] if clear_video_name in form.fields else None
        ),
        "has_video": has_video,
        "video_current": block.video_file.name if block.video_file else block.video_url,
    }


def build_section_fieldsets(
    form: SitePageContentForm,
    section: ContentSection,
) -> list[tuple[str, list]]:
    fieldsets: list[tuple[str, list]] = []
    if SECTION_VISIBLE_FIELD in form.fields:
        fieldsets.append(
            (
                "Видимость",
                [{"kind": "visibility", "field": form[SECTION_VISIBLE_FIELD]}],
            )
        )
    if section.field_groups:
        for group in section.field_groups:
            rows = _block_rows_for_keys(form, section, group.keys)
            if rows:
                fieldsets.append((group.title, rows))
    elif section.blocks:
        keys = tuple(key for _page, key in section.blocks)
        rows = _block_rows_for_keys(form, section, keys)
        if rows:
            fieldsets.append(("", rows))
    return fieldsets

