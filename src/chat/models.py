import uuid

from django.db import models


class SessionStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    CLOSED = "closed", "Closed"


class SenderType(models.TextChoices):
    SITE_USER = "site_user", "Site user"
    TELEGRAM_ADMIN = "telegram_admin", "Telegram admin"
    SYSTEM = "system", "System"


class TelegramChatSession(models.Model):
    session_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    telegram_chat_id = models.BigIntegerField(
        null=True,
        blank=True,
        unique=True,
    )
    user_identifier = models.CharField(max_length=64, db_index=True)
    status = models.CharField(
        max_length=16,
        choices=SessionStatus.choices,
        default=SessionStatus.ACTIVE,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Чат Telegram"
        verbose_name_plural = "Чаты Telegram"

    def __str__(self) -> str:
        return f"{self.session_id} ({self.status})"


class ChatMessage(models.Model):
    session = models.ForeignKey(
        TelegramChatSession,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    sender_type = models.CharField(max_length=32, choices=SenderType.choices)
    text = models.TextField()
    telegram_message_id = models.BigIntegerField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Сообщение чата"
        verbose_name_plural = "Сообщения чата"

    def __str__(self) -> str:
        return f"{self.sender_type}: {self.text[:40]}"
