from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from src.core.fields import WebPImageField
from src.core.mixins import BilingualTextMixin


class Testimonial(BilingualTextMixin, models.Model):
    author_name_ru = models.CharField(max_length=128, verbose_name="Имя автора")
    author_name_en = models.CharField(
        max_length=128, blank=True, verbose_name="Имя автора"
    )
    role_ru = models.CharField(max_length=255, blank=True, verbose_name="Роль / подпись")
    role_en = models.CharField(max_length=255, blank=True, verbose_name="Роль / подпись")
    photo = WebPImageField(upload_to="reviews/", blank=True, verbose_name="Фото")
    text_ru = models.TextField(blank=True, verbose_name="Текст отзыва")
    text_en = models.TextField(blank=True, verbose_name="Текст отзыва")
    rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Рейтинг",
    )
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активно",
        help_text="На сайте показываются только активные (одобренные) отзывы.",
    )
    is_public_submission = models.BooleanField(
        default=False,
        verbose_name="Публичная заявка",
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата",
    )

    class Meta:
        ordering = ["order", "-created_at", "pk"]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self) -> str:
        return self.author_name_ru or self.author_name_en or f"#{self.pk}"

    @property
    def author_name(self) -> str:
        value = self.get_text("author_name")
        if value:
            return value
        return self.author_name_en or self.author_name_ru or ""

    @property
    def role(self) -> str:
        return self.get_text("role")

    @property
    def text(self) -> str:
        value = self.get_text("text")
        if value:
            return value
        return self.text_en or self.text_ru or ""
