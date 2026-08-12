from django.db import models

from src.core.fields import WebPImageField
from src.core.mixins import BilingualTextMixin


class ServiceFormat(BilingualTextMixin, models.Model):
    title_ru = models.CharField(max_length=128, verbose_name="Название")
    title_en = models.CharField(max_length=128, blank=True, verbose_name="Название")
    description_ru = models.TextField(blank=True, verbose_name="Описание")
    description_en = models.TextField(blank=True, verbose_name="Описание")
    price_text_ru = models.CharField(max_length=128, blank=True, verbose_name="Цена")
    price_text_en = models.CharField(max_length=128, blank=True, verbose_name="Цена")
    label_ru = models.CharField(
        max_length=64,
        blank=True,
        verbose_name="Метка",
        help_text="Напр. Формат I",
    )
    label_en = models.CharField(max_length=64, blank=True, verbose_name="Метка")
    image = WebPImageField(upload_to="formats/", blank=True, verbose_name="Фото")
    is_featured = models.BooleanField(default=False, verbose_name="В избранном")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        ordering = ["order", "pk"]
        verbose_name = "Формат услуги"
        verbose_name_plural = "Форматы услуг"

    def __str__(self) -> str:
        return self.title_ru

    @property
    def title(self) -> str:
        return self.get_text("title")

    @property
    def description(self) -> str:
        return self.get_text("description")

    @property
    def price_text(self) -> str:
        return self.get_text("price_text")

    @property
    def label(self) -> str:
        return self.get_text("label")


class FormatFeature(BilingualTextMixin, models.Model):
    service = models.ForeignKey(
        ServiceFormat,
        on_delete=models.CASCADE,
        related_name="features",
        verbose_name="Формат",
    )
    text_ru = models.CharField(max_length=255, verbose_name="Текст (RU)")
    text_en = models.CharField(max_length=255, blank=True, verbose_name="Текст (EN)")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ["order", "pk"]
        verbose_name = "Пункт формата"
        verbose_name_plural = "Пункты формата"

    def __str__(self) -> str:
        return self.text_ru

    @property
    def text(self) -> str:
        return self.get_text("text")
