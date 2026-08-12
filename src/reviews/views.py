from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.translation import get_language
from django.views.decorators.http import require_http_methods
import time

from src.core.rate_limit import client_ip, is_rate_limited
from src.reviews.forms import ReviewForm
from src.reviews.models import Testimonial

RATE_LIMIT = 3
RATE_WINDOW = 3600


@require_http_methods(["GET"])
def review_form(request: HttpRequest) -> HttpResponse:
    form = ReviewForm(
        initial={
            "language": get_language() or "ru",
            "rating": 5,
            "form_ts": str(time.time()),
        }
    )
    return render(request, "partials/review-form.html", {"form": form})


@require_http_methods(["POST"])
def review_submit(request: HttpRequest) -> HttpResponse:
    form = ReviewForm(request.POST)
    template_form = "partials/review-form.html"
    template_success = "partials/review-success.html"

    if form.is_valid():
        if form.cleaned_data.get("website"):
            return render(request, template_success)

        ip = client_ip(request)
        if is_rate_limited(f"review_rate:{ip}", limit=RATE_LIMIT, window=RATE_WINDOW):
            form.add_error(None, "Слишком много отзывов. Попробуйте позже.")
            return render(request, template_form, {"form": form}, status=429)

        text = form.cleaned_data["text"]
        name = form.cleaned_data["name"]
        # Одна мова відвідувача — дублюємо, щоб показувати в RU/EN після схвалення
        Testimonial.objects.create(
            author_name_ru=name,
            author_name_en=name,
            text_ru=text,
            text_en=text,
            rating=form.cleaned_data["rating"],
            is_active=False,
            is_public_submission=True,
            order=0,
        )
        return render(request, template_success)

    return render(request, template_form, {"form": form}, status=422)
