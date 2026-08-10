from django.db import models

from src.core.mixins import BilingualTextMixin


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
    class Page(models.TextChoices):
        HOME = "home", "Головна"
        PRIVACY = "privacy", "Політика"
        SITE = "site", "Сайт"

    page = models.CharField(max_length=32, choices=Page.choices)
    key = models.CharField(max_length=64)
    label = models.CharField(max_length=128, blank=True)
    text_ru = models.TextField(blank=True)
    text_en = models.TextField(blank=True)
    image = models.ImageField(upload_to="blocks/", blank=True)
    video_file = models.FileField(upload_to="blocks/video/", blank=True)
    video_url = models.URLField(blank=True)
    is_visible = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Блок вмісту"
        verbose_name_plural = "Блоки вмісту"
        constraints = [
            models.UniqueConstraint(fields=["page", "key"], name="unique_site_block_page_key"),
        ]
        ordering = ["page", "key"]

    def __str__(self) -> str:
        return f"{self.page}.{self.key}"

    @property
    def cache_key(self) -> str:
        return f"{self.page}.{self.key}"

    def get_text_value(self) -> str:
        return self.get_text("text")


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
        verbose_name = "Головна — Hero"
        verbose_name_plural = "Головна — Hero"


class HomeAboutSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Головна — Про мене"
        verbose_name_plural = "Головна — Про мене"


class HomePersonalitySettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Головна — Особистість"
        verbose_name_plural = "Головна — Особистість"


class HomeGallerySettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Головна — Галерея"
        verbose_name_plural = "Головна — Галерея"


class HomeFormatsSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Головна — Формати"
        verbose_name_plural = "Головна — Формати"


class HomeTestimonialsSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Головна — Відгуки"
        verbose_name_plural = "Головна — Відгуки"


class HomeFaqSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Головна — Питання"
        verbose_name_plural = "Головна — Питання"


class HomeContactsSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Головна — Контакти"
        verbose_name_plural = "Головна — Контакти"


class PrivacySettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Політика конфіденційності"
        verbose_name_plural = "Політика конфіденційності"
