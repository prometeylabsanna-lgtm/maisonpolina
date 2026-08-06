import logging
import time

from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.translation import get_language
from django.views.decorators.http import require_http_methods

from src.leads.forms import LeadForm
from src.leads.models import Lead, LeadSource
from src.leads.services import notify

logger = logging.getLogger(__name__)

RATE_LIMIT = 5
RATE_WINDOW = 3600


def _client_ip(request: HttpRequest) -> str:
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def _rate_limited(ip: str) -> bool:
    if not ip:
        return False
    key = f"lead_rate:{ip}"
    count = cache.get(key, 0)
    if count >= RATE_LIMIT:
        return True
    cache.set(key, count + 1, RATE_WINDOW)
    return False


@require_http_methods(["GET"])
def lead_form(request: HttpRequest) -> HttpResponse:
    form = LeadForm(
        initial={
            "service": request.GET.get("service", ""),
            "source": request.GET.get("source", LeadSource.CONTACTS),
            "language": get_language() or "ru",
            "form_ts": str(time.time()),
        }
    )
    return render(
        request,
        "partials/lead-form.html",
        {
            "form": form,
            "service_label": request.GET.get("service", ""),
        },
    )


@require_http_methods(["POST"])
def lead_submit(request: HttpRequest) -> HttpResponse:
    form = LeadForm(request.POST)
    template_form = "partials/lead-form.html"
    template_success = "partials/lead-success.html"

    if form.is_valid():
        # Honeypot filled — pretend success, do not save.
        if form.cleaned_data.get("website"):
            return render(request, template_success)

        ip = _client_ip(request)
        if _rate_limited(ip):
            form.add_error(None, "Слишком много обращений. Попробуйте позже.")
            return render(
                request,
                template_form,
                {"form": form, "service_label": form.cleaned_data.get("service", "")},
                status=429,
            )

        source = form.cleaned_data.get("source") or LeadSource.CONTACTS
        if source not in LeadSource.values:
            source = LeadSource.CONTACTS

        lead = Lead.objects.create(
            name=form.cleaned_data["name"],
            contact=form.cleaned_data["contact"],
            message=form.cleaned_data.get("message", ""),
            service=form.cleaned_data.get("service", ""),
            source=source,
            language=form.cleaned_data.get("language") or (get_language() or "ru"),
            ip=ip or None,
            user_agent=(request.META.get("HTTP_USER_AGENT", "") or "")[:512],
            utm_source=request.GET.get("utm_source", "")[:128],
            utm_medium=request.GET.get("utm_medium", "")[:128],
            utm_campaign=request.GET.get("utm_campaign", "")[:128],
        )
        try:
            notify(lead)
        except Exception:
            logger.exception("Unexpected notify failure for lead %s", lead.pk)

        return render(request, template_success)

    return render(
        request,
        template_form,
        {
            "form": form,
            "service_label": request.POST.get("service", ""),
        },
        status=422,
    )
