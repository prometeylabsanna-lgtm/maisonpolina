"""CMS formset for testimonials on the Отзывы section page."""

from django import forms
from django.forms import modelformset_factory
from unfold.widgets import UnfoldAdminFileFieldWidget, UnfoldBooleanWidget

from src.core.admin_guidelines import image_help, text_help
from src.core.admin_site_content_widgets import (
    CmsAdminTextInputWidget,
    CmsAdminTextareaWidget,
)
from src.core.fields import ADMIN_IMAGE_ACCEPT, AdminWebPImageField
from src.reviews.models import Testimonial


class TestimonialCmsForm(forms.ModelForm):
    photo = AdminWebPImageField(
        label="Фото",
        required=False,
        widget=UnfoldAdminFileFieldWidget(attrs={"accept": ADMIN_IMAGE_ACCEPT}),
        help_text=image_help("reviews.photo"),
    )

    class Meta:
        model = Testimonial
        fields = (
            "photo",
            "author_name_ru",
            "author_name_en",
            "role_ru",
            "role_en",
            "text_ru",
            "text_en",
            "rating",
            "order",
            "is_active",
        )
        labels = {
            "author_name_ru": "Имя автора",
            "author_name_en": "Имя автора",
            "role_ru": "Роль / подпись",
            "role_en": "Роль / подпись",
            "text_ru": "Текст отзыва",
            "text_en": "Текст отзыва",
            "rating": "Рейтинг",
            "order": "Порядок",
            "is_active": "Активно",
        }
        help_texts = {
            "author_name_ru": text_help("reviews.author_name"),
            "author_name_en": text_help("reviews.author_name"),
            "role_ru": text_help("reviews.role"),
            "role_en": text_help("reviews.role"),
            "text_ru": text_help("reviews.text"),
            "text_en": text_help("reviews.text"),
        }
        widgets = {
            "author_name_ru": CmsAdminTextInputWidget(),
            "author_name_en": CmsAdminTextInputWidget(),
            "role_ru": CmsAdminTextInputWidget(),
            "role_en": CmsAdminTextInputWidget(),
            "text_ru": CmsAdminTextareaWidget(attrs={"rows": 4}),
            "text_en": CmsAdminTextareaWidget(attrs={"rows": 4}),
            "rating": forms.NumberInput(attrs={"class": "cms-admin-input", "min": 1, "max": 5}),
            "order": forms.NumberInput(attrs={"class": "cms-admin-input"}),
            "is_active": UnfoldBooleanWidget(),
        }


TestimonialCmsFormSet = modelformset_factory(
    Testimonial,
    form=TestimonialCmsForm,
    extra=0,
    can_delete=True,
)


def save_testimonials_formset(formset) -> None:
    instances = formset.save(commit=False)
    for obj in formset.deleted_objects:
        obj.delete()
    for idx, obj in enumerate(instances):
        blank = not any(
            [
                (obj.author_name_ru or "").strip(),
                (obj.author_name_en or "").strip(),
                (obj.text_ru or "").strip(),
                (obj.text_en or "").strip(),
                bool(obj.photo),
                bool(obj.pk),
            ]
        )
        if not obj.pk and blank:
            continue
        if obj.order == 0:
            obj.order = idx
        obj.save()
    formset.save_m2m()
