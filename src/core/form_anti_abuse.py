import time

from django import forms


class AntiAbuseFormMixin(forms.Form):
    """Honeypot + minimum submit delay for public forms."""

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
        # Honeypot: keep value so the view can short-circuit without saving.
        return self.cleaned_data.get("website", "")

    def clean_form_ts(self):
        raw = (self.cleaned_data.get("form_ts") or "").strip()
        if not raw:
            raise forms.ValidationError("Invalid form")
        try:
            started = float(raw)
        except (TypeError, ValueError) as exc:
            raise forms.ValidationError("Invalid form") from exc
        if time.time() - started < 2:
            raise forms.ValidationError("Too fast")
        return raw
