from django.db import models

from src.core.mixins import BilingualTextMixin


class ServiceFormat(BilingualTextMixin, models.Model):
    title_ru = models.CharField(max_length=128)
    title_en = models.CharField(max_length=128, blank=True)
    description_ru = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    price_text_ru = models.CharField(max_length=128, blank=True)
    price_text_en = models.CharField(max_length=128, blank=True)
    label_ru = models.CharField(max_length=64, blank=True, help_text="Напр. Формат I")
    label_en = models.CharField(max_length=64, blank=True)
    image = models.ImageField(upload_to="formats/", blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

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
    )
    text_ru = models.CharField(max_length=255)
    text_en = models.CharField(max_length=255, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "pk"]
        verbose_name = "Пункт формату"
        verbose_name_plural = "Пункти формату"

    def __str__(self) -> str:
        return self.text_ru

    @property
    def text(self) -> str:
        return self.get_text("text")
