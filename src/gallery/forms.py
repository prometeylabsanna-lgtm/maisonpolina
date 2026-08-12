from django import forms
from django.forms import modelformset_factory
from unfold.widgets import UnfoldAdminFileFieldWidget, UnfoldBooleanWidget

from src.core.admin_guidelines import image_help, text_help
from src.core.admin_site_content_widgets import CmsAdminTextInputWidget
from src.core.fields import AdminWebPImageField
from src.gallery.models import GalleryPhoto


class GalleryPhotoForm(forms.ModelForm):
    image = AdminWebPImageField(
        label="Изображение",
        required=False,
        widget=UnfoldAdminFileFieldWidget(),
        help_text=image_help("gallery.image"),
    )

    class Meta:
        model = GalleryPhoto
        fields = (
            "image",
            "alt_ru",
            "alt_en",
            "caption_ru",
            "caption_en",
            "col_span",
            "row_span",
            "order",
            "is_active",
        )
        labels = {
            "image": "Изображение",
            "alt_ru": "Alt (RU)",
            "alt_en": "Alt (EN)",
            "caption_ru": "Подпись (RU)",
            "caption_en": "Подпись (EN)",
            "col_span": "Ширина (col)",
            "row_span": "Высота (row)",
            "order": "Порядок",
            "is_active": "Активно",
        }
        help_texts = {
            "image": image_help("gallery.image"),
            "alt_ru": text_help("gallery.alt"),
            "alt_en": text_help("gallery.alt"),
            "caption_ru": text_help("gallery.caption"),
            "caption_en": text_help("gallery.caption"),
        }
        widgets = {
            "alt_ru": CmsAdminTextInputWidget(),
            "alt_en": CmsAdminTextInputWidget(),
            "caption_ru": CmsAdminTextInputWidget(),
            "caption_en": CmsAdminTextInputWidget(),
            "col_span": forms.NumberInput(attrs={"class": "cms-admin-input"}),
            "row_span": forms.NumberInput(attrs={"class": "cms-admin-input"}),
            "order": forms.NumberInput(attrs={"class": "cms-admin-input"}),
            "is_active": UnfoldBooleanWidget(),
        }


GalleryPhotoFormSet = modelformset_factory(
    GalleryPhoto,
    form=GalleryPhotoForm,
    extra=0,
    can_delete=True,
)
