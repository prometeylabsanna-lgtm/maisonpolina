from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from src.reviews.forms import ReviewForm
from src.reviews.models import Testimonial

RATE_LIMIT = 3
RATE_WINDOW = 3600


def _client_ip(request: HttpRequest) -> str:
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def _rate_limited(ip: str) -> bool:
    if not ip:
        return False
    key = f"review_rate:{ip}"
    count = cache.get(key, 0)
    if count >= RATE_LIMIT:
        return True
    cache.set(key, count + 1, RATE_WINDOW)
    return False


@require_http_methods(["POST"])
def review_submit(request: HttpRequest) -> HttpResponse:
    form = ReviewForm(request.POST)
    template_form = "partials/review-form.html"
    template_success = "partials/review-success.html"

    if form.is_valid():
        if form.cleaned_data.get("website"):
            return render(request, template_success)

        ip = _client_ip(request)
        if _rate_limited(ip):
            form.add_error(None, "Слишком много отзывов. Попробуйте позже.")
            return render(request, template_form, {"form": form}, status=429)

        text = form.cleaned_data["text"]
        # Одна мова відвідувача — дублюємо, щоб показувати в RU/EN після схвалення
        Testimonial.objects.create(
            author_name=form.cleaned_data["name"],
            text_ru=text,
            text_en=text,
            rating=form.cleaned_data["rating"],
            is_active=False,
            is_public_submission=True,
            order=0,
        )
        return render(request, template_success)

    return render(request, template_form, {"form": form}, status=422)
