from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from src.chat.models import ChatMessage, TelegramChatSession


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
class TelegramChatSessionAdmin(ModelAdmin):
    list_display = (
        "session_id",
        "user_identifier",
        "status",
        "telegram_chat_id",
        "created_at",
        "updated_at",
    )
    list_filter = ("status",)
    search_fields = ("session_id", "user_identifier")
    readonly_fields = ("session_id", "created_at", "updated_at")
    inlines = [ChatMessageInline]


@admin.register(ChatMessage)
class ChatMessageAdmin(ModelAdmin):
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
