from django.core.management.base import BaseCommand

from src.core.block_defaults import BLOCK_DEFAULTS, IMAGE_KEYS, block_content_type
from src.core.models import PersonalityItem, SeoMeta, SiteBlock, SiteSettings
from src.core.personality_item_defaults import PERSONALITY_ITEM_DEFAULTS
from src.core.seed_catalog import (
    COMPANY_LEGAL_NAME,
    FAQ_SEED,
    FORMAT_SEED,
    GALLERY_SEED,
    HOME_SEO,
    LOCATION_EN,
    LOCATION_RU,
    PLACEHOLDER_EMAILS,
    TESTIMONIAL_SEED,
)
from src.core.style_defaults import ensure_section_styles
from src.faq.models import FaqItem
from src.formats.models import FormatFeature, ServiceFormat
from src.gallery.models import GalleryPhoto
from src.reviews.models import Testimonial


class Command(BaseCommand):
    help = "Idempotent seed of SiteBlocks, section styles, formats, reviews, FAQ"

    def add_arguments(self, parser):
        parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Replace existing CMS texts and catalog rows with Ads-safe defaults",
        )

    def handle(self, *args, **options):
        overwrite = bool(options.get("overwrite"))
        self._seed_settings(overwrite=overwrite)
        created_blocks, updated_blocks = self._seed_blocks(overwrite=overwrite)
        styles_created = ensure_section_styles()
        self._seed_seo(overwrite=overwrite)
        self._seed_formats(overwrite=overwrite)
        self._seed_testimonials(overwrite=overwrite)
        self._seed_faq(overwrite=overwrite)
        self._seed_gallery(overwrite=overwrite)
        self._seed_personality_items(overwrite=overwrite)
        self.stdout.write(
            self.style.SUCCESS(
                f"Seed done. New blocks: {created_blocks}, "
                f"updated: {updated_blocks}, styles: {styles_created}, "
                f"overwrite={overwrite}"
            )
        )

    def _seed_settings(self, *, overwrite: bool) -> None:
        settings = SiteSettings.get_solo()
        fields: list[str] = []
        if overwrite or settings.location_ru in (
            "Київ, за домовленістю",
            "Москва, по договорённости",
            "Киев, по договорённости",
            "ЖК «Нова Конча-Заспа»",
            "вул. Феодосія Печерського, 1, Ходосівка, Київська область, 08173",
            "",
        ):
            settings.location_ru = LOCATION_RU
            fields.append("location_ru")
        if overwrite or settings.location_en in (
            "Kyiv, by arrangement",
            "Moscow, by arrangement",
            "Kyiv, by appointment",
            "Nova Koncha-Zaspa RC",
            "1 Feodosiia Pecherskyi St, Khodosivka, Kyiv Oblast, 08173",
            "",
        ):
            settings.location_en = LOCATION_EN
            fields.append("location_en")
        if overwrite or (settings.company_legal_name or "").strip() in (
            "",
            "MaisonPolina",
        ):
            settings.company_legal_name = COMPANY_LEGAL_NAME
            fields.append("company_legal_name")
        if overwrite or settings.copyright_name in (
            "MAISON POLINA",
            "MaisonPolina",
            "Полина",
            "",
        ):
            settings.copyright_name = COMPANY_LEGAL_NAME
            fields.append("copyright_name")
        email = (settings.email or "").strip().lower()
        if overwrite or email in PLACEHOLDER_EMAILS:
            settings.email = ""
            fields.append("email")
        if fields:
            settings.save(update_fields=[*fields])

    def _seed_blocks(self, *, overwrite: bool) -> tuple[int, int]:
        created_blocks = 0
        updated_blocks = 0
        for (page, key), defaults in BLOCK_DEFAULTS.items():
            label = defaults.get("label", key)
            text_ru = defaults.get("text_ru", "")
            text_en = defaults.get("text_en", "")
            content_type = block_content_type(key)
            block, created = SiteBlock.objects.get_or_create(
                page=page,
                key=key,
                defaults={
                    "label": label,
                    "text_ru": text_ru,
                    "text_en": text_en,
                    "content_type": content_type,
                    "is_active": True,
                    "sort_order": 0,
                },
            )
            if created:
                created_blocks += 1
                continue
            update_fields: list[str] = []
            if label and block.label != label:
                block.label = label
                update_fields.append("label")
            if overwrite:
                if block.text_ru != text_ru:
                    block.text_ru = text_ru
                    update_fields.append("text_ru")
                if block.text_en != text_en:
                    block.text_en = text_en
                    update_fields.append("text_en")
                if block.content_type != content_type:
                    block.content_type = content_type
                    update_fields.append("content_type")
                if key in IMAGE_KEYS and block.image:
                    block.image = None
                    update_fields.append("image")
                if key in IMAGE_KEYS and block.video_file:
                    block.video_file = None
                    update_fields.append("video_file")
                if key in IMAGE_KEYS and (block.video_url or "").strip():
                    block.video_url = ""
                    update_fields.append("video_url")
            if update_fields:
                # Drop duplicates while keeping order
                seen: set[str] = set()
                unique_fields: list[str] = []
                for field in [*update_fields, "updated_at"]:
                    if field not in seen:
                        seen.add(field)
                        unique_fields.append(field)
                block.save(update_fields=unique_fields)
                updated_blocks += 1
        return created_blocks, updated_blocks

    def _seed_seo(self, *, overwrite: bool) -> None:
        seo, created = SeoMeta.objects.get_or_create(
            page="home",
            defaults=HOME_SEO,
        )
        if not created and overwrite:
            for field, value in HOME_SEO.items():
                setattr(seo, field, value)
            seo.save(update_fields=[*HOME_SEO.keys()])
        SeoMeta.objects.get_or_create(
            page="privacy",
            defaults={
                "title_ru": "Политика конфиденциальности",
                "title_en": "Privacy policy",
                "description_ru": "Порядок обработки персональных данных.",
                "description_en": "How personal data is processed.",
            },
        )
        SeoMeta.objects.get_or_create(
            page="terms",
            defaults={
                "title_ru": "Условия использования — Maison Polina",
                "title_en": "Terms of use — Maison Polina",
                "description_ru": "Условия использования сайта и информационных материалов Maison Polina.",
                "description_en": "Terms of use for the Maison Polina website and informational materials.",
            },
        )

    def _seed_personality_items(self, *, overwrite: bool) -> None:
        if PersonalityItem.objects.exists() and not overwrite:
            return
        if overwrite:
            PersonalityItem.objects.all().delete()
        for group, order, label_ru, label_en, value_ru, value_en in PERSONALITY_ITEM_DEFAULTS:
            PersonalityItem.objects.create(
                group=group,
                order=order,
                label_ru=label_ru,
                label_en=label_en,
                value_ru=value_ru,
                value_en=value_en,
                is_active=True,
            )

    def _seed_gallery(self, *, overwrite: bool) -> None:
        keep_paths = {path for path, _, _ in GALLERY_SEED}
        for order, (path, caption_ru, caption_en) in enumerate(GALLERY_SEED, start=1):
            name = path.rsplit("/", 1)[-1]
            existing = (
                GalleryPhoto.objects.filter(static_image=path).first()
                or GalleryPhoto.objects.filter(image__endswith=name).first()
            )
            if existing:
                fields: list[str] = []
                if existing.static_image != path:
                    existing.static_image = path
                    fields.append("static_image")
                if overwrite or existing.caption_ru in ("Кадр вечера",):
                    existing.caption_ru = caption_ru
                    existing.caption_en = caption_en
                    existing.alt_ru = caption_ru
                    existing.alt_en = caption_en
                    fields.extend(["caption_ru", "caption_en", "alt_ru", "alt_en"])
                if existing.order != order:
                    existing.order = order
                    fields.append("order")
                if not existing.is_active:
                    existing.is_active = True
                    fields.append("is_active")
                if fields:
                    existing.save(update_fields=fields)
                continue
            GalleryPhoto.objects.create(
                static_image=path,
                caption_ru=caption_ru,
                caption_en=caption_en,
                alt_ru=caption_ru,
                alt_en=caption_en,
                order=order,
                is_active=True,
            )
        if overwrite:
            GalleryPhoto.objects.exclude(static_image__in=keep_paths).update(
                is_active=False
            )

    def _seed_formats(self, *, overwrite: bool) -> None:
        if ServiceFormat.objects.exists() and not overwrite:
            return
        if overwrite:
            FormatFeature.objects.all().delete()
            ServiceFormat.objects.all().delete()
        for item in FORMAT_SEED:
            payload = dict(item)
            features = payload.pop("features")
            fmt = ServiceFormat.objects.create(**payload)
            for idx, (ru, en) in enumerate(features):
                FormatFeature.objects.create(
                    service=fmt, text_ru=ru, text_en=en, order=idx
                )

    def _seed_testimonials(self, *, overwrite: bool) -> None:
        if Testimonial.objects.exists() and not overwrite:
            return
        if overwrite:
            Testimonial.objects.all().delete()
        for item in TESTIMONIAL_SEED:
            Testimonial.objects.create(**item)

    def _seed_faq(self, *, overwrite: bool) -> None:
        if FaqItem.objects.exists() and not overwrite:
            return
        if overwrite:
            FaqItem.objects.all().delete()
        for item in FAQ_SEED:
            FaqItem.objects.create(**item)
