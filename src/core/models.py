from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from src.core.fill_style import FillType, validate_hex_color
from src.core.mixins import BilingualTextMixin


def _hex_field(**kwargs):
    return models.CharField(
        max_length=7,
        blank=True,
        default="",
        validators=[validate_hex_color],
        **kwargs,
    )


def _fill_type_field(verbose_name: str):
    return models.CharField(
        max_length=16,
        choices=FillType.choices,
        blank=True,
        default="",
        verbose_name=verbose_name,
    )


def _angle_field(verbose_name: str):
    return models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        default=180,
        validators=[MinValueValidator(0), MaxValueValidator(360)],
        verbose_name=verbose_name,
    )


class SiteSettings(models.Model):
    brand_name = models.CharField(max_length=128, default="MAISON POLINA")
    logo = models.ImageField(upload_to="brand/", blank=True)
    phone = models.CharField(max_length=64, blank=True, default="+380 95 472 7859")
    email = models.EmailField(blank=True, default="hello@example.com")
    telegram_url = models.URLField(blank=True, default="https://t.me/")
    instagram_url = models.URLField(blank=True, default="https://instagram.com/")
    whatsapp_url = models.URLField(blank=True, default="https://wa.me/")
    copyright_name = models.CharField(max_length=128, default="MAISON POLINA")
    location_ru = models.CharField(max_length=255, blank=True, default="ЖК «Нова Конча-Заспа»")
    location_en = models.CharField(max_length=255, blank=True, default="Nova Koncha-Zaspa RC")

    class Meta:
        verbose_name = "Налаштування сайту"
        verbose_name_plural = "Налаштування сайту"

    def __str__(self) -> str:
        return self.brand_name

    @classmethod
    def get_solo(cls) -> "SiteSettings":
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def get_location(self) -> str:
        from django.utils.translation import get_language

        lang = (get_language() or "ru")[:2]
        value = getattr(self, f"location_{lang}", "") or ""
        return value or self.location_ru


