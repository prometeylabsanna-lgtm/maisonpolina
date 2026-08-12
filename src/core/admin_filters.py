"""Unfold dropdown filters for changelist (labels in Russian, no «By» prefix)."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.views.main import ChangeList
from django.core.validators import EMPTY_VALUES
from django.db.models import Field, Model, QuerySet
from django.http import HttpRequest

from unfold.contrib.filters.admin.mixins import (
    DropdownMixin,
    ValueMixin,
)
from unfold.contrib.filters.forms import DropdownForm

_ALL = "all"


class _LabeledDropdownMixin:
    """Use field verbose_name as select label (Активно, Рейтинг, …)."""

    def filter_label(self) -> str:
        return str(getattr(self, "title", "") or "").strip()


class BooleanDropdownFilter(_LabeledDropdownMixin, ValueMixin, admin.BooleanFieldListFilter):
    template = "unfold/filters/filters_field.html"
    form_class = DropdownForm

    def choices(self, changelist: ChangeList) -> Iterator:
        current = self.value()
        if current in EMPTY_VALUES:
            current = _ALL
        choices = [
            (_ALL, "Все"),
            ("1", "Да"),
            ("0", "Нет"),
        ]
        yield {
            "form": self.form_class(
                label=self.filter_label(),
                name=self.lookup_kwarg,
                choices=choices,
                data={self.lookup_kwarg: current},
            ),
        }

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet | None:
        value = self.value()
        if value in EMPTY_VALUES or value == _ALL:
            return queryset
        return super().queryset(request, queryset)


class ChoicesDropdownFilter(
    _LabeledDropdownMixin, ValueMixin, DropdownMixin, admin.ChoicesFieldListFilter
):
    all_option = [_ALL, "Все"]

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet | None:
        if self.value() in EMPTY_VALUES or self.value() == _ALL:
            return queryset
        return super().queryset(request, queryset)

    def choices(self, changelist: ChangeList) -> Iterator:
        choices = [self.all_option, *list(self.field.flatchoices)]
        current = self.value()
        if current in EMPTY_VALUES:
            current = _ALL
        yield {
            "form": self.form_class(
                label=self.filter_label(),
                name=self.lookup_kwarg,
                choices=choices,
                data={self.lookup_kwarg: current},
            ),
        }


class AllValuesDropdownFilter(
    _LabeledDropdownMixin, ValueMixin, DropdownMixin, admin.AllValuesFieldListFilter
):
    all_option = [_ALL, "Все"]

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet | None:
        if self.value() in EMPTY_VALUES or self.value() == _ALL:
            return queryset
        return super().queryset(request, queryset)

    def choices(self, changelist: ChangeList) -> Iterator:
        choices = [self.all_option, *[[val, str(val)] for val in self.lookup_choices]]
        current = self.value()
        if current in EMPTY_VALUES:
            current = _ALL
        yield {
            "form": self.form_class(
                label=self.filter_label(),
                name=self.lookup_kwarg,
                choices=choices,
                data={self.lookup_kwarg: current},
            ),
        }


class RelatedDropdownFilter(
    _LabeledDropdownMixin, ValueMixin, DropdownMixin, admin.RelatedFieldListFilter
):
    all_option = ["", "Все"]

    def __init__(
        self,
        field: Field,
        request: HttpRequest,
        params: dict[str, Any],
        model: type[Model],
        model_admin: ModelAdmin,
        field_path: str,
    ) -> None:
        super().__init__(field, request, params, model, model_admin, field_path)
        self.model_admin = model_admin
        self.request = request

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet | None:
        if self.value() in EMPTY_VALUES:
            return queryset
        return super().queryset(request, queryset)

    def choices(self, changelist: ChangeList) -> Iterator:
        choices = [self.all_option, *self.lookup_choices]
        yield {
            "form": self.form_class(
                label=self.filter_label(),
                name=self.lookup_kwarg,
                choices=choices,
                data={self.lookup_kwarg: self.value()},
            ),
        }


class DateFieldDropdownFilter(_LabeledDropdownMixin, admin.FieldListFilter):
    """Date periods as a select: Все / Сегодня / Неделя / Месяц / Год."""

    template = "unfold/filters/filters_field.html"
    form_class = DropdownForm

    def __init__(
        self,
        field: Field,
        request: HttpRequest,
        params: dict[str, Any],
        model: type[Model],
        model_admin: ModelAdmin,
        field_path: str,
    ) -> None:
        self.lookup_kwarg = f"{field_path}__period"
        super().__init__(field, request, params, model, model_admin, field_path)

    def expected_parameters(self) -> list[str]:
        return [self.lookup_kwarg]

    def value(self) -> str | None:
        raw = self.used_parameters.get(self.lookup_kwarg)
        if isinstance(raw, list) and raw:
            return raw[0]
        return raw

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet | None:
        from datetime import timedelta

        from django.utils import timezone

        value = self.value()
        if value in EMPTY_VALUES or value == _ALL:
            return queryset

        now = timezone.localtime()
        start_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today = start_today.date()

        if value == "today":
            return queryset.filter(
                **{
                    f"{self.field_path}__gte": start_today,
                    f"{self.field_path}__lt": start_today + timedelta(days=1),
                }
            )
        if value == "week":
            return queryset.filter(
                **{f"{self.field_path}__gte": now - timedelta(days=7)}
            )
        if value == "month":
            return queryset.filter(
                **{
                    f"{self.field_path}__year": today.year,
                    f"{self.field_path}__month": today.month,
                }
            )
        if value == "year":
            return queryset.filter(**{f"{self.field_path}__year": today.year})
        return queryset

    def choices(self, changelist: ChangeList) -> Iterator:
        current = self.value()
        if current in EMPTY_VALUES:
            current = _ALL
        choices = [
            (_ALL, "Все"),
            ("today", "Сегодня"),
            ("week", "7 дней"),
            ("month", "Этот месяц"),
            ("year", "Этот год"),
        ]
        yield {
            "form": self.form_class(
                label=self.filter_label(),
                name=self.lookup_kwarg,
                choices=choices,
                data={self.lookup_kwarg: current},
            ),
        }


def resolve_dropdown_filter(model: type[Model], field_name: str):
    """Pick dropdown filter class by model field type."""
    try:
        field = model._meta.get_field(field_name)
    except Exception:
        return AllValuesDropdownFilter

    from django.db import models

    if isinstance(field, models.BooleanField):
        return BooleanDropdownFilter
    if getattr(field, "choices", None):
        return ChoicesDropdownFilter
    if isinstance(field, (models.ForeignKey, models.OneToOneField)):
        return RelatedDropdownFilter
    if isinstance(field, (models.DateField, models.DateTimeField)):
        return DateFieldDropdownFilter
    return AllValuesDropdownFilter
