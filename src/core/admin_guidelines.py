"""Layout-safe image sizes and text lengths for admin help_text.

Values match frontend CSS (object-fit, aspect-ratio, nowrap, line-clamp).
Hints only — no hard validation.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ImageProfile:
    ratio: str
    size: str
    max_kb: int
    crop: str
    extra: str = ""

    def as_help(self) -> str:
        parts = [
            f"Рекомендуется {self.size} px, соотношение {self.ratio}.",
            f"JPEG или WebP, до {self.max_kb} КБ.",
            self.crop,
        ]
        if self.extra:
            parts.append(self.extra)
        return " ".join(part for part in parts if part)


@dataclass(frozen=True)
class TextLimit:
    chars: int
    note: str = ""

    def as_help(self) -> str:
        base = (
            f"Удобно до {self.chars} символов — длиннее может "
            f"неаккуратно смотреться на сайте."
        )
        if self.note:
            return f"{base} {self.note}"
        return base


IMAGE_PROFILES: dict[str, ImageProfile] = {
    "hero.media": ImageProfile(
        ratio="3:4 (половина) или 16:9 (на весь фон)",
        size="1200×1600 или 1920×1080",
        max_kb=450,
        crop="Кадр заполняет блок, края могут обрезаться. Лицо держите в центре.",
        extra="Для «Половина секции» — вертикальный портрет.",
    ),
    "about.portrait": ImageProfile(
        ratio="≈5:6 (682:800)",
        size="1364×1600",
        max_kb=350,
        crop="Портрет в рамке, края обрежутся. Лицо по центру.",
    ),
    "personality.portrait": ImageProfile(
        ratio="4:5",
        size="800×1000",
        max_kb=300,
        crop="Портрет в рамке, края обрежутся. Лицо по центру.",
    ),
    "contacts.bg": ImageProfile(
        ratio="16:9",
        size="1920×1080",
        max_kb=400,
        crop="Фон на всю секцию контактов, края обрежутся.",
    ),
    "gallery.image": ImageProfile(
        ratio="3:4",
        size="1200×1600",
        max_kb=400,
        crop="В ленте кадр обрезается под 3:4. В полном просмотре виден целиком.",
    ),
    "formats.image": ImageProfile(
        ratio="4:3",
        size="1200×900",
        max_kb=250,
        crop="Фото карточки формата, края обрежутся.",
    ),
    "reviews.photo": ImageProfile(
        ratio="1:1",
        size="256×256",
        max_kb=80,
        crop="Круглый аватар 64 px. Лицо по центру, без широких полей.",
    ),
    "settings.logo": ImageProfile(
        ratio="примерно 4:3",
        size="176×136",
        max_kb=40,
        crop="В шапке до 44×34 px. PNG с прозрачным фоном.",
        extra="Широкое фото сожмётся и станет нечитаемым.",
    ),
    "seo.og_image": ImageProfile(
        ratio="1.91:1",
        size="1200×630",
        max_kb=200,
        crop="Картинка для соцсетей и мессенджеров. Важное — в центре.",
    ),
}

TEXT_LIMITS: dict[str, TextLimit] = {
    "hero.title": TextLimit(24, "Имя на первом экране, крупный шрифт."),
    "hero.subtitle": TextLimit(40, "Подзаголовок под именем."),
    "hero.lead": TextLimit(220, "Абзац в колонке ≈36 знаков в строке."),
    "hero.cta_primary": TextLimit(22, "Текст кнопки."),
    "hero.cta_secondary": TextLimit(22, "Текст кнопки."),
    "hero.tagline": TextLimit(48, "Строка внизу экрана. На телефоне — бегущая лента."),
    "hero.media_layout": TextLimit(
        0,
        "Половина — вертикальный портрет 3:4. На весь фон — горизонталь 16:9.",
    ),
    "about.eyebrow": TextLimit(18, "Короткий надзаголовок."),
    "about.title": TextLimit(22, "На планшете заголовок в одну строку вместе с акцентом."),
    "about.title_accent": TextLimit(28, "Вторая часть заголовка, в одну строку с первой."),
    "about.body_1": TextLimit(280, "Один абзац биографии."),
    "about.body_2": TextLimit(280, "Один абзац биографии."),
    "about.body_3": TextLimit(220, "Один абзац биографии."),
    "about.quote": TextLimit(90, "Цитата под текстом."),
    "about.stat_1_value": TextLimit(6, "Цифра в трёх колонках."),
    "about.stat_2_value": TextLimit(6, "Цифра в трёх колонках."),
    "about.stat_3_value": TextLimit(6, "Цифра в трёх колонках."),
    "about.stat_1_label": TextLimit(22, "Подпись под цифрой, три колонки."),
    "about.stat_2_label": TextLimit(22, "Подпись под цифрой, три колонки."),
    "about.stat_3_label": TextLimit(22, "Подпись под цифрой, три колонки."),
    "about.cta": TextLimit(22, "Текст кнопки."),
    "personality.eyebrow": TextLimit(18, "Короткий надзаголовок."),
    "personality.title": TextLimit(22, "Первая часть заголовка."),
    "personality.title_accent": TextLimit(28, "Вторая часть заголовка."),
    "personality.facts_title": TextLimit(24, "Подзаголовок списка параметров."),
    "personality.languages": TextLimit(80, "Одна-две строки."),
    "personality.respect": TextLimit(80, "Одна-две строки."),
    "personality.education": TextLimit(80, "Одна-две строки."),
    "personality.travel": TextLimit(80, "Одна-две строки."),
    "personality.label": TextLimit(18, "Название строки: колонка узкая, заглавные."),
    "personality.value": TextLimit(40, "Значение в правой колонке."),
    "gallery.eyebrow": TextLimit(18, "Короткий надзаголовок."),
    "gallery.title": TextLimit(28, "Заголовок секции."),
    "gallery.title_accent": TextLimit(28, "Вторая часть заголовка."),
    "gallery.caption": TextLimit(40, "Подпись к кадру, не обязательна на сайте."),
    "gallery.alt": TextLimit(80, "Короткое описание фото. На сайте не видно."),
    "formats.eyebrow": TextLimit(18, "Короткий надзаголовок."),
    "formats.title": TextLimit(36, "Название секции или карточки."),
    "formats.title_accent": TextLimit(28, "Вторая часть заголовка секции."),
    "formats.note": TextLimit(220, "Примечание под карточками."),
    "formats.label": TextLimit(18, "Метка вроде «Формат I»."),
    "formats.description": TextLimit(180, "Описание в карточке, 2–4 предложения."),
    "formats.price_text": TextLimit(28, "Цена или «по запросу»."),
    "formats.feature": TextLimit(60, "Пункт «что входит»."),
    "formats.featured_badge": TextLimit(16, "Бейдж на избранной карточке."),
    "formats.includes": TextLimit(18, "Заголовок списка в карточке."),
    "formats.order_cta": TextLimit(22, "Кнопка в карточке."),
    "testimonials.eyebrow": TextLimit(24, "Надзаголовок блока отзывов."),
    "reviews.author_name": TextLimit(28, "Имя под отзывом, заглавные."),
    "reviews.role": TextLimit(40, "Род занятий под именем."),
    "reviews.text": TextLimit(
        280,
        "Длиннее свернётся в 5 строк с кнопкой «ещё».",
    ),
    "faq.eyebrow": TextLimit(18, "Короткий надзаголовок."),
    "faq.title": TextLimit(28, "Заголовок секции."),
    "faq.title_accent": TextLimit(28, "Вторая часть заголовка."),
    "faq.cta": TextLimit(22, "Текст кнопки."),
    "faq.question": TextLimit(90, "Одна строка-две на телефоне."),
    "faq.answer": TextLimit(400, "Ответ в раскрывающейся панели."),
    "contacts.eyebrow": TextLimit(18, "Короткий надзаголовок."),
    "contacts.title": TextLimit(28, "Заголовок секции."),
    "contacts.title_accent": TextLimit(28, "Вторая часть заголовка."),
    "contacts.lead": TextLimit(180, "Короткий текст над формой."),
    "contacts.privacy_note": TextLimit(120, "Пометка о конфиденциальности."),
    "contacts.telegram_title": TextLimit(24, "Заголовок канала."),
    "contacts.telegram_sub": TextLimit(40, "Подпись под каналом."),
    "contacts.form_label": TextLimit(24, "Подпись формы."),
    "privacy.title": TextLimit(48, "Заголовок страницы."),
    "privacy.body": TextLimit(0, "Юридический текст без жёсткого лимита. Абзацы до 600 символов читаются лучше."),
    "nav.about": TextLimit(14, "Пункт меню в шапке в одну строку."),
    "nav.gallery": TextLimit(14, "Пункт меню в шапке в одну строку."),
    "nav.services": TextLimit(14, "Пункт меню в шапке в одну строку."),
    "nav.reviews": TextLimit(14, "Пункт меню в шапке в одну строку."),
    "nav.faq": TextLimit(14, "Пункт меню в шапке в одну строку."),
    "nav.contact": TextLimit(14, "Пункт меню в шапке в одну строку."),
    "header.cta": TextLimit(18, "Кнопка в шапке, без переноса."),
    "header.brand_line_1": TextLimit(16, "Первая строка имени в шапке."),
    "header.brand_line_2": TextLimit(16, "Вторая строка имени в шапке."),
    "header.brand_aria": TextLimit(40, "Скрытая подпись для доступности."),
    "header.nav_aria": TextLimit(40, "Скрытая подпись для доступности."),
    "header.menu_aria": TextLimit(40, "Скрытая подпись для доступности."),
    "mobile.nav_aria": TextLimit(40, "Скрытая подпись для доступности."),
    "mobile.close": TextLimit(16, "Кнопка закрытия меню."),
    "lang.aria": TextLimit(40, "Скрытая подпись для доступности."),
    "dock.aria": TextLimit(40, "Скрытая подпись для доступности."),
    "dock.home": TextLimit(12, "Подпись в нижней панели телефона."),
    "dock.gallery": TextLimit(12, "Подпись в нижней панели телефона."),
    "dock.contacts": TextLimit(12, "Подпись в нижней панели телефона."),
    "footer.brand": TextLimit(24, "Имя в подвале."),
    "footer.location_label": TextLimit(18, "Подпись колонки."),
    "footer.contact_label": TextLimit(18, "Подпись колонки."),
    "footer.menu_label": TextLimit(18, "Подпись колонки."),
    "footer.menu_aria": TextLimit(40, "Скрытая подпись для доступности."),
    "footer.telegram_title": TextLimit(24, "Заголовок канала."),
    "footer.telegram_sub": TextLimit(40, "Подпись под каналом."),
    "footer.menu_more": TextLimit(18, "Пункт меню."),
    "footer.privacy_1": TextLimit(28, "Первая строка ссылки на политику."),
    "footer.privacy_2": TextLimit(28, "Вторая строка ссылки на политику."),
    "form.name": TextLimit(18, "Подпись поля."),
    "form.contact": TextLimit(24, "Подпись поля."),
    "form.message": TextLimit(24, "Подпись поля."),
    "form.consent_prefix": TextLimit(80, "Текст согласия до ссылки на политику."),
    "form.privacy_link": TextLimit(28, "Текст ссылки в согласии."),
    "form.submit": TextLimit(22, "Текст кнопки отправки."),
    "form.service_hint": TextLimit(40, "Подсказка про выбранный формат."),
    "form.honeypot": TextLimit(24, "Скрытое поле, на сайте не видно."),
    "ui.close": TextLimit(16, "Кнопка закрытия окна."),
    "lead.modal_title": TextLimit(36, "Заголовок окна заявки."),
    "lead.success_title": TextLimit(36, "Заголовок после отправки."),
    "lead.success_text": TextLimit(120, "Текст после отправки."),
    "review.modal_title": TextLimit(36, "Заголовок окна отзыва."),
    "review.form_name": TextLimit(18, "Подпись поля."),
    "review.form_rating": TextLimit(18, "Подпись поля."),
    "review.form_text": TextLimit(24, "Подпись поля."),
    "review.submit": TextLimit(22, "Текст кнопки."),
    "review.success_title": TextLimit(36, "Заголовок после отправки."),
    "review.success_text": TextLimit(120, "Текст после отправки."),
    "review.cta": TextLimit(22, "Кнопка оставить отзыв."),
    "review.more": TextLimit(16, "«Ещё» у длинного отзыва."),
    "review.less": TextLimit(16, "«Свернуть» у длинного отзыва."),
    "gallery.open": TextLimit(24, "Подпись открытия кадра."),
    "gallery.prev": TextLimit(16, "Стрелка назад."),
    "gallery.next": TextLimit(16, "Стрелка вперёд."),
    "lightbox.close": TextLimit(16, "Закрыть просмотр."),
    "lightbox.prev": TextLimit(16, "Предыдущий кадр."),
    "lightbox.next": TextLimit(16, "Следующий кадр."),
    "carousel.prev": TextLimit(16, "Стрелка карусели."),
    "carousel.next": TextLimit(16, "Стрелка карусели."),
    "personality.portrait_alt": TextLimit(80, "Alt портрета, на экране не видно."),
    "chat.title": TextLimit(24, "Заголовок панели чата."),
    "chat.subtitle": TextLimit(40, "Подзаголовок панели."),
    "chat.open": TextLimit(16, "Кнопка открытия."),
    "chat.close": TextLimit(16, "Кнопка закрытия."),
    "chat.panel_aria": TextLimit(40, "Скрытая подпись для доступности."),
    "chat.input_label": TextLimit(24, "Подпись поля ввода."),
    "chat.placeholder": TextLimit(36, "Подсказка внутри поля."),
    "chat.send": TextLimit(16, "Кнопка отправки."),
    "chat.empty": TextLimit(80, "Текст пустого чата."),
    "chat.error_rate": TextLimit(80, "Сообщение об ошибке."),
    "chat.error_session": TextLimit(80, "Сообщение об ошибке."),
    "chat.error_send": TextLimit(80, "Сообщение об ошибке."),
    "error.404_text": TextLimit(90, "Текст на странице 404, колонка ≈36 знаков."),
    "error.404_cta": TextLimit(22, "Кнопка возврата."),
    "error.500_text": TextLimit(90, "Текст на странице ошибки, колонка ≈36 знаков."),
    "error.500_cta": TextLimit(22, "Кнопка возврата."),
    "settings.brand_name": TextLimit(24, "Имя бренда, где нет отдельного логотипа."),
    "settings.copyright_name": TextLimit(28, "Имя в копирайте подвала."),
    "settings.location": TextLimit(48, "Адрес / локация в подвале."),
    "seo.title": TextLimit(60, "Title вкладки и поиска. Лучше 50–60."),
    "seo.description": TextLimit(
        160,
        "Краткое описание для поисковиков и соцсетей. Лучше 140–160 символов.",
    ),
}

_SUFFIX_LIMITS: tuple[tuple[str, TextLimit], ...] = (
    (".eyebrow", TextLimit(18, "Короткий надзаголовок.")),
    (".title_accent", TextLimit(28, "Вторая часть заголовка.")),
    (".cta_primary", TextLimit(22, "Текст кнопки.")),
    (".cta_secondary", TextLimit(22, "Текст кнопки.")),
    (".cta", TextLimit(22, "Текст кнопки.")),
    (".title", TextLimit(32, "Заголовок.")),
    (".lead", TextLimit(220, "Короткий абзац.")),
)


def join_help(*parts: str) -> str:
    return " ".join(part.strip() for part in parts if part and part.strip())


def field_guideline_key(
    field_name: str,
    *,
    prefix: str = "",
    mapping: dict[str, str] | None = None,
) -> str:
    if mapping and field_name in mapping:
        return mapping[field_name]
    base = field_name
    for suffix in ("_ru", "_en"):
        if base.endswith(suffix):
            base = base[: -len(suffix)]
            break
    if prefix:
        return f"{prefix}.{base}"
    return base


def image_help(key: str) -> str:
    profile = IMAGE_PROFILES.get(key)
    return profile.as_help() if profile else ""


def text_help(key: str) -> str:
    limit = TEXT_LIMITS.get(key)
    if limit is None:
        for suffix, fallback in _SUFFIX_LIMITS:
            if key.endswith(suffix):
                limit = fallback
                break
    if limit is None:
        return ""
    if limit.chars <= 0:
        return limit.note
    return limit.as_help()


def guideline_help(key: str) -> str:
    return image_help(key) or text_help(key)


class AdminGuidelinesMixin:
    """Attach layout-safe help_text to ModelAdmin / Inline fields."""

    guidelines_prefix: str = ""
    guidelines_field_map: dict[str, str] = {}

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        key = field_guideline_key(
            db_field.name,
            prefix=self.guidelines_prefix,
            mapping=self.guidelines_field_map,
        )
        hint = guideline_help(key)
        if hint:
            existing = kwargs.get("help_text") or getattr(db_field, "help_text", "")
            kwargs["help_text"] = join_help(str(existing) if existing else "", hint)
        return super().formfield_for_dbfield(db_field, request, **kwargs)
