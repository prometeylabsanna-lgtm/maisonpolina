from django.db import models
from django.utils import timezone


class LeadSource(models.TextChoices):
    HEADER = "header", "Шапка"
    HERO = "hero", "Первый экран"
    ABOUT = "about", "Обо мне"
    FORMATS = "formats", "Форматы"
    FAQ = "faq", "Вопросы"
    CONTACTS = "contacts", "Контакты"


class LeadStatus(models.TextChoices):
    NEW = "new", "Новая"
    IN_PROGRESS = "in_progress", "В работе"
    WON = "won", "Успешная"
    LOST = "lost", "Отклонена"


class Lead(models.Model):
    name = models.CharField(max_length=128, verbose_name="Имя")
    contact = models.CharField(max_length=255, verbose_name="Контакт")
    message = models.TextField(blank=True, verbose_name="Сообщение")
    service = models.CharField(max_length=255, blank=True, verbose_name="Услуга")
    source = models.CharField(
        max_length=32,
        choices=LeadSource.choices,
        default=LeadSource.CONTACTS,
        verbose_name="Источник",
    )
    language = models.CharField(max_length=8, default="ru", verbose_name="Язык")
    status = models.CharField(
        max_length=32,
        choices=LeadStatus.choices,
        default=LeadStatus.NEW,
        verbose_name="Статус",
    )
    admin_note = models.TextField(blank=True, verbose_name="Заметка")
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP")
    user_agent = models.CharField(max_length=512, blank=True, verbose_name="User-Agent")
    utm_source = models.CharField(max_length=128, blank=True, verbose_name="utm_source")
    utm_medium = models.CharField(max_length=128, blank=True, verbose_name="utm_medium")
    utm_campaign = models.CharField(
        max_length=128, blank=True, verbose_name="utm_campaign"
    )
    notified_at = models.DateTimeField(null=True, blank=True, verbose_name="Уведомление")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self) -> str:
        return f"{self.name} — {self.contact}"

    def mark_notified(self) -> None:
        self.notified_at = timezone.now()
        self.save(update_fields=["notified_at"])
