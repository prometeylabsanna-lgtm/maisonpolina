import time

from django import forms
from django.utils.translation import gettext_lazy as _

from src.core.form_validators import (
    validate_message_text,
    validate_person_name,
    validate_phone,
)


class LeadForm(forms.Form):
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
    # Honeypot — must stay empty
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "tabindex": "-1",
        "autocomplete": "off",
        "aria-hidden": "true",
    }))
    form_ts = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_website(self):
        # Honeypot: keep value so the view can short-circuit without saving.
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
        return validate_person_name(self.cleaned_data.get("name") or "")

    def clean_contact(self):
        return validate_phone(self.cleaned_data.get("contact") or "")

    def clean_message(self):
        return validate_message_text(self.cleaned_data.get("message") or "")
