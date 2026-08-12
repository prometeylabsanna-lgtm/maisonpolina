"""TinyMCE widgets and ModelAdmin mixin for long text fields."""

from django.db import models
from tinymce.widgets import TinyMCE

# Long body fields — TinyMCE. Titles / eyebrows / CTAs stay plain inputs.
RICH_TEXT_KEYS: frozenset[str] = frozenset(
    {
        "hero.lead",
        "about.body_1",
        "about.body_2",
        "about.body_3",
        "about.quote",
        "formats.note",
        "contacts.lead",
        "privacy.body",
        "personality.languages",
        "personality.respect",
        "personality.education",
        "personality.travel",
        "lead.success_text",
        "review.success_text",
    }
)

# One-line / short sentence bodies — compact TinyMCE height.
COMPACT_RICH_TEXT_KEYS: frozenset[str] = frozenset(
    {
        "about.quote",
        "personality.languages",
        "personality.respect",
        "personality.education",
        "personality.travel",
        "lead.success_text",
        "review.success_text",
    }
)

# Short multiline UI chrome — plain textarea, not TinyMCE
PLAIN_TEXTAREA_KEYS: frozenset[str] = frozenset(
    {
        "form.consent_prefix",
        "chat.empty",
        "chat.error_rate",
        "chat.error_session",
        "chat.error_send",
        "error.404_text",
        "error.500_text",
    }
)

MODELADMIN_RICH_FIELDS: frozenset[str] = frozenset(
    {
        "description_ru",
        "description_en",
        "answer_ru",
        "answer_en",
        "text_ru",
        "text_en",
        "admin_note",
    }
)

_TINYMCE_HEIGHT_PRIVACY = 420
_TINYMCE_HEIGHT_DEFAULT = 280
_TINYMCE_HEIGHT_COMPACT = 100


def cms_tinymce_height_for_key(key: str, *, page: str = "") -> int:
    if key == "privacy.body" or (page == "privacy" and key == "body"):
        return _TINYMCE_HEIGHT_PRIVACY
    if key in COMPACT_RICH_TEXT_KEYS or f"{page}.{key}" in COMPACT_RICH_TEXT_KEYS:
        return _TINYMCE_HEIGHT_COMPACT
    return _TINYMCE_HEIGHT_DEFAULT


def is_rich_text_key(page: str, key: str) -> bool:
    return key in RICH_TEXT_KEYS or f"{page}.{key}" in RICH_TEXT_KEYS


def is_plain_textarea_key(page: str, key: str) -> bool:
    return key in PLAIN_TEXTAREA_KEYS or f"{page}.{key}" in PLAIN_TEXTAREA_KEYS


def cms_tinymce_widget(*, height: int = _TINYMCE_HEIGHT_DEFAULT) -> TinyMCE:
    rows = 3 if height <= 120 else 12 if height < 400 else 18
    return TinyMCE(
        attrs={"cols": 80, "rows": rows, "class": "cms-admin-input tinymce"},
        mce_attrs={"height": height},
    )


class TinyMCEAdminMixin:
    """Apply TinyMCE to configured TextField names; leave CharField alone."""

    tinymce_fields: frozenset[str] | set[str] | tuple[str, ...] = MODELADMIN_RICH_FIELDS

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if (
            isinstance(db_field, models.TextField)
            and db_field.name in self.tinymce_fields
        ):
            kwargs["widget"] = TinyMCE(
                attrs={"cols": 80, "rows": 15},
                mce_attrs={"height": 320},
            )
            return db_field.formfield(**kwargs)
        return super().formfield_for_dbfield(db_field, request, **kwargs)
