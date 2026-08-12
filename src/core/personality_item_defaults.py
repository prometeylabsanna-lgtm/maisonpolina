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
    ("facts", 7, "Обувь", "Shoes", "39", "39"),
    ("facts", 8, "Одежда", "Clothing", "38", "38"),
    ("facts", 9, "Зодиак", "Zodiac", "Водолей", "Aquarius"),
    ("facts", 10, "Тату", "Tattoo", "нет", "none"),
    ("facts", 11, "Пирсинг", "Piercing", "нет", "none"),
    ("facts", 12, "Цветы", "Flowers", "Орхидеи, Лилии", "Orchids, lilies"),
    ("facts", 13, "Кухня", "Cuisine", "Итальянская", "Italian"),
    ("facts", 14, "Алкоголь", "Alcohol", "уточнять", "upon request"),
    ("facts", 15, "Курение", "Smoking", "Не курю", "Non-smoker"),
    ("extras", 1, "", "", "мастер спорта", "Master of Sport"),
    ("extras", 2, "", "", "профессиональная модель", "professional model"),
    ("extras", 3, "", "", "фешн-журналист", "fashion journalist"),
)
