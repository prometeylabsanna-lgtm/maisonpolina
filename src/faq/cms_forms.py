"""CMS formset for FAQ items on the Вопросы section page."""

from django import forms
from django.forms import modelformset_factory
from unfold.widgets import UnfoldBooleanWidget

from src.core.admin_guidelines import text_help
from src.core.admin_site_content_widgets import (
    CmsAdminTextInputWidget,
    CmsAdminTextareaWidget,
)
from src.faq.models import FaqItem


class FaqItemCmsForm(forms.ModelForm):
    class Meta:
        model = FaqItem
        fields = (
            "question_ru",
            "question_en",
            "answer_ru",
            "answer_en",
            "order",
            "is_active",
        )
        labels = {
            "question_ru": "Вопрос",
            "question_en": "Вопрос",
            "answer_ru": "Ответ",
            "answer_en": "Ответ",
            "order": "Порядок",
            "is_active": "Активно",
        }
        help_texts = {
            "question_ru": text_help("faq.question"),
            "question_en": text_help("faq.question"),
            "answer_ru": text_help("faq.answer"),
            "answer_en": text_help("faq.answer"),
        }
        widgets = {
            "question_ru": CmsAdminTextInputWidget(),
            "question_en": CmsAdminTextInputWidget(),
            "answer_ru": CmsAdminTextareaWidget(attrs={"rows": 4}),
            "answer_en": CmsAdminTextareaWidget(attrs={"rows": 4}),
            "order": forms.NumberInput(attrs={"class": "cms-admin-input"}),
            "is_active": UnfoldBooleanWidget(),
        }


FaqItemCmsFormSet = modelformset_factory(
    FaqItem,
    form=FaqItemCmsForm,
    extra=0,
    can_delete=True,
)


def save_faq_formset(formset) -> None:
    instances = formset.save(commit=False)
    for obj in formset.deleted_objects:
        obj.delete()
    for idx, obj in enumerate(instances):
        blank = not any(
            [
                (obj.question_ru or "").strip(),
                (obj.question_en or "").strip(),
                (obj.answer_ru or "").strip(),
                (obj.answer_en or "").strip(),
            ]
        )
        if not obj.pk and blank:
            continue
        if obj.order == 0:
            obj.order = idx
        obj.save()
    formset.save_m2m()
