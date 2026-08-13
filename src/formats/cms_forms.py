"""CMS formset for service formats on the Услуги section page."""

from django import forms
from django.forms import modelformset_factory
from unfold.widgets import UnfoldAdminFileFieldWidget, UnfoldBooleanWidget

from src.core.admin_guidelines import image_help, text_help
from src.core.admin_site_content_widgets import (
    CmsAdminTextInputWidget,
    CmsAdminTextareaWidget,
)
from src.core.fields import ADMIN_IMAGE_ACCEPT, AdminWebPImageField
from src.formats.models import FormatFeature, ServiceFormat


class ServiceFormatCmsForm(forms.ModelForm):
    image = AdminWebPImageField(
        label="Фото",
        required=False,
        widget=UnfoldAdminFileFieldWidget(attrs={"accept": ADMIN_IMAGE_ACCEPT}),
        help_text=image_help("formats.image"),
    )
    features_ru = forms.CharField(
        label="Что входит",
        required=False,
        widget=CmsAdminTextareaWidget(attrs={"rows": 4}),
        help_text="Каждый пункт с новой строки.",
    )
    features_en = forms.CharField(
        label="Что входит",
        required=False,
        widget=CmsAdminTextareaWidget(attrs={"rows": 4}),
        help_text="One item per line.",
    )

    class Meta:
        model = ServiceFormat
        fields = (
            "image",
            "title_ru",
            "title_en",
            "label_ru",
            "label_en",
            "description_ru",
            "description_en",
            "price_text_ru",
            "price_text_en",
            "is_featured",
            "order",
            "is_active",
        )
        labels = {
            "title_ru": "Название",
            "title_en": "Название",
            "label_ru": "Метка",
            "label_en": "Метка",
            "description_ru": "Описание",
            "description_en": "Описание",
            "price_text_ru": "Цена",
            "price_text_en": "Цена",
            "is_featured": "В избранном",
            "order": "Порядок",
            "is_active": "Активно",
        }
        help_texts = {
            "title_ru": text_help("formats.title"),
            "title_en": text_help("formats.title"),
            "label_ru": text_help("formats.label"),
            "label_en": text_help("formats.label"),
            "description_ru": text_help("formats.description"),
            "description_en": text_help("formats.description"),
            "price_text_ru": text_help("formats.price_text"),
            "price_text_en": text_help("formats.price_text"),
        }
        widgets = {
            "title_ru": CmsAdminTextInputWidget(),
            "title_en": CmsAdminTextInputWidget(),
            "label_ru": CmsAdminTextInputWidget(),
            "label_en": CmsAdminTextInputWidget(),
            "description_ru": CmsAdminTextareaWidget(attrs={"rows": 3}),
            "description_en": CmsAdminTextareaWidget(attrs={"rows": 3}),
            "price_text_ru": CmsAdminTextInputWidget(),
            "price_text_en": CmsAdminTextInputWidget(),
            "order": forms.NumberInput(attrs={"class": "cms-admin-input"}),
            "is_featured": UnfoldBooleanWidget(),
            "is_active": UnfoldBooleanWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            feats = list(self.instance.features.order_by("order", "pk"))
            self.fields["features_ru"].initial = "\n".join(
                (item.text_ru or "").strip() for item in feats
            )
            self.fields["features_en"].initial = "\n".join(
                (item.text_en or "").strip() for item in feats
            )


ServiceFormatCmsFormSet = modelformset_factory(
    ServiceFormat,
    form=ServiceFormatCmsForm,
    extra=0,
    can_delete=True,
)


def _lines(value: str) -> list[str]:
    return [line.strip() for line in (value or "").splitlines() if line.strip()]


def sync_format_features(service: ServiceFormat, form: ServiceFormatCmsForm) -> None:
    ru_lines = _lines(form.cleaned_data.get("features_ru", ""))
    en_lines = _lines(form.cleaned_data.get("features_en", ""))
    count = max(len(ru_lines), len(en_lines))
    existing = list(service.features.order_by("order", "pk"))
    for idx in range(count):
        ru = ru_lines[idx] if idx < len(ru_lines) else ""
        en = en_lines[idx] if idx < len(en_lines) else ""
        if idx < len(existing):
            obj = existing[idx]
            obj.text_ru = ru or en
            obj.text_en = en
            obj.order = idx
            obj.save()
        else:
            FormatFeature.objects.create(
                service=service,
                text_ru=ru or en,
                text_en=en,
                order=idx,
            )
    for obj in existing[count:]:
        obj.delete()


def save_formats_formset(formset) -> None:
    instances = formset.save(commit=False)
    for obj in formset.deleted_objects:
        obj.delete()
    for idx, obj in enumerate(instances):
        blank = not any(
            [
                (obj.title_ru or "").strip(),
                (obj.title_en or "").strip(),
                bool(obj.image),
                bool(obj.pk),
            ]
        )
        if not obj.pk and blank:
            continue
        if obj.order == 0:
            obj.order = idx
        obj.save()
    for form in formset.forms:
        if not form.cleaned_data or form.cleaned_data.get("DELETE"):
            continue
        instance = form.instance
        if not instance.pk:
            continue
        sync_format_features(instance, form)
    formset.save_m2m()
