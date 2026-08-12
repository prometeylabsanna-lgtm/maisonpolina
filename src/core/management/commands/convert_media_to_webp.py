from pathlib import Path

from django.apps import apps
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db.models.fields.files import ImageField

from src.core.webp import convert_bytes_to_webp, webp_name

OUR_APPS = {"core", "gallery", "formats", "reviews"}


class Command(BaseCommand):
    help = "Convert existing ImageField media (JPG/PNG/…) to WebP and update DB paths"

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument(
            "--keep-original",
            action="store_true",
            help="Do not delete the source file after convert",
        )

    def handle(self, *args, **options):
        dry = options["dry_run"]
        keep = options["keep_original"]
        converted = 0
        skipped = 0
        for model in apps.get_models():
            if model._meta.app_label not in OUR_APPS:
                continue
            if model._meta.proxy:
                continue
            image_fields = [
                field
                for field in model._meta.get_fields()
                if isinstance(field, ImageField)
            ]
            if not image_fields:
                continue
            for obj in model.objects.all().iterator():
                for field in image_fields:
                    status = self._convert_field(obj, field, dry=dry, keep=keep)
                    if status == "converted":
                        converted += 1
                    elif status == "skipped":
                        skipped += 1
        self.stdout.write(f"converted={converted} skipped={skipped}")

    def _convert_field(self, obj, field: ImageField, *, dry: bool, keep: bool) -> str:
        file = getattr(obj, field.attname)
        if not file or not file.name:
            return ""
        if Path(file.name).suffix.lower() == ".webp":
            return "skipped"
        try:
            file.open("rb")
            data = file.read()
        except (FileNotFoundError, OSError, ValueError):
            return "skipped"
        finally:
            file.close()
        result = convert_bytes_to_webp(data, file.name)
        if result is None:
            return "skipped"
        payload, new_basename = result
        new_name = str(Path(file.name).with_name(Path(new_basename).name))
        if dry:
            self.stdout.write(f"would convert {file.name} -> {new_name}")
            return "converted"
        old_name = file.name
        file.save(Path(new_name).name, ContentFile(payload, name=webp_name(new_name)), save=True)
        if not keep and old_name != file.name:
            try:
                file.storage.delete(old_name)
            except OSError:
                pass
        self.stdout.write(f"{old_name} -> {file.name}")
        return "converted"
