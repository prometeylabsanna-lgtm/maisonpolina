from django.db import models
from django.templatetags.static import static

from src.core.fields import WebPImageField
from src.core.mixins import BilingualTextMixin


class GalleryPhoto(BilingualTextMixin, models.Model):
    image = WebPImageField(upload_to="gallery/", blank=True, verbose_name="Фото")
    static_image = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Внутренний файл",
        help_text="Внутренний путь к файлу. Обычно не меняется.",
    )
    alt_ru = models.CharField(max_length=255, blank=True, verbose_name="Описание фото")
    alt_en = models.CharField(max_length=255, blank=True, verbose_name="Описание фото")
    caption_ru = models.CharField(max_length=255, blank=True, verbose_name="Подпись")
    caption_en = models.CharField(max_length=255, blank=True, verbose_name="Подпись")
    col_span = models.PositiveSmallIntegerField(default=1, verbose_name="Ширина")
    row_span = models.PositiveSmallIntegerField(default=2, verbose_name="Высота")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        ordering = ["order", "pk"]
        verbose_name = "Фото галереи"
        verbose_name_plural = "Галерея"

    def __str__(self) -> str:
        return self.caption_ru or self.static_image or f"Photo {self.pk}"

    @property
    def alt(self) -> str:
        return self.get_text("alt")

    @property
    def caption(self) -> str:
        return self.get_text("caption")

    def get_image_url(self) -> str:
        """Prefer shipped static images (Vercel-safe), else media upload.

        If static path is .jpg/.png and a sibling .webp exists, serve WebP.
        """
        if self.static_image:
            path = self.static_image
            lower = path.lower()
            if lower.endswith((".jpg", ".jpeg", ".png")):
                from pathlib import Path

                from django.contrib.staticfiles.finders import find

                webp_path = str(Path(path).with_suffix(".webp"))
                if find(webp_path):
                    return static(webp_path)
            return static(path)
        if self.image:
            try:
                return self.image.url
            except ValueError:
                return ""
        return ""
