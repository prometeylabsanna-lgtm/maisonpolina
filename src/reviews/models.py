from django.db import models

from src.core.mixins import BilingualTextMixin


class Testimonial(BilingualTextMixin, models.Model):
    author_name = models.CharField(max_length=128)
    role_ru = models.CharField(max_length=255, blank=True)
    role_en = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to="reviews/", blank=True)
    text_ru = models.TextField()
    text_en = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "pk"]
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"

    def __str__(self) -> str:
        return self.author_name

    @property
    def role(self) -> str:
        return self.get_text("role")

    @property
    def text(self) -> str:
        return self.get_text("text")
