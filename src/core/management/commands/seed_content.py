from django.core.management.base import BaseCommand

from src.core.block_defaults import BLOCK_DEFAULTS
from src.core.models import SeoMeta, SiteBlock, SiteSettings
from src.faq.models import FaqItem
from src.formats.models import FormatFeature, ServiceFormat
from src.gallery.models import GalleryPhoto
from src.reviews.models import Testimonial


class Command(BaseCommand):
    help = "Idempotent seed of SiteBlocks, formats, reviews, FAQ"

    def handle(self, *args, **options):
        settings = SiteSettings.get_solo()
        if settings.location_ru in (
            "Київ, за домовленістю",
            "Москва, по договорённости",
            "",
        ):
            settings.location_ru = "Киев, по договорённости"
        if settings.location_en in (
            "Kyiv, by arrangement",
            "Moscow, by arrangement",
            "",
        ):
            settings.location_en = "Kyiv, by appointment"
        settings.save(update_fields=["location_ru", "location_en"])
        created_blocks = 0
        for (page, key), defaults in BLOCK_DEFAULTS.items():
            _, created = SiteBlock.objects.get_or_create(
                page=page,
                key=key,
                defaults={
                    "label": defaults.get("label", key),
                    "text_ru": defaults.get("text_ru", ""),
                    "text_en": defaults.get("text_en", ""),
                    "is_visible": defaults.get("is_visible", True),
                },
            )
            if created:
                created_blocks += 1

        SeoMeta.objects.get_or_create(
            page="home",
            defaults={
                "title_ru": "Полина",
                "title_en": "Polina",
                "description_ru": (
                    "Приватное сопровождение на ужины, приёмы и деловые поездки."
                ),
                "description_en": (
                    "Private companionship for dinners, receptions and business trips."
                ),
            },
        )
        SeoMeta.objects.get_or_create(
            page="privacy",
            defaults={
                "title_ru": "Политика конфиденциальности",
                "title_en": "Privacy policy",
                "description_ru": "Порядок обработки персональных данных.",
                "description_en": "How personal data is processed.",
            },
        )

        self._seed_formats()
        self._seed_testimonials()
        self._seed_faq()
        self._seed_gallery()
        self.stdout.write(
            self.style.SUCCESS(f"Seed done. New blocks: {created_blocks}")
        )

    def _seed_gallery(self) -> None:
        """Ship gallery from static/images/gallery (Vercel-safe, like AJERES)."""
        items = [
            ("images/gallery/gallery-01.jpg", "Кадр вечера", "Evening frame"),
            ("images/gallery/gallery-02.jpg", "Кадр вечера", "Evening frame"),
            ("images/gallery/gallery-03.jpg", "Кадр вечера", "Evening frame"),
            ("images/gallery/gallery-04.jpg", "Кадр вечера", "Evening frame"),
            ("images/gallery/gallery-05.jpg", "Кадр вечера", "Evening frame"),
            ("images/gallery/gallery-06.jpg", "Кадр вечера", "Evening frame"),
        ]
        for order, (path, caption_ru, caption_en) in enumerate(items, start=1):
            name = path.rsplit("/", 1)[-1]
            existing = (
                GalleryPhoto.objects.filter(static_image=path).first()
                or GalleryPhoto.objects.filter(image__endswith=name).first()
            )
            if existing:
                if existing.static_image != path:
                    existing.static_image = path
                    existing.save(update_fields=["static_image"])
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

    def _seed_formats(self) -> None:
        if ServiceFormat.objects.exists():
            return
        data = [
            {
                "title_ru": "Знакомство",
                "title_en": "Introduction",
                "label_ru": "Формат I",
                "label_en": "Format I",
                "description_ru": (
                    "Полтора часа личной беседы: цель обращения, формат встреч, "
                    "взаимные ожидания."
                ),
                "description_en": (
                    "An hour and a half of private conversation: purpose, "
                    "meeting format, mutual expectations."
                ),
                "price_text_ru": "400 $",
                "price_text_en": "400 $",
                "is_featured": False,
                "order": 1,
                "features": [
                    ("Обсуждение формата и целей", "Discussion of format and goals"),
                    ("Условия конфиденциальности", "Privacy terms"),
                ],
            },
            {
                "title_ru": "Сопровождение на вечер",
                "title_en": "Evening accompaniment",
                "label_ru": "Формат II",
                "label_en": "Format II",
                "description_ru": (
                    "Полное сопровождение делового приёма, премьеры или ужина — "
                    "от встречи до прощания."
                ),
                "description_en": (
                    "Full accompaniment for a business reception, premiere or dinner — "
                    "from greeting to farewell."
                ),
                "price_text_ru": "1000 $",
                "price_text_en": "1000 $",
                "is_featured": True,
                "order": 2,
                "features": [
                    (
                        "Индивидуальный бриф перед встречей",
                        "Individual brief before the meeting",
                    ),
                    (
                        "Сопровождение на протяжении вечера",
                        "Accompaniment throughout the evening",
                    ),
                    ("Соглашение о неразглашении", "Non-disclosure agreement"),
                    (
                        "Логистика и транспорт по согласованию",
                        "Logistics and transport by arrangement",
                    ),
                ],
            },
            {
                "title_ru": "Поездка",
                "title_en": "Trip",
                "label_ru": "Формат III",
                "label_en": "Format III",
                "description_ru": (
                    "Сопровождение в деловой или частной поездке — "
                    "от выезда до возвращения. "
                    "Отдельная комната для меня — обязательное условие."
                ),
                "description_en": (
                    "Accompaniment on a business or private trip — "
                    "from departure to return. "
                    "A separate room for me is required."
                ),
                "price_text_ru": "По договорённости",
                "price_text_en": "By arrangement",
                "is_featured": False,
                "order": 3,
                "features": [
                    (
                        "Согласование маршрута и расписания",
                        "Itinerary and schedule alignment",
                    ),
                    (
                        "Присутствие на встречах и событиях",
                        "Presence at meetings and events",
                    ),
                    (
                        "Логистика и связь на всём пути",
                        "Logistics and contact throughout the trip",
                    ),
                ],
            },
        ]
        for item in data:
            features = item.pop("features")
            fmt = ServiceFormat.objects.create(**item)
            for idx, (ru, en) in enumerate(features):
                FormatFeature.objects.create(
                    service=fmt, text_ru=ru, text_en=en, order=idx
                )

    def _seed_testimonials(self) -> None:
        if Testimonial.objects.exists():
            return
        items = [
            {
                "author_name": "Марина Т.",
                "role_ru": "Основатель инвестиционного фонда",
                "role_en": "Founder of an investment fund",
                "text_ru": (
                    "Полина сопровождала меня на переговорах длиной в целый год. "
                    "Ни одной неловкой паузы — и ни одной ситуации, где я чувствовала "
                    "себя не на месте."
                ),
                "text_en": (
                    "Polina accompanied me through a year of negotiations. "
                    "Not a single awkward pause — and never a moment when I felt out of place."
                ),
                "order": 1,
            },
            {
                "author_name": "Александр Г.",
                "role_ru": "Дирижёр",
                "role_en": "Conductor",
                "text_ru": (
                    "Работа тихая и очень точная. Она не переделывает ситуацию, "
                    "она убирает всё, что мешает её увидеть."
                ),
                "text_en": (
                    "The work is quiet and precise. She does not reshape the situation — "
                    "she removes what prevents seeing it."
                ),
                "order": 2,
            },
            {
                "author_name": "Ольга Р.",
                "role_ru": "Дипломатическая служба",
                "role_en": "Diplomatic service",
                "text_ru": (
                    "Три поездки, четыре страны, ни одной ошибки в графике. "
                    "Это дороже любых консультаций по этикету."
                ),
                "text_en": (
                    "Three trips, four countries, not a single scheduling error. "
                    "Worth more than any etiquette consulting."
                ),
                "order": 3,
            },
        ]
        for item in items:
            Testimonial.objects.create(**item)

    def _seed_faq(self) -> None:
        if FaqItem.objects.exists():
            return
        items = [
            {
                "question_ru": "Как проходит первая встреча?",
                "question_en": "How does the first meeting work?",
                "answer_ru": (
                    "Мы начинаем с короткого знакомства: цели, формат, взаимные "
                    "ожидания. Если всё подходит — согласуем следующую дату."
                ),
                "answer_en": (
                    "We start with a short introduction: goals, format, mutual "
                    "expectations. If it fits — we agree on the next date."
                ),
                "order": 1,
            },
            {
                "question_ru": "Где проходят встречи?",
                "question_en": "Where do meetings take place?",
                "answer_ru": (
                    "В Киеве и по договорённости в других городах. "
                    "Логистика за пределами города обсуждается отдельно."
                ),
                "answer_en": (
                    "In Kyiv and, by arrangement, in other cities. "
                    "Travel outside the city is discussed separately."
                ),
                "order": 2,
            },
            {
                "question_ru": "Сохраняется ли конфиденциальность?",
                "question_en": "Is privacy preserved?",
                "answer_ru": (
                    "Да. Имена и детали встреч остаются между нами. "
                    "При необходимости подписывается соглашение о неразглашении."
                ),
                "answer_en": (
                    "Yes. Names and meeting details stay between us. "
                    "A non-disclosure agreement can be signed when needed."
                ),
                "order": 3,
            },
            {
                "question_ru": "За сколько нужно бронировать дату?",
                "question_en": "How far in advance should I book?",
                "answer_ru": (
                    "Желательно за 5–7 дней. Для поездок — раньше, чтобы согласовать график."
                ),
                "answer_en": (
                    "Preferably 5–7 days ahead. For travel — earlier, to align the schedule."
                ),
                "order": 4,
            },
            {
                "question_ru": "Как происходит оплата?",
                "question_en": "How does payment work?",
                "answer_ru": (
                    "Половина суммы при подтверждении даты, остаток — по завершении встречи."
                ),
                "answer_en": (
                    "Half the fee when the date is confirmed, the rest after the meeting."
                ),
                "order": 5,
            },
        ]
        for item in items:
            FaqItem.objects.create(**item)
