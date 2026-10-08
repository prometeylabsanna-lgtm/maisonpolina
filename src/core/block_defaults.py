"""Default SiteBlock values. No model imports — safe at import time."""

from src.core.block_defaults_chrome import CHROME_BLOCK_DEFAULTS

IMAGE_KEYS: frozenset[str] = frozenset(
    {
        "hero.media",
        "about.portrait",
        "personality.portrait",
        "contacts.bg",
    }
)

VIDEO_KEYS: frozenset[str] = frozenset({"hero.media"})

CHOICE_KEYS: dict[str, tuple[tuple[str, str], ...]] = {
    "hero.media_layout": (
        ("half", "Половина секции"),
        ("full", "На весь фон"),
    ),
}

# Static fallbacks shown on the site when SiteBlock.image is empty (same as templates/).
IMAGE_STATIC_FALLBACKS: dict[str, str] = {
    "hero.media": "images/hero-portrait.png",
    "about.portrait": "images/about-portrait.jpg",
    "personality.portrait": "images/personality-portrait.jpg",
    "contacts.bg": "images/contacts-bg.jpg",
}


def is_visibility_key(key: str) -> bool:
    return key.endswith("_section_visible") or key.endswith("_visible")


def block_content_type(key: str) -> str:
    return "image" if key in IMAGE_KEYS else "text"


