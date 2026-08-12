import logging
import time

from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import get_language
from django.views.generic import TemplateView

from src.core.models import PersonalityItem, SeoMeta
from src.core.services import get_block_text, get_site_blocks, is_section_visible
from src.faq.models import FaqItem
from src.formats.models import ServiceFormat
from src.gallery.models import GalleryPhoto
from src.leads.forms import LeadForm
from src.leads.models import LeadSource
from src.reviews.forms import ReviewForm
from src.reviews.models import Testimonial

logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        try:
            from src.core.vercel_bootstrap import bootstrap_vercel_db

            bootstrap_vercel_db()
            blocks = get_site_blocks()
            seo = SeoMeta.objects.filter(page="home").first()
            gallery_photos = GalleryPhoto.objects.filter(is_active=True)
            personality_facts = PersonalityItem.objects.filter(
                group=PersonalityItem.Group.FACTS, is_active=True
            )
            personality_extras = PersonalityItem.objects.filter(
                group=PersonalityItem.Group.EXTRAS, is_active=True
            )
            formats = ServiceFormat.objects.filter(is_active=True).prefetch_related(
                "features"
            )
            testimonials = Testimonial.objects.filter(is_active=True)
            faq_items = FaqItem.objects.filter(is_active=True)
        except Exception:
            logger.exception("HomeView context bootstrap failed")
            if not settings.DEBUG:
                raise
            blocks = {}
            seo = None
            gallery_photos = GalleryPhoto.objects.none()
            personality_facts = PersonalityItem.objects.none()
            personality_extras = PersonalityItem.objects.none()
            formats = ServiceFormat.objects.none()
            testimonials = Testimonial.objects.none()
            faq_items = FaqItem.objects.none()

        ctx["page_title"] = "MAISON POLINA"
        ctx["seo"] = seo
        if seo:
            ctx["seo_title"] = seo.get_text("title")
            ctx["seo_description"] = seo.get_text("description")
        ctx["blocks"] = blocks
        ctx["section_visible"] = {
            "hero": is_section_visible("home", "hero_section_visible", blocks=blocks),
            "about": is_section_visible("home", "about_section_visible", blocks=blocks),
            "personality": is_section_visible(
                "home", "personality_section_visible", blocks=blocks
            ),
            "gallery": is_section_visible("home", "gallery_section_visible", blocks=blocks),
            "formats": is_section_visible("home", "formats_section_visible", blocks=blocks),
            "testimonials": is_section_visible(
                "home", "testimonials_section_visible", blocks=blocks
            ),
            "faq": is_section_visible("home", "faq_section_visible", blocks=blocks),
            "contacts": is_section_visible(
                "home", "contacts_section_visible", blocks=blocks
            ),
        }
        ctx["gallery_photos"] = gallery_photos
        ctx["personality_facts"] = personality_facts
        ctx["personality_extras"] = personality_extras
        ctx["formats"] = formats
        ctx["testimonials"] = testimonials
        ctx["faq_items"] = faq_items
        utm = {
            "utm_source": (self.request.GET.get("utm_source") or "")[:128],
            "utm_medium": (self.request.GET.get("utm_medium") or "")[:128],
            "utm_campaign": (self.request.GET.get("utm_campaign") or "")[:128],
        }
        lang = get_language() or "ru"
        ts = str(time.time())
        form = LeadForm(
            initial={
                "source": LeadSource.CONTACTS,
                "language": lang,
                "form_ts": ts,
                **utm,
            }
        )
        ctx["contacts_form"] = form
        ctx["lead_form"] = LeadForm(
            initial={
                "source": LeadSource.HERO,
                "language": lang,
                "form_ts": ts,
                **utm,
            }
        )
        ctx["review_form"] = ReviewForm(
            initial={
                "language": lang,
                "rating": 5,
                "form_ts": ts,
            }
        )
        return ctx


class PrivacyView(TemplateView):
    template_name = "pages/privacy.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        blocks = get_site_blocks()
        lang = get_language() or "ru"
        ts = str(time.time())
        ctx["lead_form"] = LeadForm(
            initial={
                "source": LeadSource.CONTACTS,
                "language": lang,
                "form_ts": ts,
            }
        )
        ctx["review_form"] = ReviewForm(
            initial={
                "language": lang,
                "rating": 5,
                "form_ts": ts,
            }
        )
        ctx["page_title"] = get_block_text(
            "privacy", "title", blocks=blocks, fallback="Политика конфиденциальности"
        )
        seo = SeoMeta.objects.filter(page="privacy").first()
        ctx["seo"] = seo
        if seo:
            ctx["seo_title"] = seo.get_text("title")
            ctx["seo_description"] = seo.get_text("description")
        ctx["privacy_title"] = get_block_text("privacy", "title", blocks=blocks)
        ctx["privacy_body"] = get_block_text("privacy", "body", blocks=blocks)
        return ctx


def robots_txt(_request):
    from django.conf import settings

    sitemap = f"{settings.SITE_URL.rstrip('/')}/sitemap.xml"
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",  # decoy; do not publish ADMIN_URL
        f"Sitemap: {sitemap}",
    ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")
