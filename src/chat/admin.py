from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import path
from django.views.decorators.http import require_POST
from unfold.admin import ModelAdmin, TabularInline

from src.chat.models import ChatMessage, SenderType, SessionStatus, TelegramChatSession
from src.core.admin_changelist import TopDropdownFilterMixin

_MAX_REPLY = 4000


class ChatMessageInline(TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = (
        "sender_type",
        "text",
        "telegram_message_id",
        "created_at",
    )
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(TelegramChatSession)
class TelegramChatSessionAdmin(TopDropdownFilterMixin, ModelAdmin):
    change_form_outer_after_template = "admin/chat/session_reply.html"
    list_display = (
        "session_id",
        "user_identifier",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = ("status",)
    search_fields = ("session_id", "user_identifier")
    readonly_fields = ("session_id", "created_at", "updated_at")
    fields = ("session_id", "user_identifier", "status", "created_at", "updated_at")
    inlines = [ChatMessageInline]

    def get_urls(self):
        custom = [
            path(
                "<path:object_id>/reply/",
                self.admin_site.admin_view(self.reply_view),
                name="chat_telegramchatsession_reply",
            ),
        ]
        return custom + super().get_urls()

    def reply_view(self, request: HttpRequest, object_id: str) -> HttpResponse:
        session = get_object_or_404(TelegramChatSession, pk=object_id)
        if not self.has_change_permission(request, session):
            raise PermissionDenied
        return _save_admin_reply(request, session)


@require_POST
def _save_admin_reply(request: HttpRequest, session: TelegramChatSession) -> HttpResponse:
    change_url = redirect("admin:chat_telegramchatsession_change", session.pk)
    if session.status != SessionStatus.ACTIVE:
        messages.error(request, "Диалог закрыт. Ответ не отправлен.")
        return change_url
    text = (request.POST.get("admin_reply") or "").strip()
    if not text:
        messages.error(request, "Введите текст ответа.")
        return change_url
    ChatMessage.objects.create(
        session=session,
        sender_type=SenderType.TELEGRAM_ADMIN,
        text=text[:_MAX_REPLY],
    )
    session.save(update_fields=["updated_at"])
    messages.success(request, "Ответ отправлен в чат на сайте.")
    return change_url


@admin.register(ChatMessage)
class ChatMessageAdmin(TopDropdownFilterMixin, ModelAdmin):
    list_display = (
        "id",
        "session",
        "sender_type",
        "telegram_message_id",
        "created_at",
    )
    list_filter = ("sender_type",)
    search_fields = ("text", "session__session_id")
    readonly_fields = ("created_at",)
