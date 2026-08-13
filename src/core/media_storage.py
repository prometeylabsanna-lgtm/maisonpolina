"""Database-backed media storage + HTTP serving (Vercel-safe)."""

from __future__ import annotations

import mimetypes
from io import BytesIO
from pathlib import Path
from urllib.parse import quote

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import Storage, default_storage
from django.http import FileResponse, Http404, HttpRequest, HttpResponse
from django.utils.deconstruct import deconstructible


def _safe_media_path(path: str) -> str:
    cleaned = (path or "").replace("\\", "/").lstrip("/")
    if not cleaned or cleaned.startswith("/") or ".." in cleaned.split("/"):
        raise Http404()
    return cleaned


def _content_type_for(name: str, fallback: str = "") -> str:
    guessed, _encoding = mimetypes.guess_type(name)
    return guessed or fallback or "application/octet-stream"


@deconstructible
class DatabaseFileStorage(Storage):
    """Store uploads in Postgres so Vercel /tmp does not drop them."""

    def _open(self, name, mode="rb"):
        from src.core.models import StoredMedia

        row = StoredMedia.objects.filter(name=name).first()
        if row is None:
            raise FileNotFoundError(name)
        return ContentFile(bytes(row.content), name=name)

    def _save(self, name, content):
        from src.core.models import StoredMedia

        if hasattr(content, "seek"):
            try:
                content.seek(0)
            except OSError:
                pass
        data = content.read()
        if isinstance(data, memoryview):
            data = data.tobytes()
        elif isinstance(data, bytearray):
            data = bytes(data)
        ctype = _content_type_for(name, getattr(content, "content_type", "") or "")
        StoredMedia.objects.update_or_create(
            name=name,
            defaults={
                "content": data,
                "content_type": ctype,
                "size": len(data),
            },
        )
        return name

    def exists(self, name):
        from src.core.models import StoredMedia

        return StoredMedia.objects.filter(name=name).exists()

    def delete(self, name):
        from src.core.models import StoredMedia

        StoredMedia.objects.filter(name=name).delete()

    def size(self, name):
        from src.core.models import StoredMedia

        row = StoredMedia.objects.filter(name=name).only("size").first()
        if row is None:
            raise FileNotFoundError(name)
        return row.size

    def url(self, name):
        base = settings.MEDIA_URL or "/media/"
        if not base.endswith("/"):
            base = f"{base}/"
        return f"{base}{quote(name)}"

    def listdir(self, path):
        from src.core.models import StoredMedia

        prefix = (path or "").replace("\\", "/").strip("/")
        if prefix:
            prefix = f"{prefix}/"
        directories: set[str] = set()
        files: list[str] = []
        for name in StoredMedia.objects.filter(name__startswith=prefix).values_list(
            "name", flat=True
        ):
            rest = name[len(prefix) :]
            if "/" in rest:
                directories.add(rest.split("/", 1)[0])
            elif rest:
                files.append(rest)
        return list(directories), files


def serve_media(request: HttpRequest, path: str) -> HttpResponse:
    """Serve /media/* from default storage, then StoredMedia (Vercel)."""
    name = _safe_media_path(path)
    payload, content_type = _read_media(name)
    response = FileResponse(
        BytesIO(payload),
        as_attachment=False,
        filename=Path(name).name,
        content_type=content_type,
    )
    response["Cache-Control"] = "public, max-age=86400"
    return response


def _read_media(name: str) -> tuple[bytes, str]:
    from src.core.models import StoredMedia

    if default_storage.exists(name):
        with default_storage.open(name, "rb") as handle:
            payload = handle.read()
        if payload:
            return payload, _content_type_for(name)
    row = StoredMedia.objects.filter(name=name).first()
    if row is not None:
        return bytes(row.content), row.content_type or _content_type_for(name)
    raise Http404()
