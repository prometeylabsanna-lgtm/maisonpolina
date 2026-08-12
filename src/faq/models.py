from django.db import models

from src.core.mixins import BilingualTextMixin


class FaqItem(BilingualTextMixin, models.Model):
    question_ru = models.CharField(max_length=255, verbose_name="Вопрос")
    question_en = models.CharField(max_length=255, blank=True, verbose_name="Вопрос")
    answer_ru = models.TextField(verbose_name="Ответ")
    answer_en = models.TextField(blank=True, verbose_name="Ответ")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

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
