"""Shared IP extraction and fixed-window rate limiting."""

from __future__ import annotations

from django.core.cache import cache
from django.http import HttpRequest


def client_ip(request: HttpRequest) -> str:
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "") or ""


def is_rate_limited(key: str, *, limit: int, window: int) -> bool:
    """Fixed-window counter. Returns True when the key has exceeded *limit*.

    Uses cache.add to start the window so TTL is not refreshed on every hit.
    Missing IP keys should be passed as empty — caller decides policy.
    """
    if not key:
        return True
    added = cache.add(key, 1, window)
    if added:
        return False
    try:
        count = cache.incr(key)
    except ValueError:
        cache.set(key, 1, window)
        return False
    return count > limit
