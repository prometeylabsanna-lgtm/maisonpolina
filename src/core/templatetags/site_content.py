from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

from src.core.block_defaults import BLOCK_DEFAULTS
from src.core.services import get_block, get_block_text, is_section_visible

register = template.Library()


def _looks_like_html(text: str) -> bool:
    return "<" in text and ">" in text


def _resolve_block_text(context, page, key, fallback="") -> str:
    blocks = context.get("site_blocks") or context.get("blocks")
    text = get_block_text(page, key, blocks=blocks, fallback="")
    if text:
        return text
    defaults = BLOCK_DEFAULTS.get((page, key), {})
    lang = (get_language() or "ru")[:2]
    return (
        defaults.get(f"text_{lang}", "")
        or defaults.get("text_ru", "")
        or fallback
    )


@register.filter
def get_item(mapping, key):
    if mapping is None:
        return None
    try:
        return mapping.get(key)
    except AttributeError:
        return None


@register.filter
def richtext(value):
    """Render TinyMCE HTML as-is; plain text → escaped paragraphs."""
    if not value:
        return ""
    text = str(value)
    if _looks_like_html(text):
        return mark_safe(text)
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        return mark_safe(escape(text).replace("\n", "<br>"))
    html = "".join(
        f"<p>{escape(p).replace(chr(10), '<br>')}</p>" for p in paragraphs
    )
    return mark_safe(html)


@register.simple_tag(takes_context=True)
def block_plain(context, page, key, fallback=""):
    return _resolve_block_text(context, page, key, fallback)


@register.simple_tag(takes_context=True)
def block_html(context, page, key, fallback=""):
    return richtext(_resolve_block_text(context, page, key, fallback))


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


@register.simple_tag(takes_context=True)
def block_video_src(context, page, key):
    blocks = context.get("site_blocks") or context.get("blocks")
    block = get_block(page, key, blocks)
    if not block:
        return ""
    getter = getattr(block, "get_video_src", None)
    return getter() if callable(getter) else ""


@register.filter
def video_mime(url):
    lower = (url or "").lower().split("?", 1)[0]
    if lower.endswith(".webm"):
        return "video/webm"
    return "video/mp4"


@register.simple_tag
def gallery_image_url(photo):
    """Prefer shipped static gallery images (Vercel-safe), else media."""
    getter = getattr(photo, "get_image_url", None)
    if callable(getter):
        return getter()
    return ""


@register.filter
def nl2p(value):
    return richtext(value)


@register.filter
def emphasize_phrases(value, phrases: str):
    """Wrap first match of each phrase in <span class="personality__em">."""
    if not value:
        return ""
    raw = str(value)
    if _looks_like_html(raw):
        return mark_safe(raw)
    text = escape(raw)
    for part in phrases.split("|"):
        phrase = part.strip()
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
