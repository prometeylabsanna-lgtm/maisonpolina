from django.db import models

from src.core.mixins import BilingualTextMixin


class FaqItem(BilingualTextMixin, models.Model):
    question_ru = models.CharField(max_length=255)
    question_en = models.CharField(max_length=255, blank=True)
    answer_ru = models.TextField()
    answer_en = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "pk"]
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы и ответы"

    def __str__(self) -> str:
        return self.question_ru

    @property
    def question(self) -> str:
        return self.get_text("question")

    @property
    def answer(self) -> str:
        return self.get_text("answer")
