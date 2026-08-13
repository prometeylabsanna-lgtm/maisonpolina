from django import forms
from django.forms import modelformset_factory
from unfold.widgets import UnfoldAdminFileFieldWidget, UnfoldBooleanWidget

from src.core.admin_guidelines import image_help, text_help
from src.core.admin_site_content_widgets import CmsAdminTextInputWidget
from src.core.fields import ADMIN_IMAGE_ACCEPT, AdminWebPImageField
from src.gallery.models import GalleryPhoto


class GalleryPhotoForm(forms.ModelForm):
    image = AdminWebPImageField(
        label="Фото",
        required=False,
        widget=UnfoldAdminFileFieldWidget(attrs={"accept": ADMIN_IMAGE_ACCEPT}),
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
            "image": "Фото",
            "alt_ru": "Описание фото",
            "alt_en": "Описание фото",
            "caption_ru": "Подпись",
            "caption_en": "Подпись",
            "col_span": "Ширина",
            "row_span": "Высота",
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
