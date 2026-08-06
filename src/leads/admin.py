import csv

from django.contrib import admin, messages
from django.http import HttpResponse
from unfold.admin import ModelAdmin

from src.leads.models import Lead, LeadStatus


@admin.action(description="Позначити «В роботі»")
def mark_in_progress(modeladmin, request, queryset):
    updated = queryset.update(status=LeadStatus.IN_PROGRESS)
    messages.success(request, f"Оновлено: {updated}")


@admin.action(description="Позначити «Успішна»")
def mark_won(modeladmin, request, queryset):
    updated = queryset.update(status=LeadStatus.WON)
    messages.success(request, f"Оновлено: {updated}")


@admin.action(description="Позначити «Відхилена»")
def mark_lost(modeladmin, request, queryset):
    updated = queryset.update(status=LeadStatus.LOST)
    messages.success(request, f"Оновлено: {updated}")


@admin.action(description="Експорт у CSV")
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
class LeadAdmin(ModelAdmin):
    list_display = (
        "created_at",
        "name",
        "contact",
        "service",
        "source",
        "language",
        "status",
        "notified_at",
    )
    list_filter = ("status", "source", "language", "created_at")
    search_fields = ("name", "contact", "service", "message")
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
        (None, {"fields": ("name", "contact", "message", "service", "source", "language")}),
        ("Статус", {"fields": ("status", "admin_note", "notified_at")}),
        (
            "Технічне",
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
            },
        ),
    )
