"""Canonical seed payloads for formats, FAQ, gallery and SEO (Ads-safe)."""

from __future__ import annotations

FORMAT_SEED: list[dict] = [
    {
        "title_ru": "Оценка потребностей",
        "title_en": "Needs Assessment",
        "label_ru": "Формат I",
        "label_en": "Format I",
        "description_ru": (
            "Конфиденциальная консультация для определения ваших требований "
            "к стилю жизни и ожиданий от поездок."
        ),
        "description_en": (
            "Confidential consultation to define your lifestyle requirements "
            "and travel expectations."
        ),
        "price_text_ru": "Консультация",
        "price_text_en": "Consultation fee",
        "is_featured": False,
        "order": 1,
        "features": [
            (
                "Обсуждение целей, подписание NDA",
                "Discussion of goals, NDA signing",
            ),
            (
                "Оплачивается как консультация",
                "Consultation fee applies",
            ),
        ],
    },
    {
        "title_ru": "Координация гала-вечеров и корпоративных мероприятий",
        "title_en": "Gala & Corporate Event Coordination",
        "label_ru": "Формат II",
        "label_en": "Format II",
        "description_ru": (
            "Комплексная организация вашего участия в премьерах, гала-вечерах "
            "и закрытых корпоративных ужинах. Обеспечение безупречного выполнения "
            "вашего графика."
        ),
        "description_en": (
            "End-to-end coordination of your attendance at premieres, galas, "
            "and high-stakes corporate dinners. Ensuring flawless execution "
            "of your schedule."
        ),
        "price_text_ru": "от 1000 $",
        "price_text_en": "from $1000",
        "is_featured": True,
        "order": 2,
        "features": [
            (
                "Брифинг по мероприятию",
                "Event briefing",
            ),
            (
                "Управление логистикой на месте",
                "On-site logistics management",
            ),
            (
                "Строгое соблюдение NDA",
                "Strict NDA",
            ),
            (
                "Ставки начинаются от $1000",
                "Rates starting from $1000",
            ),
        ],
    },
    {
        "title_ru": "Глобальный консьерж и поездки",
        "title_en": "Global Concierge & Travel",
        "label_ru": "Формат III",
        "label_en": "Format III",
        "description_ru": (
            "Полное управление вашим маршрутом, логистикой на месте и комплексная "
            "операционная поддержка во время частных или деловых поездок."
        ),
        "description_en": (
            "Complete management of your itinerary, on-ground logistics, and "
            "comprehensive operational support during confidential or business trips."
        ),
        "price_text_ru": "По договорённости",
        "price_text_en": "By arrangement",
        "is_featured": False,
        "order": 3,
        "features": [
            (
                "Согласование графика",
                "Schedule alignment",
            ),
            (
                "Управление логистикой",
                "Logistics management",
            ),
            (
                "Координация подрядчиков",
                "Vendor coordination",
            ),
        ],
    },
]

FAQ_SEED: list[dict] = [
    {
        "question_ru": "Как проходит первая консультация?",
        "question_en": "How does the initial consultation work?",
        "answer_ru": (
            "Мы определяем ваши потребности и согласовываем ожидания в отношении "
            "приватности и логистики. Если наши видения совпадают, мы подписываем "
            "соглашение о неразглашении (NDA)."
        ),
        "answer_en": (
            "We outline your lifestyle needs and set mutual expectations regarding "
            "privacy and logistics. If our visions match, we sign a Non-Disclosure "
            "Agreement (NDA)."
        ),
        "order": 1,
    },
    {
        "question_ru": "Где проходят консультации?",
        "question_en": "Where do consultations take place?",
        "answer_ru": (
            "В Киеве и, по предварительной договоренности, по всему миру. "
            "Логистика поездок обсуждается отдельно."
        ),
        "answer_en": (
            "In Kyiv and, by arrangement, globally. "
            "Travel logistics are discussed separately."
        ),
        "order": 2,
    },
    {
        "question_ru": "Сохраняется ли конфиденциальность?",
        "question_en": "Is privacy preserved?",
        "answer_ru": (
            "Да. Конфиденциальность — основа услуг консьержа. Ваша личность и маршрут "
            "остаются в строгой тайне в рамках NDA."
        ),
        "answer_en": (
            "Yes. Discretion is the core of concierge services. Your identity and "
            "itinerary remain strictly confidential under an NDA."
        ),
        "order": 3,
    },
    {
        "question_ru": "За какое время необходимо делать бронирование?",
        "question_en": "How far in advance should I book?",
        "answer_ru": (
            "Желательно за 5–7 дней. Для координации международных поездок — раньше, "
            "чтобы успеть согласовать график."
        ),
        "answer_en": (
            "Preferably 5–7 days ahead. For global travel coordination — earlier, "
            "to align the schedule."
        ),
        "order": 4,
    },
]

GALLERY_SEED: list[tuple[str, str, str]] = [
    (
        "images/gallery/gallery-01.jpg",
        "Деловой портрет на мероприятии",
        "Business portrait at an event",
    ),
    (
        "images/gallery/gallery-02.jpg",
        "Координация на площадке",
        "On-site coordination",
    ),
    (
        "images/gallery/gallery-03.jpg",
        "Премиальный деловой образ",
        "Premium business look",
    ),
    (
        "images/gallery/gallery-04.jpg",
        "Международное деловое мероприятие",
        "International business event",
    ),
    (
        "images/gallery/gallery-05.jpg",
        "Студийный деловой портрет",
        "Studio business portrait",
    ),
]

HOME_SEO = {
    "title_ru": "Maison Polina — премиальный бизнес-консьерж",
    "title_en": "Maison Polina — Premium Executive Concierge",
    "description_ru": (
        "Управление стилем жизни, координация премиальных поездок и поддержка "
        "на мероприятиях для лидеров индустрии и дипломатов."
    ),
    "description_en": (
        "Lifestyle management, premium travel coordination, and event assistance "
        "for industry leaders and diplomats."
    ),
}

LOCATION_RU = "ЖК Новая Конча-Заспа, Ходосовка, Киевская область, 08173"
LOCATION_EN = "Nova Koncha Zaspa RC, Khodosivka, Kyiv Oblast, 08173"
COMPANY_LEGAL_NAME = "Maison Polina"

PLACEHOLDER_EMAILS = frozenset(
    {
        "",
        "hello@example.com",
        "admin@example.com",
    }
)

TESTIMONIAL_SEED: list[dict] = [
    {
        "author_name_ru": "Дмитрий К.",
        "author_name_en": "Dmitry K.",
        "role_ru": "Основатель инвестиционного фонда",
        "role_en": "Founder of an investment fund",
        "text_ru": (
            "Команда Maison Polina вела логистику наших переговоров целый год. "
            "Ни одной срыва в графике — и полное ощущение контроля над процессом."
        ),
        "text_en": (
            "The Maison Polina team managed logistics for our negotiations for a year. "
            "Not a single schedule failure — and a clear sense of process control."
        ),
        "order": 1,
    },
    {
        "author_name_ru": "Александр Г.",
        "author_name_en": "Alexander G.",
        "role_ru": "Дирижёр",
        "role_en": "Conductor",
        "text_ru": (
            "Работа тихая и очень точная. Они не переделывают ситуацию — "
            "убирают всё, что мешает её увидеть."
        ),
        "text_en": (
            "The work is quiet and precise. They do not reshape the situation — "
            "they remove what prevents seeing it."
        ),
        "order": 2,
    },
    {
        "author_name_ru": "Андрей М.",
        "author_name_en": "Andrey M.",
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
