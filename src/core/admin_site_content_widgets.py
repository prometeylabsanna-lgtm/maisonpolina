from __future__ import annotations

from typing import Any, Optional

from django.contrib.admin.widgets import AdminTextInputWidget, AdminTextareaWidget
from unfold.widgets import INPUT_CLASSES, TEXTAREA_CLASSES


def _join_classes(base_classes: list[str], extra_class: str = "") -> str:
    classes = list(base_classes)
    if extra_class:
        for token in extra_class.split():
            if token and token not in classes:
                classes.append(token)
    return " ".join(classes)


class CmsAdminTextInputWidget(AdminTextInputWidget):
    def __init__(self, attrs: Optional[dict[str, Any]] = None) -> None:
        merged = dict(attrs or {})
        extra_class = merged.pop("class", "")
        # Keep Unfold classes when available, always force visible cms input.
        try:
            classes = _join_classes(INPUT_CLASSES, f"cms-admin-input {extra_class}")
        except Exception:
            classes = f"cms-admin-input {extra_class}".strip()
        super().__init__(attrs={**merged, "class": classes})


class CmsAdminTextareaWidget(AdminTextareaWidget):
    def __init__(self, attrs: Optional[dict[str, Any]] = None) -> None:
        merged = dict(attrs or {})
        extra_class = merged.pop("class", "")
        try:
            classes = _join_classes(TEXTAREA_CLASSES, f"cms-admin-input {extra_class}")
        except Exception:
            classes = f"cms-admin-input {extra_class}".strip()
        super().__init__(
            attrs={
                **merged,
                "class": classes,
                "rows": merged.get("rows", 3),
            }
        )
