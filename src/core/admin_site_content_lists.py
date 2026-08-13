"""Bind/save collection formsets on CMS section pages."""

from __future__ import annotations

from django.http import HttpRequest

from src.core.models import PersonalityItem
from src.core.personality_forms import (
    PersonalityExtraFormSet,
    PersonalityFactFormSet,
    personality_item_queryset,
    save_personality_formset,
)
from src.core.site_content_types import ContentSection
from src.faq.cms_forms import FaqItemCmsFormSet, save_faq_formset
from src.faq.models import FaqItem
from src.formats.cms_forms import ServiceFormatCmsFormSet, save_formats_formset
from src.formats.models import ServiceFormat
from src.gallery.forms import GalleryPhotoFormSet
from src.gallery.models import GalleryPhoto
from src.reviews.cms_forms import TestimonialCmsFormSet, save_testimonials_formset
from src.reviews.models import Testimonial


def _bind(formset_cls, queryset, prefix: str, request: HttpRequest, *, post: bool):
    if post:
        return formset_cls(
            request.POST, request.FILES, queryset=queryset, prefix=prefix
        )
    return formset_cls(queryset=queryset, prefix=prefix)


def bind_section_formsets(request: HttpRequest, section: ContentSection, *, post: bool):
    data = {
        "gallery": None,
        "personality_facts": None,
        "personality_extras": None,
        "formats": None,
        "testimonials": None,
        "faq": None,
    }
    if section.has_gallery:
        data["gallery"] = _bind(
            GalleryPhotoFormSet,
            GalleryPhoto.objects.all().order_by("order", "pk"),
            "gallery",
            request,
            post=post,
        )
    if section.has_personality_items:
        data["personality_facts"] = _bind(
            PersonalityFactFormSet,
            personality_item_queryset(PersonalityItem.Group.FACTS),
            "personality_facts",
            request,
            post=post,
        )
        data["personality_extras"] = _bind(
            PersonalityExtraFormSet,
            personality_item_queryset(PersonalityItem.Group.EXTRAS),
            "personality_extras",
            request,
            post=post,
        )
    if section.has_formats:
        data["formats"] = _bind(
            ServiceFormatCmsFormSet,
            ServiceFormat.objects.all().order_by("order", "pk"),
            "formats",
            request,
            post=post,
        )
    if section.has_testimonials:
        data["testimonials"] = _bind(
            TestimonialCmsFormSet,
            Testimonial.objects.all().order_by("order", "pk"),
            "testimonials",
            request,
            post=post,
        )
    if section.has_faq:
        data["faq"] = _bind(
            FaqItemCmsFormSet,
            FaqItem.objects.all().order_by("order", "pk"),
            "faq",
            request,
            post=post,
        )
    return data


def formsets_valid(formsets: dict) -> bool:
    return all(fs.is_valid() for fs in formsets.values() if fs is not None)


def save_section_formsets(formsets: dict) -> None:
    if formsets["gallery"] is not None:
        _save_gallery(formsets["gallery"])
    if formsets["personality_facts"] is not None:
        save_personality_formset(
            formsets["personality_facts"], PersonalityItem.Group.FACTS
        )
    if formsets["personality_extras"] is not None:
        save_personality_formset(
            formsets["personality_extras"], PersonalityItem.Group.EXTRAS
        )
    if formsets["formats"] is not None:
        save_formats_formset(formsets["formats"])
    if formsets["testimonials"] is not None:
        save_testimonials_formset(formsets["testimonials"])
    if formsets["faq"] is not None:
        save_faq_formset(formsets["faq"])


def _save_gallery(gallery_formset) -> None:
    instances = gallery_formset.save(commit=False)
    for obj in gallery_formset.deleted_objects:
        obj.delete()
    for idx, obj in enumerate(instances):
        if not obj.image and not obj.pk and not getattr(obj, "static_image", ""):
            continue
        if obj.order == 0:
            obj.order = idx
        obj.save()
    gallery_formset.save_m2m()
