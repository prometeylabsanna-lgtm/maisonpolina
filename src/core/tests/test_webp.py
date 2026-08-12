from io import BytesIO
from pathlib import Path

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from src.core.admin_site_content_form import SitePageContentForm, load_section_blocks
from src.core.fields import AdminWebPImageField
from src.core.models import SiteBlock, SiteSettings
from src.core.site_content_registry import get_section
from src.core.webp import convert_bytes_to_webp, convert_path_to_webp
from src.gallery.models import GalleryPhoto


def _jpeg_bytes(size=(24, 16), color=(40, 12, 16)) -> bytes:
    buf = BytesIO()
    Image.new("RGB", size, color).save(buf, format="JPEG")
    return buf.getvalue()


def _png_rgba_bytes() -> bytes:
    buf = BytesIO()
    Image.new("RGBA", (12, 12), (200, 160, 80, 128)).save(buf, format="PNG")
    return buf.getvalue()


def test_convert_jpeg_bytes_to_webp():
    payload, name = convert_bytes_to_webp(_jpeg_bytes(), "portrait.jpg")
    assert name == "portrait.webp"
    assert payload[:4] == b"RIFF"
    with Image.open(BytesIO(payload)) as image:
        assert image.format == "WEBP"


def test_skip_webp_and_svg():
    assert convert_bytes_to_webp(b"not-an-image", "a.webp") is None
    assert convert_bytes_to_webp(_jpeg_bytes(), "icon.svg") is None


def test_convert_path_replace(tmp_path: Path):
    source = tmp_path / "shot.png"
    source.write_bytes(_png_rgba_bytes())
    target = convert_path_to_webp(source, replace=True)
    assert target == tmp_path / "shot.webp"
    assert target.is_file()
    assert not source.exists()


@pytest.mark.django_db
def test_admin_imagefield_saves_webp():
    block, _ = SiteBlock.objects.get_or_create(
        page="home",
        key="about.portrait",
        defaults={"content_type": SiteBlock.ContentType.IMAGE, "is_active": True},
    )
    block.image.save(
        "face.jpg",
        SimpleUploadedFile("face.jpg", _jpeg_bytes(), content_type="image/jpeg"),
        save=True,
    )
    assert block.image.name.endswith(".webp")
    with Image.open(block.image.path) as image:
        assert image.format == "WEBP"


@pytest.mark.django_db
def test_gallery_upload_becomes_webp():
    photo = GalleryPhoto.objects.create(alt_ru="Кадр", order=1)
    photo.image.save(
        "gallery-new.png",
        SimpleUploadedFile("gallery-new.png", _png_rgba_bytes(), content_type="image/png"),
        save=True,
    )
    assert photo.image.name.endswith(".webp")


def test_admin_form_field_converts_on_clean():
    field = AdminWebPImageField(required=False)
    uploaded = SimpleUploadedFile(
        "hero.jpg", _jpeg_bytes(), content_type="image/jpeg"
    )
    result = field.clean(uploaded)
    assert result.name.endswith(".webp")
    with Image.open(result) as image:
        assert image.format == "WEBP"


@pytest.mark.django_db
def test_cms_admin_form_upload_saves_webp():
    SiteSettings.get_solo()
    section = get_section("home", "about")
    assert section is not None
    blocks = load_section_blocks(section)
    field_name = "block__home__about.portrait__image"
    uploaded = SimpleUploadedFile(
        "portrait.jpg", _jpeg_bytes(), content_type="image/jpeg"
    )
    form = SitePageContentForm(
        section,
        blocks,
        data={},
        files={field_name: uploaded},
    )
    assert form.is_valid(), form.errors
    form.save()
    block = SiteBlock.objects.get(page="home", key="about.portrait")
    assert block.image.name.endswith(".webp")

