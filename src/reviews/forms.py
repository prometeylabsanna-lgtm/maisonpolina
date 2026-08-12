from django import forms
from django.utils.translation import gettext_lazy as _

from src.core.form_anti_abuse import AntiAbuseFormMixin
from src.core.form_validators import (
    MSG_MESSAGE_MIN,
    validate_message_text,
    validate_person_name,
)


class ReviewForm(AntiAbuseFormMixin):
    name = forms.CharField(
        max_length=128,
        label=_("Имя"),
        widget=forms.TextInput(attrs={"autocomplete": "name"}),
    )
    text = forms.CharField(
        min_length=2,
        max_length=1200,
        label=_("Отзыв"),
        widget=forms.Textarea(attrs={"rows": 4}),
        error_messages={
            "min_length": MSG_MESSAGE_MIN,
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

    def clean_name(self):
        return validate_person_name(self.cleaned_data.get("name") or "")

    def clean_text(self):
        return validate_message_text(self.cleaned_data.get("text") or "", required=True)

    def clean_language(self):
        lang = (self.cleaned_data.get("language") or "ru")[:2].lower()
        return lang if lang in {"ru", "en"} else "ru"
