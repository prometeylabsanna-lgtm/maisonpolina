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


def cms_tinymce_widget(*, height: int = 280) -> TinyMCE:
    return TinyMCE(
        attrs={"cols": 80, "rows": 12, "class": "cms-admin-input tinymce"},
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
