"""Default personality fact/extra rows for idempotent seed."""

from __future__ import annotations

# (group, order, label_ru, label_en, value_ru, value_en)
PERSONALITY_ITEM_DEFAULTS: tuple[tuple[str, int, str, str, str, str], ...] = (
    (
        "facts",
        1,
        "Направление",
        "Focus",
        "Управление стилем жизни",
        "Lifestyle Management",
    ),
    (
        "facts",
        2,
        "Направление",
        "Focus",
        "Деловой этикет",
        "Business Etiquette",
    ),
    (
        "facts",
        3,
        "Направление",
        "Focus",
        "Кросс-культурная коммуникация",
        "Cross-cultural Communication",
    ),
    (
        "extras",
        1,
        "",
        "",
        "Опыт в премиальном hospitality",
        "High-end hospitality background",
    ),
    (
        "extras",
        2,
        "",
        "",
        "Event-менеджмент",
        "Event Management",
    ),
    (
        "extras",
        3,
        "",
        "",
        "PR и коммуникации",
        "PR & Communications expert",
    ),
)
