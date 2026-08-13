"""Raster → WebP conversion (Pillow). No Django imports."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

WEBP_QUALITY = 82
WEBP_METHOD = 6
SKIP_SUFFIXES = {".webp", ".svg", ".ico", ".mp4", ".webm", ".mov"}
CONVERT_SUFFIXES = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".tif",
    ".tiff",
    ".heic",
    ".heif",
}

_HEIF_READY = False


def ensure_heif_support() -> bool:
    """Register iPhone HEIC/HEIF so Pillow and Django ImageField can open them."""
    global _HEIF_READY
    if _HEIF_READY:
        return True
    try:
        from pillow_heif import register_heif_opener
    except ImportError:
        return False
    register_heif_opener()
    _HEIF_READY = True
    return True


ensure_heif_support()


def webp_name(source_name: str) -> str:
    path = Path(source_name or "image")
    stem = path.stem or "image"
    return str(path.with_name(f"{stem}.webp"))


def convert_bytes_to_webp(data: bytes, source_name: str = "image") -> tuple[bytes, str] | None:
    suffix = Path(source_name or "").suffix.lower()
    if suffix in SKIP_SUFFIXES:
        return None
    if suffix and suffix not in CONVERT_SUFFIXES:
        return None
    if not data:
        return None
    try:
        with Image.open(BytesIO(data)) as raw:
            raw.load()
            image = ImageOps.exif_transpose(raw) or raw
            if getattr(image, "is_animated", False):
                image.seek(0)
                image = image.copy()
            converted = _prepare_mode(image)
            buffer = BytesIO()
            converted.save(
                buffer,
                format="WEBP",
                quality=WEBP_QUALITY,
                method=WEBP_METHOD,
            )
            return buffer.getvalue(), webp_name(source_name)
    except (UnidentifiedImageError, OSError, ValueError):
        return None


def convert_path_to_webp(path: Path, *, replace: bool = False) -> Path | None:
    path = Path(path)
    if not path.is_file():
        return None
    result = convert_bytes_to_webp(path.read_bytes(), path.name)
    if result is None:
        return None
    payload, name = result
    target = path.with_name(Path(name).name)
    target.write_bytes(payload)
    if replace and target != path:
        path.unlink(missing_ok=True)
    return target


def _prepare_mode(image: Image.Image) -> Image.Image:
    if image.mode in {"RGBA", "RGB"}:
        return image
    if image.mode in {"P", "LA", "PA"}:
        return image.convert("RGBA")
    if "A" in image.getbands():
        return image.convert("RGBA")
    return image.convert("RGB")