# (page, key) -> dict with text_ru, text_en, label
_PAGE_BLOCK_DEFAULTS: dict[tuple[str, str], dict] = {
    ("home", "hero_section_visible"): {
        "label": "Баннер — видимость",
        "text_ru": "1",
        "text_en": "1",
    },
    ("home", "hero.title"): {
        "label": "Баннер — имя",
        "text_ru": "MAISON POLINA",
        "text_en": "MAISON POLINA",
    },
    ("home", "hero.subtitle"): {
        "label": "Баннер — подзаголовок",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "hero.lead"): {
        "label": "Баннер — текст",
        "text_ru": (
            "Премиальный бизнес-консьерж. Мы ценим ваше время, приватность и статус. "
            "Безупречное управление стилем жизни, координация премиальных поездок "
            "и поддержка на мероприятиях высшего уровня для лидеров индустрии и дипломатов."
        ),
        "text_en": (
            "Premium Executive Concierge. We value your time, privacy, and status. "
            "Seamless lifestyle management, high-end travel coordination, and premium "
            "event assistance tailored for industry leaders and diplomats."
        ),
    },
    ("home", "hero.cta_primary"): {
        "label": "Баннер — главная кнопка",
        "text_ru": "Оставить заявку",
        "text_en": "Send a request",
    },
    ("home", "hero.cta_secondary"): {
        "label": "Баннер — вторая кнопка",
        "text_ru": "Услуги и цены",
        "text_en": "Services and rates",
    },
    ("home", "hero.tagline"): {
        "label": "Баннер — слоган",
        "text_ru": "НЕЗАВИСИМОСТЬ · КОНФИДЕНЦИАЛЬНОСТЬ · ПРОФЕССИОНАЛИЗМ",
        "text_en": "INDEPENDENT · CONFIDENTIAL · PROFESSIONAL",
    },
    ("home", "hero.media"): {
        "label": "Баннер — фото",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "hero.media_layout"): {
        "label": "Баннер — размер фото",
        "text_ru": "half",
        "text_en": "half",
    },
    ("home", "about_section_visible"): {
        "label": "Обо мне — видимость",
        "text_ru": "1",
        "text_en": "1",
    },
    ("home", "about.eyebrow"): {
        "label": "Обо мне — надзаголовок",
        "text_ru": "О компании",
        "text_en": "About the agency",
    },
    ("home", "about.title"): {
        "label": "Обо мне — заголовок",
        "text_ru": "Управление премиальным",
        "text_en": "High-End Lifestyle",
    },
    ("home", "about.title_accent"): {
        "label": "Обо мне — акцент в заголовке",
        "text_ru": "стилем жизни",
        "text_en": "Management",
    },
    ("home", "about.body_1"): {
        "label": "Обо мне — абзац 1",
        "text_ru": (
            "Обладая обширной международной экспертизой и опытом работы в более чем "
            "20 странах, мы понимаем мировые стандарты премиального бизнеса. "
            "Специализируемся на индивидуальных маршрутах, координации статусных "
            "мероприятий и обеспечении безупречной реализации на местах и "
            "бесперебойной логистики для ваших самых важных событий. Наше агентство "
            "ведет ограниченное количество премиальных проектов ежемесячно, чтобы "
            "гарантировать максимальное внимание и высочайшее качество сервиса."
        ),
        "text_en": (
            "With extensive global expertise and operations across 20+ countries, "
            "we understand the global standards of premium business. Specialized in "
            "bespoke itineraries, high-profile event coordination, and ensuring "
            "flawless on-ground execution and seamless logistics for your most "
            "critical events. Our agency takes on a limited number of premium "
            "projects each month to guarantee full attention and exceptional "
            "service quality."
        ),
    },
    ("home", "about.body_2"): {
        "label": "Обо мне — абзац 2",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "about.body_3"): {
        "label": "Обо мне — абзац 3",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "about.quote"): {
        "label": "Обо мне — цитата",
        "text_ru": "Безупречный сервис незаметен, пока он вам не понадобится.",
        "text_en": "Impeccable service is invisible until you need it.",
    },
    ("home", "about.stat_1_value"): {
        "label": "Обо мне — цифра 1",
        "text_ru": "8",
        "text_en": "8",
    },
    ("home", "about.stat_1_label"): {
        "label": "Обо мне — подпись 1",
        "text_ru": "лет практики",
        "text_en": "years of practice",
    },
    ("home", "about.stat_2_value"): {
        "label": "Обо мне — цифра 2",
        "text_ru": "200+",
        "text_en": "200+",
    },
    ("home", "about.stat_2_label"): {
        "label": "Обо мне — подпись 2",
        "text_ru": "успешных проектов",
        "text_en": "projects concluded",
    },
    ("home", "about.stat_3_value"): {
        "label": "Обо мне — цифра 3",
        "text_ru": "6",
        "text_en": "6",
    },
    ("home", "about.stat_3_label"): {
        "label": "Обо мне — подпись 3",
        "text_ru": "активных клиентов в месяц",
        "text_en": "active clients per month",
    },
    ("home", "about.cta"): {
        "label": "Обо мне — кнопка",
        "text_ru": "Написать нам",
        "text_en": "Write to us",
    },
    ("home", "about.portrait"): {
        "label": "Обо мне — портрет",
        "text_ru": "Команда Maison Polina на мероприятии",
        "text_en": "Maison Polina team at an event",
    },
    ("home", "personality_section_visible"): {
        "label": "Личность — видимость",
        "text_ru": "1",
        "text_en": "1",
    },
    ("home", "personality.eyebrow"): {
        "label": "Личность — надзаголовок",
        "text_ru": "Экспертиза",
        "text_en": "Expertise",
    },
    ("home", "personality.title"): {
        "label": "Личность — заголовок (светлое слово)",
        "text_ru": "Профессиональный",
        "text_en": "Professional",
    },
    ("home", "personality.title_accent"): {
        "label": "Личность — акцент в заголовке",
        "text_ru": "профиль",
        "text_en": "Profile",
    },
    ("home", "personality.facts_title"): {
        "label": "Личность — подзаголовок параметров",
        "text_ru": "Ключевые компетенции",
        "text_en": "Core competencies",
    },
    ("home", "personality.age"): {
        "label": "Личность — возраст",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "personality.eyes"): {
        "label": "Личность — глаза",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "personality.hair"): {
        "label": "Личность — волосы",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "personality.height"): {
        "label": "Личность — рост",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "personality.weight"): {
        "label": "Личность — вес",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "personality.measurements"): {
        "label": "Личность — параметры",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "personality.shoes"): {
        "label": "Личность — обувь",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "personality.clothing"): {
        "label": "Личность — одежда",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "personality.zodiac"): {
        "label": "Личность — зодиак",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "personality.tattoo"): {
        "label": "Личность — тату",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "personality.piercing"): {
        "label": "Личность — пирсинг",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "personality.flowers"): {
        "label": "Личность — цветы",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "personality.cuisine"): {
        "label": "Личность — кухня",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "personality.alcohol"): {
        "label": "Личность — алкоголь",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "personality.smoking"): {
        "label": "Личность — курение",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "personality.extra_title"): {
        "label": "Личность — подзаголовок дополнительного (не используется)",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "personality.extra_1"): {
        "label": "Личность — пункт 1",
        "text_ru": "Опыт в премиальном hospitality",
        "text_en": "High-end hospitality background",
    },
    ("home", "personality.extra_2"): {
        "label": "Личность — пункт 2",
        "text_ru": "Event-менеджмент",
        "text_en": "Event Management",
    },
    ("home", "personality.extra_3"): {
        "label": "Личность — пункт 3",
        "text_ru": "PR и коммуникации",
        "text_en": "PR & Communications expert",
    },
    ("home", "personality.languages"): {
        "label": "Личность — мови",
        "text_ru": (
            "Ключевые компетенции: Управление стилем жизни, Деловой этикет, "
            "Кросс-культурная коммуникация."
        ),
        "text_en": (
            "Core Competencies: Lifestyle Management, Business Etiquette, "
            "Cross-cultural Communication."
        ),
    },
    ("home", "personality.respect"): {
        "label": "Личность — повес до культур",
        "text_ru": (
            "Языки: Английский, Русский, Украинский. Мы уважаем каждую культуру, "
            "религию и традицию. Работаем строго в рамках мировых корпоративных стандартов."
        ),
        "text_en": (
            "Languages: English, Russian, Ukrainian. We respect every culture, "
            "religion, and tradition. Operating strictly within global corporate standards."
        ),
    },
    ("home", "personality.education"): {
        "label": "Личность — образование",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "personality.travel"): {
        "label": "Личность — путешествия",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "personality.portrait"): {
        "label": "Личность — фото",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "gallery_section_visible"): {
        "label": "Галерея — видимость",
        "text_ru": "1",
        "text_en": "1",
    },
    ("home", "gallery.eyebrow"): {
        "label": "Галерея — надзаголовок",
        "text_ru": "Галерея",
        "text_en": "Gallery",
    },
    ("home", "gallery.title"): {
        "label": "Галерея — заголовок",
        "text_ru": "Кадры нашей",
        "text_en": "Frames from our",
    },
    ("home", "gallery.title_accent"): {
        "label": "Галерея — акцент",
        "text_ru": "работы",
        "text_en": "work",
    },
    ("home", "formats_section_visible"): {
        "label": "Форматы — видимость",
        "text_ru": "1",
        "text_en": "1",
    },
    ("home", "formats.eyebrow"): {
        "label": "Форматы — надзаголовок",
        "text_ru": "Услуги и цены",
        "text_en": "Services and rates",
    },
    ("home", "formats.title"): {
        "label": "Форматы — заголовок",
        "text_ru": "Три формата",
        "text_en": "Three formats of",
    },
    ("home", "formats.title_accent"): {
        "label": "Форматы — акцент",
        "text_ru": "премиального ассистирования",
        "text_en": "executive assistance",
    },
    ("home", "formats.note"): {
        "label": "Форматы — примечание",
        "text_ru": (
            "Аванс в размере 50% необходим для бронирования графика, "
            "остаток выплачивается по завершении проекта."
        ),
        "text_en": (
            "A 50% retainer is required to secure the schedule, "
            "with the balance due upon completion of the project."
        ),
    },
    ("home", "testimonials_section_visible"): {
        "label": "Отзывы — видимость",
        "text_ru": "1",
        "text_en": "1",
    },
    ("home", "testimonials.eyebrow"): {
        "label": "Отзывы — надзаголовок",
        "text_ru": "Отзывы",
        "text_en": "Testimonials",
    },
    ("home", "faq_section_visible"): {
        "label": "Вопросы — видимость",
        "text_ru": "1",
        "text_en": "1",
    },
    ("home", "faq.eyebrow"): {
        "label": "Вопросы — надзаголовок",
        "text_ru": "Вопросы",
        "text_en": "Questions",
    },
    ("home", "faq.title"): {
        "label": "Вопросы — заголовок",
        "text_ru": "Ответы",
        "text_en": "Answers",
    },
    ("home", "faq.title_accent"): {
        "label": "Вопросы — акцент",
        "text_ru": "перед брифингом",
        "text_en": "before the briefing",
    },
    ("home", "faq.cta"): {
        "label": "Вопросы — кнопка",
        "text_ru": "Задать вопрос",
        "text_en": "Ask a question",
    },
    ("home", "contacts_section_visible"): {
        "label": "Контакты — видимость",
        "text_ru": "1",
        "text_en": "1",
    },
    ("home", "contacts.eyebrow"): {
        "label": "Контакты — надзаголовок",
        "text_ru": "Контакты",
        "text_en": "Contacts",
    },
    ("home", "contacts.title"): {
        "label": "Контакты — заголовок",
        "text_ru": "Запросите профессиональную",
        "text_en": "Request a Professional",
    },
    ("home", "contacts.title_accent"): {
        "label": "Контакты — акцент",
        "text_ru": "консультацию",
        "text_en": "Consultation",
    },
    ("home", "contacts.lead"): {
        "label": "Контакты — текст",
        "text_ru": (
            "Оставьте заявку — наша команда свяжется с вами в течение 24 часов "
            "для планирования брифинга по проекту."
        ),
        "text_en": (
            "Leave a request — our team will contact you within 24 hours "
            "to schedule a project briefing."
        ),
    },
    ("home", "contacts.privacy_note"): {
        "label": "Контакты — примечание про конфиденциальность",
        "text_ru": "Все обращения остаются конфиденциальными.",
        "text_en": "All inquiries remain confidential.",
    },
    ("privacy", "title"): {
        "label": "Политика — заголовок",
        "text_ru": "Политика конфиденциальности",
        "text_en": "Privacy policy",
    },
    ("privacy", "body"): {
        "label": "Политика — текст",
        "text_ru": (
            "Настоящая политика описывает порядок обработки персональных данных, "
            "которые вы добровольно оставляете через форму заявки на сайте: имя, "
            "контакт и комментарий.\n\n"
            "Данные используются исключительно для ответа на обращение и не "
            "передаются третьим лицам, за исключением случаев, прямо предусмотренных "
            "законодательством.\n\n"
            "Вы можете запросить удаление своих данных, написав на адрес электронной "
            "почты, указанный в разделе контактов."
        ),
        "text_en": (
            "This policy describes how personal data you voluntarily submit "
            "through the request form is processed: name, contact details and comment.\n\n"
            "Data is used solely to reply to your inquiry and is not shared with "
            "third parties except where required by law.\n\n"
            "You may request deletion of your data by writing to the email address "
            "listed in the contacts section."
        ),
    },
    ("terms", "title"): {
        "label": "Условия — заголовок",
        "text_ru": "Условия использования",
        "text_en": "Terms of use",
    },
    ("terms", "body"): {
        "label": "Условия — текст",
        "text_ru": (
            "Используя сайт Maison Polina, вы подтверждаете, что ознакомились "
            "с настоящими условиями и принимаете их.\n\n"
            "Материалы сайта носят информационный характер и описывают услуги "
            "премиального бизнес-консьержа и lifestyle management. Заявки и "
            "переписка не создают договорных обязательств до отдельного "
            "письменного согласования сторон.\n\n"
            "Запрещается копировать контент, вводить в заблуждение относительно "
            "связи с брендом или использовать сайт способом, нарушающим закон "
            "либо права третьих лиц.\n\n"
            "Мы можем обновлять эти условия; актуальная редакция публикуется на "
            "этой странице. По вопросам обращайтесь через контакты на сайте."
        ),
        "text_en": (
            "By using the Maison Polina website, you confirm that you have read "
            "and accept these terms.\n\n"
            "Site materials are informational and describe premium executive "
            "concierge and lifestyle management services. Inquiries and "
            "correspondence do not create contractual obligations until the "
            "parties agree in writing.\n\n"
            "You may not copy content, misrepresent an affiliation with the brand, "
            "or use the site in any way that violates the law or third-party rights.\n\n"
            "We may update these terms; the current version is published on this "
            "page. For questions, use the contact channels on the site."
        ),
    },
}

BLOCK_DEFAULTS: dict[tuple[str, str], dict] = {
    **_PAGE_BLOCK_DEFAULTS,
    **CHROME_BLOCK_DEFAULTS,
}

BLOCK_CONTENT_TYPES: dict[tuple[str, str], str] = {
    (page, key): block_content_type(key) for page, key in BLOCK_DEFAULTS
}


def all_block_keys() -> list[tuple[str, str]]:
    return list(BLOCK_DEFAULTS.keys())


def get_block_field_label(page: str, key: str) -> str:
    defaults = BLOCK_DEFAULTS.get((page, key), {})
    label = defaults.get("label") or key
    # Admin UI: short name without section prefix ("Личность — возраст" → "Возраст")
    if " — " in label:
        short = label.split(" — ", 1)[1].strip()
        if short:
            return short[:1].upper() + short[1:]
    return label
