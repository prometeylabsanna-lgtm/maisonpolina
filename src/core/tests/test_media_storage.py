from io import BytesIO

import pytest
from django.core.files.base import ContentFile
from django.http import Http404
from PIL import Image

from src.core.media_storage import (
    DatabaseFileStorage,
    _safe_media_path,
    serve_media,
)
from src.core.models import StoredMedia


def _jpeg_bytes(size=(24, 16), color=(40, 12, 16)) -> bytes:
    buf = BytesIO()
    Image.new("RGB", size, color).save(buf, format="JPEG")
    return buf.getvalue()


def test_safe_media_path_rejects_traversal():
    with pytest.raises(Http404):
        _safe_media_path("../secret.txt")
    with pytest.raises(Http404):
        _safe_media_path("foo/../../etc/passwd")
    assert _safe_media_path("blocks/shot.webp") == "blocks/shot.webp"
    assert _safe_media_path("/blocks/shot.webp") == "blocks/shot.webp"


@pytest.mark.django_db
def test_database_storage_roundtrip():
    storage = DatabaseFileStorage()
    name = storage.save(
        "blocks/about.webp",
        ContentFile(_jpeg_bytes(), name="about.webp"),
    )
    assert name == "blocks/about.webp"
    assert storage.exists(name)
    assert storage.size(name) > 0
    assert storage.url(name) == "/media/blocks/about.webp"
    assert storage.open(name).read()[:2] == b"\xff\xd8"
    storage.delete(name)
    assert not storage.exists(name)


@pytest.mark.django_db
def test_serve_media_from_stored_row(client):
    payload = _jpeg_bytes()
    StoredMedia.objects.create(
        name="blocks/event.jpg",
        content=payload,
        content_type="image/jpeg",
        size=len(payload),
    )
    response = client.get("/media/blocks/event.jpg")
    assert response.status_code == 200
    assert response["Content-Type"].startswith("image/jpeg")
    assert b"".join(response.streaming_content) == payload


@pytest.mark.django_db
def test_serve_media_missing_is_404(client):
    response = client.get("/media/blocks/missing.webp")
    assert response.status_code == 404


@pytest.mark.django_db
def test_serve_media_view_rejects_traversal(rf):
    request = rf.get("/media/../secret")
    with pytest.raises(Http404):
        serve_media(request, "../secret")
