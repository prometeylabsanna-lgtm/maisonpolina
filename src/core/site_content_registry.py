from __future__ import annotations

from typing import Iterator

from django.urls import reverse_lazy

from src.core.block_defaults import get_block_field_label as _defaults_label
from src.core.site_content_sections import CONTENT_SECTIONS
from src.core.site_content_types import ContentSection, FieldGroup

__all__ = [
    "CONTENT_SECTIONS",
    "ContentSection",
    "FieldGroup",
    "build_content_sidebar_items",
    "get_block_field_label",
    "get_section",
    "iter_section_blocks",
]


def get_block_field_label(page: str, key: str) -> str:
    return _defaults_label(page, key)


def get_section(page_slug: str, section_slug: str) -> ContentSection | None:
    for section in CONTENT_SECTIONS:
        if section.page_slug == page_slug and section.slug == section_slug:
            return section
    return None


def iter_section_blocks(section: ContentSection) -> Iterator[tuple[str, str]]:
    yield from section.blocks
    if section.visibility_key:
        yield section.page_slug, section.visibility_key


def build_content_sidebar_items() -> list[dict]:
    return [
        {
            "title": section.sidebar_title or section.title,
            "icon": section.sidebar_icon,
            "link": reverse_lazy(f"admin:core_{section.admin_model_name}_changelist"),
        }
        for section in CONTENT_SECTIONS
    ]
