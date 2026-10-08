"""Technical SEO helpers: absolute URLs, Open Graph image, JSON-LD graphs."""

from __future__ import annotations

import json
import re
from html import unescape
from typing import Any
from urllib.parse import urlparse

from django.conf import settings
from django.http import HttpRequest
from django.templatetags.static import static
from django.utils.html import strip_tags

from src.core.models import SeoMeta, SiteSettings

_WS_RE = re.compile(r"\s+")


def absolute_uri(request: HttpRequest, url: str) -> str:
    value = (url or "").strip()
    if not value:
        return ""
    if urlparse(value).scheme in {"http", "https"}:
        return value
    return request.build_absolute_uri(value)


def site_base_url(request: HttpRequest) -> str:
    configured = (getattr(settings, "SITE_URL", "") or "").rstrip("/")
    if configured:
        return configured
    return request.build_absolute_uri("/").rstrip("/")


def resolve_og_image_url(
    request: HttpRequest,
    *,
    seo: SeoMeta | None,
    site_settings: SiteSettings,
) -> str:
    if seo is not None:
        image = getattr(seo, "og_image", None)
        if image:
            try:
                return absolute_uri(request, image.url)
            except ValueError:
                pass
    logo = getattr(site_settings, "logo", None)
    if logo:
        try:
            return absolute_uri(request, logo.url)
        except ValueError:
            pass
    return absolute_uri(request, static("apple-touch-icon.png"))


def plain_text(value: str, *, limit: int = 5000) -> str:
    text = _WS_RE.sub(" ", unescape(strip_tags(value or ""))).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def organization_schema(
    request: HttpRequest, site_settings: SiteSettings
) -> dict[str, Any]:
    base = site_base_url(request)
    data: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": (
            site_settings.company_legal_name
            or site_settings.brand_name
            or "Maison Polina"
        ),
        "url": base + "/",
    }
    logo_url = resolve_og_image_url(request, seo=None, site_settings=site_settings)
    if logo_url:
        data["logo"] = logo_url
    phone = (site_settings.phone or "").strip()
    if phone:
        data["telephone"] = phone
    email = (site_settings.email or "").strip()
    if email:
        data["email"] = email
    location = (site_settings.get_location() or "").strip()
    if location:
        data["address"] = {
            "@type": "PostalAddress",
            "streetAddress": location,
            "addressCountry": "UA",
        }
    same_as = [
        url
        for url in (
            site_settings.telegram_url,
            site_settings.instagram_url,
            site_settings.get_whatsapp_url(),
        )
        if url and url.rstrip("/") not in {"https://t.me", "https://instagram.com"}
    ]
    if same_as:
        data["sameAs"] = same_as
    return data


def website_schema(request: HttpRequest, site_settings: SiteSettings) -> dict[str, Any]:
    base = site_base_url(request)
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": site_settings.brand_name or "Maison Polina",
        "url": base + "/",
        "inLanguage": ["ru", "en"],
        "publisher": {
            "@type": "Organization",
            "name": (
                site_settings.company_legal_name
                or site_settings.brand_name
                or "Maison Polina"
            ),
        },
    }


def faq_page_schema(faq_items) -> dict[str, Any] | None:
    entities = []
    for item in faq_items:
        question = plain_text(getattr(item, "question", ""), limit=300)
        answer = plain_text(getattr(item, "answer", ""), limit=5000)
        if not question or not answer:
            continue
        entities.append(
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": answer,
                },
            }
        )
    if not entities:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities,
    }


def dumps_jsonld(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))
