"""Shared fill (solid / gradient) helpers for SectionStyle."""

from __future__ import annotations

import re

from django.core.exceptions import ValidationError
from django.db import models

HEX_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


class FillType(models.TextChoices):
    SOLID = "solid", "Один цвет"
    GRADIENT = "gradient", "Градиент"


def validate_hex_color(value: str) -> None:
    if not value:
        return
    if not HEX_RE.match(value.strip()):
        raise ValidationError("Нужен цвет в формате #4c0d13")


def normalize_hex(value: str) -> str:
    return (value or "").strip()


def resolve_fill(
    *,
    fill_type: str,
    solid_color: str,
    gradient_start: str,
    gradient_end: str,
    gradient_angle: int | None,
) -> str | None:
    """Return CSS background value or None to keep stylesheet defaults."""
    solid = normalize_hex(solid_color)
    start = normalize_hex(gradient_start)
    end = normalize_hex(gradient_end)
    angle = 180 if gradient_angle is None else int(gradient_angle)

    if fill_type == FillType.GRADIENT:
        if start and end:
            return f"linear-gradient({angle}deg, {start}, {end})"
        return None
    if fill_type == FillType.SOLID:
        return solid or None
    # Unset type: prefer solid if provided, else complete gradient
    if solid:
        return solid
    if start and end:
        return f"linear-gradient({angle}deg, {start}, {end})"
    return None


def fill_field_names(prefix: str) -> tuple[str, ...]:
    return (
        f"{prefix}_fill_type",
        f"{prefix}_solid_color",
        f"{prefix}_gradient_start",
        f"{prefix}_gradient_end",
        f"{prefix}_gradient_angle",
    )
