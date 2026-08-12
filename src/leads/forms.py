from django import forms
from django.utils.translation import gettext_lazy as _

from src.core.form_anti_abuse import AntiAbuseFormMixin
from src.core.form_validators import (
    validate_message_text,
    validate_person_name,
    validate_phone,
)


class LeadForm(AntiAbuseFormMixin):
    name = forms.CharField(
        max_length=128,
        label=_("Имя"),
        widget=forms.TextInput(attrs={"autocomplete": "name"}),
    )
    contact = forms.CharField(
        max_length=255,
        label=_("Телефон"),
        widget=forms.TextInput(
            attrs={
                "autocomplete": "tel",
                "inputmode": "tel",
            }
        ),
    )
    message = forms.CharField(
        required=False,
        label=_("Комментарий"),
        widget=forms.Textarea(attrs={"rows": 3}),
    )
    consent = forms.BooleanField(
        label=_("Согласен на обработку персональных данных"),
        error_messages={"required": _("Необходимо согласие на обработку данных")},
    )
    service = forms.CharField(required=False, widget=forms.HiddenInput)
    source = forms.CharField(required=False, widget=forms.HiddenInput)
    language = forms.CharField(required=False, widget=forms.HiddenInput)
    utm_source = forms.CharField(required=False, max_length=128, widget=forms.HiddenInput)
    utm_medium = forms.CharField(required=False, max_length=128, widget=forms.HiddenInput)
    utm_campaign = forms.CharField(required=False, max_length=128, widget=forms.HiddenInput)

    def clean_name(self):
        return validate_person_name(self.cleaned_data.get("name") or "")

    def clean_contact(self):
        return validate_phone(self.cleaned_data.get("contact") or "")

    def clean_message(self):
        return validate_message_text(self.cleaned_data.get("message") or "")

    def clean_language(self):
        lang = (self.cleaned_data.get("language") or "ru")[:2].lower()
        return lang if lang in {"ru", "en"} else "ru"
