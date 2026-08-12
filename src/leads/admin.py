import csv

from django.contrib import admin, messages
from django.http import HttpResponse
from unfold.admin import ModelAdmin

from src.core.admin_changelist import TopDropdownFilterMixin
from src.core.admin_tinymce import TinyMCEAdminMixin
from src.core.admin_utils import status_badge
from src.leads.models import Lead, LeadStatus

_STATUS_TONE = {
    LeadStatus.NEW: "info",
    LeadStatus.IN_PROGRESS: "warning",
    LeadStatus.WON: "success",
    LeadStatus.LOST: "danger",
}


@admin.action(description="Отметить «В работе»")
def mark_in_progress(modeladmin, request, queryset):
    updated = queryset.update(status=LeadStatus.IN_PROGRESS)
    messages.success(request, f"Обновлено: {updated}")


@admin.action(description="Отметить «Успешная»")
def mark_won(modeladmin, request, queryset):
    updated = queryset.update(status=LeadStatus.WON)
    messages.success(request, f"Обновлено: {updated}")


@admin.action(description="Отметить «Отклонена»")
def mark_lost(modeladmin, request, queryset):
    updated = queryset.update(status=LeadStatus.LOST)
    messages.success(request, f"Обновлено: {updated}")


@admin.action(description="Экспорт в CSV")
def export_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="leads.csv"'
    response.write("\ufeff")
    writer = csv.writer(response)
    writer.writerow(
        [
            "id",
            "created_at",
            "name",
            "contact",
            "service",
            "source",
            "language",
            "status",
            "message",
            "utm_source",
            "utm_medium",
            "utm_campaign",
        ]
    )
    for lead in queryset:
        writer.writerow(
            [
                lead.pk,
                lead.created_at.isoformat(),
                lead.name,
                lead.contact,
                lead.service,
                lead.source,
                lead.language,
                lead.status,
                lead.message,
                lead.utm_source,
                lead.utm_medium,
                lead.utm_campaign,
            ]
        )
    return response


@admin.register(Lead)
class LeadAdmin(TopDropdownFilterMixin, TinyMCEAdminMixin, ModelAdmin):
    list_display = (
        "created_at",
        "name",
        "contact",
        "service",
        "source",
        "language",
        "status_badge",
        "notified_at",
    )
    list_filter = ("status", "source", "language", "created_at")
    search_fields = ("name", "contact", "service", "message")
    tinymce_fields = ("admin_note",)
    readonly_fields = (
        "created_at",
        "ip",
        "user_agent",
        "utm_source",
        "utm_medium",
        "utm_campaign",
        "notified_at",
    )
    actions = [mark_in_progress, mark_won, mark_lost, export_csv]
    date_hierarchy = "created_at"
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "contact",
                    "message",
                    "service",
                    "source",
                    "language",
                )
            },
        ),
        ("Статус", {"fields": ("status", "admin_note", "notified_at")}),
        (
            "Служебное",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "ip",
                    "user_agent",
                    "utm_source",
                    "utm_medium",
                    "utm_campaign",
                ),
                "description": "Служебные сведения по заявке. Обычно менять не нужно.",
            },
        ),
    )

    @admin.display(description="Статус", ordering="status")
    def status_badge(self, obj):
        return status_badge(
            obj.get_status_display(),
            tone=_STATUS_TONE.get(obj.status, "neutral"),
        )
