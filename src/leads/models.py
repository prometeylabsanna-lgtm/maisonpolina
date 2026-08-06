from django.db import models
from django.utils import timezone


class LeadSource(models.TextChoices):
    HEADER = "header", "Шапка"
    HERO = "hero", "Перший екран"
    ABOUT = "about", "Про мене"
    FORMATS = "formats", "Формати"
    FAQ = "faq", "Питання"
    CONTACTS = "contacts", "Контакти"


class LeadStatus(models.TextChoices):
    NEW = "new", "Нова"
    IN_PROGRESS = "in_progress", "В роботі"
    WON = "won", "Успішна"
    LOST = "lost", "Відхилена"


class Lead(models.Model):
    name = models.CharField(max_length=128)
    contact = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    service = models.CharField(max_length=255, blank=True)
    source = models.CharField(
        max_length=32,
        choices=LeadSource.choices,
        default=LeadSource.CONTACTS,
    )
    language = models.CharField(max_length=8, default="ru")
    status = models.CharField(
        max_length=32,
        choices=LeadStatus.choices,
        default=LeadStatus.NEW,
    )
    admin_note = models.TextField(blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=512, blank=True)
    utm_source = models.CharField(max_length=128, blank=True)
    utm_medium = models.CharField(max_length=128, blank=True)
    utm_campaign = models.CharField(max_length=128, blank=True)
    notified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self) -> str:
        return f"{self.name} — {self.contact}"

    def mark_notified(self) -> None:
        self.notified_at = timezone.now()
        self.save(update_fields=["notified_at"])
