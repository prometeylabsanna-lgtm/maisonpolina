import time

from django.http import HttpResponse
from django.utils.translation import get_language
from django.views.generic import TemplateView

from src.core.models import SeoMeta
from src.core.services import get_block_text, get_site_blocks, is_section_visible
from src.faq.models import FaqItem
from src.formats.models import ServiceFormat
from src.gallery.models import GalleryPhoto
from src.leads.forms import LeadForm
from src.leads.models import LeadSource
from src.reviews.models import Testimonial


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        blocks = get_site_blocks()
        ctx["page_title"] = "Полина"
        seo = SeoMeta.objects.filter(page="home").first()
        ctx["seo"] = seo
        if seo:
            ctx["seo_title"] = seo.get_text("title")
            ctx["seo_description"] = seo.get_text("description")
        ctx["blocks"] = blocks
        ctx["section_visible"] = {
            "hero": is_section_visible("home", "hero_section_visible", blocks=blocks),
            "about": is_section_visible("home", "about_section_visible", blocks=blocks),
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
        ctx["gallery_photos"] = GalleryPhoto.objects.filter(is_active=True)
        ctx["formats"] = ServiceFormat.objects.filter(is_active=True).prefetch_related(
            "features"
        )
        ctx["testimonials"] = Testimonial.objects.filter(is_active=True)
        ctx["faq_items"] = FaqItem.objects.filter(is_active=True)
        form = LeadForm(
            initial={
                "source": LeadSource.CONTACTS,
                "language": get_language() or "ru",
                "form_ts": str(time.time()),
            }
        )
        ctx["contacts_form"] = form
        ctx["lead_form"] = LeadForm(
            initial={
                "source": LeadSource.HERO,
                "language": get_language() or "ru",
                "form_ts": str(time.time()),
            }
        )
        return ctx


class PrivacyView(TemplateView):
    template_name = "pages/privacy.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        blocks = get_site_blocks()
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
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Sitemap: /sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
