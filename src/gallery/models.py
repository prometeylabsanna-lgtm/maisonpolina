from django.db import models

from src.core.mixins import BilingualTextMixin


class GalleryPhoto(BilingualTextMixin, models.Model):
    image = models.ImageField(upload_to="gallery/")
    alt_ru = models.CharField(max_length=255, blank=True)
    alt_en = models.CharField(max_length=255, blank=True)
    caption_ru = models.CharField(max_length=255, blank=True)
    caption_en = models.CharField(max_length=255, blank=True)
    col_span = models.PositiveSmallIntegerField(default=1)
    row_span = models.PositiveSmallIntegerField(default=2)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "pk"]
        verbose_name = "Фото галереї"
        verbose_name_plural = "Галерея"

    def __str__(self) -> str:
        return self.caption_ru or f"Photo {self.pk}"

    @property
    def alt(self) -> str:
        return self.get_text("alt")

    @property
    def caption(self) -> str:
        return self.get_text("caption")
