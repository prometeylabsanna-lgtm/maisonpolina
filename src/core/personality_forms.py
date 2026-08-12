from django import forms
from django.forms import modelformset_factory
from unfold.widgets import UnfoldBooleanWidget

from src.core.admin_guidelines import text_help
from src.core.admin_site_content_widgets import CmsAdminTextInputWidget
from src.core.models import PersonalityItem


class PersonalityItemForm(forms.ModelForm):
    class Meta:
        model = PersonalityItem
        fields = (
            "label_ru",
            "label_en",
            "value_ru",
            "value_en",
            "order",
            "is_active",
        )
        labels = {
            "label_ru": "Название (RU)",
            "label_en": "Название (EN)",
            "value_ru": "Значение (RU)",
            "value_en": "Значение (EN)",
            "order": "Порядок",
            "is_active": "Активно",
        }
        help_texts = {
            "label_ru": text_help("personality.label"),
            "label_en": text_help("personality.label"),
            "value_ru": text_help("personality.value"),
            "value_en": text_help("personality.value"),
        }
        widgets = {
            "label_ru": CmsAdminTextInputWidget(),
            "label_en": CmsAdminTextInputWidget(),
            "value_ru": CmsAdminTextInputWidget(),
            "value_en": CmsAdminTextInputWidget(),
            "order": forms.NumberInput(attrs={"class": "cms-admin-input"}),
            "is_active": UnfoldBooleanWidget(),
        }


def make_personality_item_formset():
    return modelformset_factory(
        PersonalityItem,
        form=PersonalityItemForm,
        extra=0,
        can_delete=True,
    )


PersonalityFactFormSet = make_personality_item_formset()
PersonalityExtraFormSet = make_personality_item_formset()


def personality_item_queryset(group: str):
    return PersonalityItem.objects.filter(group=group).order_by("order", "pk")


def save_personality_formset(formset, group: str) -> None:
    instances = formset.save(commit=False)
    for obj in formset.deleted_objects:
        obj.delete()
    for idx, obj in enumerate(instances):
        blank = not any(
            [
                (obj.label_ru or "").strip(),
                (obj.label_en or "").strip(),
                (obj.value_ru or "").strip(),
                (obj.value_en or "").strip(),
            ]
        )
        if not obj.pk and blank:
            continue
        obj.group = group
        if obj.order == 0:
            obj.order = idx + 1
        obj.save()
    formset.save_m2m()
