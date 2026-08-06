from django.utils.translation import get_language


class BilingualTextMixin:
    """Return language-specific text with fallback to RU."""

    def get_text(self, field: str) -> str:
        lang = (get_language() or "ru")[:2]
        value = getattr(self, f"{field}_{lang}", "") or ""
        if value:
            return value
        return getattr(self, f"{field}_ru", "") or ""
