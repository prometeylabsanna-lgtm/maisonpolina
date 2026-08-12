from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from src.core.models import SectionStyle, SeoMeta, SiteBlock, SiteSettings, PersonalityItem
from src.core.section_styles import invalidate_section_styles_cache
from src.core.services import invalidate_site_blocks_cache
from src.faq.models import FaqItem
from src.formats.models import FormatFeature, ServiceFormat
from src.gallery.models import GalleryPhoto
from src.reviews.models import Testimonial


@receiver([post_save, post_delete], sender=SiteBlock)
@receiver([post_save, post_delete], sender=SiteSettings)
@receiver([post_save, post_delete], sender=SeoMeta)
@receiver([post_save, post_delete], sender=GalleryPhoto)
@receiver([post_save, post_delete], sender=PersonalityItem)
@receiver([post_save, post_delete], sender=ServiceFormat)
@receiver([post_save, post_delete], sender=FormatFeature)
@receiver([post_save, post_delete], sender=Testimonial)
@receiver([post_save, post_delete], sender=FaqItem)
def clear_content_cache(**_kwargs) -> None:
    invalidate_site_blocks_cache()


@receiver([post_save, post_delete], sender=SectionStyle)
def clear_section_styles_cache(**_kwargs) -> None:
    invalidate_section_styles_cache()
