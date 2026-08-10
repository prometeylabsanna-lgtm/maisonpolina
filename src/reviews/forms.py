import time

from django import forms
from django.utils.translation import gettext_lazy as _


class ReviewForm(forms.Form):
    name = forms.CharField(
        max_length=128,
        label=_("Имя"),
        widget=forms.TextInput(attrs={"autocomplete": "name"}),
    )
    text = forms.CharField(
        min_length=10,
        max_length=1200,
        label=_("Отзыв"),
        widget=forms.Textarea(attrs={"rows": 4}),
        error_messages={
            "min_length": _("Напишите чуть подробнее — минимум 10 символов"),
        },
    )
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        label=_("Оценка"),
        error_messages={
            "min_value": _("Выберите оценку от 1 до 5"),
            "max_value": _("Выберите оценку от 1 до 5"),
            "required": _("Выберите оценку"),
        },
    )
    language = forms.CharField(required=False, widget=forms.HiddenInput)
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "tabindex": "-1",
                "autocomplete": "off",
                "aria-hidden": "true",
            }
        ),
    )
    form_ts = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_website(self):
        return self.cleaned_data.get("website", "")

    def clean_form_ts(self):
        raw = self.cleaned_data.get("form_ts") or ""
        if not raw:
            return raw
        try:
            started = float(raw)
        except (TypeError, ValueError):
            return raw
        if time.time() - started < 2:
            raise forms.ValidationError("Too fast")
        return raw

    def clean_name(self):
        return (self.cleaned_data.get("name") or "").strip()

    def clean_text(self):
        return (self.cleaned_data.get("text") or "").strip()

    def clean_language(self):
        lang = (self.cleaned_data.get("language") or "ru")[:2].lower()
        return lang if lang in {"ru", "en"} else "ru"