class SiteBlock(BilingualTextMixin, models.Model):
    class ContentType(models.TextChoices):
        TEXT = "text", "Текст"
        IMAGE = "image", "Фото"

    class Page(models.TextChoices):
        HOME = "home", "Главная"
        PRIVACY = "privacy", "Политика"
        SITE = "site", "Сайт"

    page = models.CharField(max_length=32, choices=Page.choices, verbose_name="Страница")
    key = models.CharField(max_length=64, verbose_name="Ключ блока")
    label = models.CharField(max_length=128, blank=True, verbose_name="Название в админке")
    content_type = models.CharField(
        max_length=16,
        choices=ContentType.choices,
        default=ContentType.TEXT,
        verbose_name="Тип контента",
    )
    text_ru = models.TextField(blank=True, verbose_name="Текст RU")
    text_en = models.TextField(blank=True, verbose_name="Текст EN")
    image = models.ImageField(upload_to="blocks/", blank=True, verbose_name="Изображение")
    video_file = models.FileField(upload_to="blocks/video/", blank=True)
    video_url = models.URLField(blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Блок контента"
        verbose_name_plural = "Блоки контента"
        constraints = [
            models.UniqueConstraint(fields=["page", "key"], name="unique_site_block_page_key"),
        ]
        ordering = ["page", "sort_order", "key"]

    def __str__(self) -> str:
        return f"{self.get_page_display()} · {self.label or self.key}"

    @property
    def cache_key(self) -> str:
        return f"{self.page}.{self.key}"

    def get_text_value(self) -> str:
        return self.get_text("text")

    def visibility_on(self) -> bool:
        return self.text_ru.strip() in {"1", "true", "True"}


class SeoMeta(BilingualTextMixin, models.Model):
    page = models.CharField(max_length=64, unique=True)
    title_ru = models.CharField(max_length=255, blank=True)
    title_en = models.CharField(max_length=255, blank=True)
    description_ru = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    og_image = models.ImageField(upload_to="seo/", blank=True)

    class Meta:
        verbose_name = "SEO"
        verbose_name_plural = "SEO"

    def __str__(self) -> str:
        return self.page


# Proxy models for CMS section screens
class HomeHeroSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Главная — Hero"
        verbose_name_plural = "Главная — Hero"


class HomeAboutSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Главная — Обо мне"
        verbose_name_plural = "Главная — Обо мне"


class HomePersonalitySettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Главная — Личность"
        verbose_name_plural = "Главная — Личность"


class HomeGallerySettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Главная — Галерея"
        verbose_name_plural = "Главная — Галерея"


class HomeFormatsSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Главная — Форматы"
        verbose_name_plural = "Главная — Форматы"


class HomeTestimonialsSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Главная — Отзывы"
        verbose_name_plural = "Главная — Отзывы"


class HomeFaqSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Главная — Вопросы"
        verbose_name_plural = "Главная — Вопросы"


class HomeContactsSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Главная — Контакты"
        verbose_name_plural = "Главная — Контакты"


class PrivacySettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Политика конфиденциальности"
        verbose_name_plural = "Политика конфиденциальности"


class SiteHeaderSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Шапка"
        verbose_name_plural = "Шапка"


class SiteFooterSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Подвал"
        verbose_name_plural = "Подвал"


class SiteUiSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Интерфейс и формы"
        verbose_name_plural = "Интерфейс и формы"


class SiteChatSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Чат"
        verbose_name_plural = "Чат"


class SiteErrorsSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Страницы ошибок"
        verbose_name_plural = "Страницы ошибок"


class ThemeStylesSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Стили"
        verbose_name_plural = "Стили"


class SectionStyle(models.Model):
    """Per-section background and button fills. Empty fields → CSS tokens."""

    class Section(models.TextChoices):
        HEADER = "header", "Шапка"
        HERO = "hero", "Hero"
        ABOUT = "about", "Про мене"
        PERSONALITY = "personality", "Особистість"
        GALLERY = "gallery", "Галерея"
        FORMATS = "formats", "Формати"
        TESTIMONIALS = "testimonials", "Відгуки"
        FAQ = "faq", "Питання"
        CONTACTS = "contacts", "Контакти"
        FOOTER = "footer", "Підвал"

    section = models.CharField(
        max_length=32,
        unique=True,
        choices=Section.choices,
    )
    label = models.CharField(max_length=128, blank=True)

    bg_fill_type = _fill_type_field("Фон — тип")
    bg_solid_color = _hex_field(verbose_name="Фон — колір")
    bg_gradient_start = _hex_field(verbose_name="Фон — градієнт від")
    bg_gradient_end = _hex_field(verbose_name="Фон — градієнт до")
    bg_gradient_angle = _angle_field("Фон — кут")

    btn_primary_fill_type = _fill_type_field("Primary — тип")
    btn_primary_solid_color = _hex_field(verbose_name="Primary — колір")
    btn_primary_gradient_start = _hex_field(verbose_name="Primary — градієнт від")
    btn_primary_gradient_end = _hex_field(verbose_name="Primary — градієнт до")
    btn_primary_gradient_angle = _angle_field("Primary — кут")

    btn_secondary_fill_type = _fill_type_field("Secondary — тип")
    btn_secondary_solid_color = _hex_field(verbose_name="Secondary — колір")
    btn_secondary_gradient_start = _hex_field(verbose_name="Secondary — градієнт від")
    btn_secondary_gradient_end = _hex_field(verbose_name="Secondary — градієнт до")
    btn_secondary_gradient_angle = _angle_field("Secondary — кут")

    btn_header_fill_type = _fill_type_field("Header CTA — тип")
    btn_header_solid_color = _hex_field(verbose_name="Header CTA — колір")
    btn_header_gradient_start = _hex_field(verbose_name="Header CTA — градієнт від")
    btn_header_gradient_end = _hex_field(verbose_name="Header CTA — градієнт до")
    btn_header_gradient_angle = _angle_field("Header CTA — кут")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Стиль секції"
        verbose_name_plural = "Стилі секцій"
        ordering = ["section"]

    def __str__(self) -> str:
        return self.label or self.get_section_display()

    def bg_css(self) -> str | None:
        from src.core.fill_style import resolve_fill

        return resolve_fill(
            fill_type=self.bg_fill_type,
            solid_color=self.bg_solid_color,
            gradient_start=self.bg_gradient_start,
            gradient_end=self.bg_gradient_end,
            gradient_angle=self.bg_gradient_angle,
        )

    def btn_primary_css(self) -> str | None:
        from src.core.fill_style import resolve_fill

        return resolve_fill(
            fill_type=self.btn_primary_fill_type,
            solid_color=self.btn_primary_solid_color,
            gradient_start=self.btn_primary_gradient_start,
            gradient_end=self.btn_primary_gradient_end,
            gradient_angle=self.btn_primary_gradient_angle,
        )

    def btn_secondary_css(self) -> str | None:
        from src.core.fill_style import resolve_fill

        return resolve_fill(
            fill_type=self.btn_secondary_fill_type,
            solid_color=self.btn_secondary_solid_color,
            gradient_start=self.btn_secondary_gradient_start,
            gradient_end=self.btn_secondary_gradient_end,
            gradient_angle=self.btn_secondary_gradient_angle,
        )

    def btn_header_css(self) -> str | None:
        from src.core.fill_style import resolve_fill

        return resolve_fill(
            fill_type=self.btn_header_fill_type,
            solid_color=self.btn_header_solid_color,
            gradient_start=self.btn_header_gradient_start,
            gradient_end=self.btn_header_gradient_end,
            gradient_angle=self.btn_header_gradient_angle,
        )
