"""Default personality fact/extra rows for idempotent seed."""

from __future__ import annotations

# (group, order, label_ru, label_en, value_ru, value_en)
PERSONALITY_ITEM_DEFAULTS: tuple[tuple[str, int, str, str, str, str], ...] = (
    ("facts", 1, "Возраст", "Age", "32", "32"),
    ("facts", 2, "Глаза", "Eyes", "серые", "gray"),
    ("facts", 3, "Волосы", "Hair", "русые", "light brown"),
    ("facts", 4, "Рост", "Height", "174", "174"),
    ("facts", 5, "Вес", "Weight", "59", "59"),
    ("facts", 6, "Параметры", "Measurements", "90-60-94", "90-60-94"),
    ("facts", 7, "Цветы", "Flowers", "Орхидеи, Лилии", "Orchids, lilies"),
    ("facts", 8, "Кухня", "Cuisine", "Итальянская", "Italian"),
    ("facts", 9, "Алкоголь", "Alcohol", "уточнять", "upon request"),
    ("facts", 10, "Курение", "Smoking", "Не курю", "Non-smoker"),
    ("extras", 1, "", "", "мастер спорта", "Master of Sport"),
    ("extras", 2, "", "", "профессиональная модель", "professional model"),
    ("extras", 3, "", "", "фешн-журналист", "fashion journalist"),
)
