from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from src.core.mixins import BilingualTextMixin


class Testimonial(BilingualTextMixin, models.Model):
    author_name_ru = models.CharField(max_length=128)
    author_name_en = models.CharField(max_length=128, blank=True)
    role_ru = models.CharField(max_length=255, blank=True)
    role_en = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to="reviews/", blank=True)
    text_ru = models.TextField(blank=True)
    text_en = models.TextField(blank=True)
    rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(
        default=True,
        help_text="На сайті показуються лише активні (схвалені) відгуки.",
    )
    is_public_submission = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ["order", "-created_at", "pk"]
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"

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
