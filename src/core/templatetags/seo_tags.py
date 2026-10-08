from django import template

from src.core.seo import (
    dumps_jsonld,
    faq_page_schema,
    organization_schema,
    resolve_og_image_url,
    website_schema,
)

register = template.Library()


@register.simple_tag(takes_context=True)
def og_image_url(context) -> str:
    request = context["request"]
    return resolve_og_image_url(
        request,
        seo=context.get("seo"),
        site_settings=context["site_settings"],
    )


@register.inclusion_tag("partials/seo-jsonld.html", takes_context=True)
def render_jsonld(context) -> dict:
    request = context["request"]
    site_settings = context["site_settings"]
    blocks = [
        dumps_jsonld(organization_schema(request, site_settings)),
        dumps_jsonld(website_schema(request, site_settings)),
    ]
    faq_items = context.get("faq_items")
    if faq_items is not None:
        faq = faq_page_schema(faq_items)
        if faq is not None:
            blocks.append(dumps_jsonld(faq))
    return {"json_ld_blocks": blocks}
