from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from src.core.fields import WebPImageField
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


def _fill_type_field(verbose_name: str, **kwargs):
    return models.CharField(
        max_length=16,
        choices=FillType.choices,
        blank=True,
        default="",
        verbose_name=verbose_name,
        **kwargs,
    )


def _angle_field(verbose_name: str, **kwargs):
    return models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        default=180,
        validators=[MinValueValidator(0), MaxValueValidator(360)],
        verbose_name=verbose_name,
        help_text=kwargs.pop(
            "help_text",
            "От 0 до 360. Например, 180 — сверху вниз.",
        ),
        **kwargs,
    )


class SiteSettings(models.Model):
    brand_name = models.CharField(
        max_length=128, default="MAISON POLINA", verbose_name="Название бренда"
    )
    logo = WebPImageField(upload_to="brand/", blank=True, verbose_name="Логотип")
    phone = models.CharField(
        max_length=64, blank=True, default="+380 95 472 2029", verbose_name="Телефон"
    )
    email = models.EmailField(
        blank=True, default="hello@example.com", verbose_name="Email"
    )
    telegram_url = models.URLField(
        blank=True, default="https://t.me/", verbose_name="Telegram"
    )
    instagram_url = models.URLField(
        blank=True, default="https://instagram.com/", verbose_name="Instagram"
    )
    whatsapp_url = models.URLField(
        blank=True, default="https://wa.me/", verbose_name="WhatsApp"
    )
    copyright_name = models.CharField(
        max_length=128, default="MAISON POLINA", verbose_name="Имя в копирайте"
    )
    location_ru = models.CharField(
        max_length=255,
        blank=True,
        default="ЖК «Нова Конча-Заспа»",
        verbose_name="Адрес / локация",
    )
    location_en = models.CharField(
        max_length=255,
        blank=True,
        default="Nova Koncha-Zaspa RC",
        verbose_name="Адрес / локация",
    )

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

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

    def get_whatsapp_url(self) -> str:
        url = (self.whatsapp_url or "").strip()
        if not url:
            return ""
        bare = url.rstrip("/").lower()
        if bare in {
            "https://wa.me",
            "http://wa.me",
            "https://www.wa.me",
            "http://www.wa.me",
            "https://api.whatsapp.com/send",
            "http://api.whatsapp.com/send",
        }:
            return ""
        return url


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
    image = WebPImageField(upload_to="blocks/", blank=True, verbose_name="Изображение")
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

    def get_video_src(self) -> str:
        if self.video_file:
            try:
                return self.video_file.url
            except ValueError:
                pass
        url = (self.video_url or "").strip()
        if not url:
            return ""
        lower = url.lower()
        if any(host in lower for host in ("youtube.com", "youtu.be", "vimeo.com")):
            return ""
        return url


class PersonalityItem(BilingualTextMixin, models.Model):
    """Dynamic label+value rows for personality facts / extras."""

    class Group(models.TextChoices):
        FACTS = "facts", "Внешность"
        EXTRAS = "extras", "Дополнительно"

    group = models.CharField(
        max_length=16,
        choices=Group.choices,
        db_index=True,
        verbose_name="Группа",
    )
    label_ru = models.CharField(max_length=128, blank=True, verbose_name="Название")
    label_en = models.CharField(max_length=128, blank=True, verbose_name="Название")
    value_ru = models.CharField(max_length=255, blank=True, verbose_name="Значение")
    value_en = models.CharField(max_length=255, blank=True, verbose_name="Значение")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        ordering = ["group", "order", "pk"]
        verbose_name = "Пункт личности"
        verbose_name_plural = "Пункты личности"

    def __str__(self) -> str:
        return self.label_ru or self.value_ru or f"Item {self.pk}"

    @property
    def label(self) -> str:
        return self.get_text("label")

    @property
    def value(self) -> str:
        return self.get_text("value")


class SeoMeta(BilingualTextMixin, models.Model):
    page = models.CharField(max_length=64, unique=True, verbose_name="Страница")
    title_ru = models.CharField(max_length=255, blank=True, verbose_name="Заголовок")
    title_en = models.CharField(max_length=255, blank=True, verbose_name="Заголовок")
    description_ru = models.TextField(blank=True, verbose_name="Описание")
    description_en = models.TextField(blank=True, verbose_name="Описание")
    og_image = WebPImageField(
        upload_to="seo/", blank=True, verbose_name="Картинка для соцсетей"
    )

    class Meta:
        verbose_name = "SEO"
        verbose_name_plural = "SEO"

    def __str__(self) -> str:
        return self.page


# Proxy models for CMS section screens
class HomeHeroSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Баннер"
        verbose_name_plural = "Баннер"


class HomeAboutSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Восемь лет ярких впечатлений"
        verbose_name_plural = "Восемь лет ярких впечатлений"


class HomePersonalitySettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Дополнительная информация"
        verbose_name_plural = "Дополнительная информация"


class HomeGallerySettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Галерея"
        verbose_name_plural = "Галерея"


class HomeFormatsSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Услуги"
        verbose_name_plural = "Услуги"


class HomeTestimonialsSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Отзывы"
        verbose_name_plural = "Отзывы"


class HomeFaqSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Вопросы"
        verbose_name_plural = "Вопросы"


class HomeContactsSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Заявка"
        verbose_name_plural = "Заявка"


class PrivacySettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Политика конфиденциальности"
        verbose_name_plural = "Политика конфиденциальности"


class SiteHeaderSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Шапка профиля"
        verbose_name_plural = "Шапка профиля"


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
        verbose_name = "Цвета и кнопки"
        verbose_name_plural = "Цвета и кнопки"


class SectionStyle(models.Model):
    """Per-section background and button fills. Empty fields → CSS tokens."""

    class Section(models.TextChoices):
        HEADER = "header", "Шапка"
        HERO = "hero", "Первый экран (Hero)"
        ABOUT = "about", "Обо мне"
        PERSONALITY = "personality", "Личность"
        GALLERY = "gallery", "Галерея"
        FORMATS = "formats", "Форматы"
        TESTIMONIALS = "testimonials", "Отзывы"
        FAQ = "faq", "Вопросы"
        CONTACTS = "contacts", "Контакты"
        FOOTER = "footer", "Подвал"

    section = models.CharField(
        max_length=32,
        unique=True,
        choices=Section.choices,
        verbose_name="Секция",
    )
    label = models.CharField(
        max_length=128,
        blank=True,
        verbose_name="Название",
        help_text="Как секция называется в списке ниже.",
    )

    bg_fill_type = _fill_type_field("Фон: как залить")
    bg_solid_color = _hex_field(
        verbose_name="Фон: цвет",
        help_text="Если выбран «Один цвет». Пример: #4c0d13",
    )
    bg_gradient_start = _hex_field(
        verbose_name="Фон: градиент — начало",
        help_text="Первый цвет градиента.",
    )
    bg_gradient_end = _hex_field(
        verbose_name="Фон: градиент — конец",
        help_text="Второй цвет градиента.",
    )
    bg_gradient_angle = _angle_field("Фон: угол градиента (°)")

    btn_primary_fill_type = _fill_type_field("Главная кнопка: как залить")
    btn_primary_solid_color = _hex_field(verbose_name="Главная кнопка: цвет")
    btn_primary_gradient_start = _hex_field(verbose_name="Главная кнопка: градиент — начало")
    btn_primary_gradient_end = _hex_field(verbose_name="Главная кнопка: градиент — конец")
    btn_primary_gradient_angle = _angle_field("Главная кнопка: угол градиента (°)")

    btn_secondary_fill_type = _fill_type_field("Вторая кнопка: как залить")
    btn_secondary_solid_color = _hex_field(verbose_name="Вторая кнопка: цвет")
    btn_secondary_gradient_start = _hex_field(verbose_name="Вторая кнопка: градиент — начало")
    btn_secondary_gradient_end = _hex_field(verbose_name="Вторая кнопка: градиент — конец")
    btn_secondary_gradient_angle = _angle_field("Вторая кнопка: угол градиента (°)")

    btn_header_fill_type = _fill_type_field("Кнопка в шапке: как залить")
    btn_header_solid_color = _hex_field(verbose_name="Кнопка в шапке: цвет")
    btn_header_gradient_start = _hex_field(verbose_name="Кнопка в шапке: градиент — начало")
    btn_header_gradient_end = _hex_field(verbose_name="Кнопка в шапке: градиент — конец")
    btn_header_gradient_angle = _angle_field("Кнопка в шапке: угол градиента (°)")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Стиль секции"
        verbose_name_plural = "Стили секций"
        ordering = ["section"]

    def __str__(self) -> str:
        return self.label or self.get_section_display()

    def _fill_css(self, prefix: str) -> str | None:
        from src.core.fill_style import resolve_fill

        return resolve_fill(
            fill_type=getattr(self, f"{prefix}fill_type"),
            solid_color=getattr(self, f"{prefix}solid_color"),
            gradient_start=getattr(self, f"{prefix}gradient_start"),
            gradient_end=getattr(self, f"{prefix}gradient_end"),
            gradient_angle=getattr(self, f"{prefix}gradient_angle"),
        )

    def bg_css(self) -> str | None:
        return self._fill_css("bg_")

    def btn_primary_css(self) -> str | None:
        return self._fill_css("btn_primary_")

    def btn_secondary_css(self) -> str | None:
        return self._fill_css("btn_secondary_")

    def btn_header_css(self) -> str | None:
        return self._fill_css("btn_header_")


class StoredMedia(models.Model):
    """Persistent file bytes for Vercel (no local disk)."""

    name = models.CharField(max_length=255, unique=True, db_index=True)
    content = models.BinaryField()
    content_type = models.CharField(max_length=64, blank=True, default="")
    size = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"

    def __str__(self) -> str:
        return self.name
