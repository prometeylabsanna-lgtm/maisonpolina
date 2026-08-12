"""Changelist mixin: dropdown filters above the list, Russian defaults."""

from __future__ import annotations

from django.http import HttpRequest, HttpResponseRedirect

from src.core.admin_filters import resolve_dropdown_filter


class TopDropdownFilterMixin:
    """Place filters above results as selects; default Активно=Да when present."""

    list_filter_submit = True
    list_filter_sheet = True
    # None → auto: is_active__exact=1 if is_active is in list_filter
    list_filter_defaults: dict[str, str] | None = None

    def get_list_filter(self, request: HttpRequest):
        raw = super().get_list_filter(request)
        wrapped: list = []
        for item in raw:
            if isinstance(item, (tuple, list)):
                wrapped.append(item)
                continue
            if isinstance(item, str):
                wrapped.append(
                    (item, resolve_dropdown_filter(self.model, item))
                )
                continue
            wrapped.append(item)
        return wrapped

    def get_list_filter_defaults(self) -> dict[str, str]:
        if self.list_filter_defaults is not None:
            return dict(self.list_filter_defaults)
        defaults: dict[str, str] = {}
        for item in self.list_filter or ():
            name = item[0] if isinstance(item, (tuple, list)) else item
            if name == "is_active":
                defaults["is_active__exact"] = "1"
        return defaults

    def changelist_view(self, request: HttpRequest, extra_context=None):
        defaults = self.get_list_filter_defaults()
        if defaults and request.method == "GET":
            query = request.GET
            missing = {
                key: value
                for key, value in defaults.items()
                if key not in query
            }
            if missing:
                params = query.copy()
                for key, value in missing.items():
                    params[key] = value
                return HttpResponseRedirect(
                    f"{request.path}?{params.urlencode()}"
                )
        return super().changelist_view(request, extra_context=extra_context)
