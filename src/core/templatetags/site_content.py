from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

from src.core.block_defaults import BLOCK_DEFAULTS
from src.core.services import get_block, get_block_text, is_section_visible

register = template.Library()


@register.simple_tag(takes_context=True)
def block_plain(context, page, key, fallback=""):
    blocks = context.get("site_blocks") or context.get("blocks")
    text = get_block_text(page, key, blocks=blocks, fallback="")
    if not text:
        defaults = BLOCK_DEFAULTS.get((page, key), {})
        lang = (get_language() or "ru")[:2]
        text = (
            defaults.get(f"text_{lang}", "")
            or defaults.get("text_ru", "")
            or fallback
        )
    return text


@register.simple_tag(takes_context=True)
def section_visible(context, page, key):
    blocks = context.get("site_blocks") or context.get("blocks")
    return is_section_visible(page, key, blocks=blocks)


@register.simple_tag(takes_context=True)
def block_image(context, page, key):
    blocks = context.get("site_blocks") or context.get("blocks")
    block = get_block(page, key, blocks)
    if block and block.image:
        return block.image
    return None


@register.filter
def nl2p(value):
    if not value:
        return ""
    paragraphs = [p.strip() for p in str(value).split("\n\n") if p.strip()]
    html = "".join(f"<p>{escape(p).replace(chr(10), '<br>')}</p>" for p in paragraphs)
    return mark_safe(html)


@register.filter
def emphasize_phrases(value, phrases: str):
    """Wrap first match of each phrase in <span class="personality__em">."""
    if not value:
        return ""
    text = escape(str(value))
    for raw in phrases.split("|"):
        phrase = raw.strip()
        if not phrase:
            continue
        needle = escape(phrase)
        if needle in text:
            text = text.replace(
                needle,
                f'<span class="personality__em">{needle}</span>',
                1,
            )
    return mark_safe(text)
