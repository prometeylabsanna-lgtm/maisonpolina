from django.core.cache import cache

from src.core.models import SiteBlock, SiteSettings

SITE_BLOCKS_CACHE_KEY = "site_blocks_v1"
SITE_BLOCKS_CACHE_TTL = 60


def get_site_blocks() -> dict:
    blocks = cache.get(SITE_BLOCKS_CACHE_KEY)
    if blocks is None:
        blocks = {
            b.cache_key: b
            for b in SiteBlock.objects.all()
        }
        cache.set(SITE_BLOCKS_CACHE_KEY, blocks, SITE_BLOCKS_CACHE_TTL)
    return blocks


def invalidate_site_blocks_cache() -> None:
    cache.delete(SITE_BLOCKS_CACHE_KEY)


def get_block(page: str, key: str, blocks: dict | None = None) -> SiteBlock | None:
    store = blocks if blocks is not None else get_site_blocks()
    return store.get(f"{page}.{key}")


def get_block_text(
    page: str,
    key: str,
    *,
    blocks: dict | None = None,
    fallback: str = "",
) -> str:
    block = get_block(page, key, blocks)
    if not block:
        return fallback
    return block.get_text_value() or fallback


def is_section_visible(
    page: str,
    visibility_key: str,
    *,
    blocks: dict | None = None,
) -> bool:
    block = get_block(page, visibility_key, blocks)
    if not block:
        return True
    if hasattr(block, "visibility_on"):
        return block.visibility_on()
    return str(getattr(block, "text_ru", "") or "").strip() in {"1", "true", "True"}


def get_site_settings() -> SiteSettings:
    return SiteSettings.get_solo()
