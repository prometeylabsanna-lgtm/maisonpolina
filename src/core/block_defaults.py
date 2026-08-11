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


def is_visibility_key(key: str) -> bool:
    return key.endswith("_section_visible") or key.endswith("_visible")


def block_content_type(key: str) -> str:
    return "image" if key in IMAGE_KEYS else "text"


# (page, key) -> dict with text_ru, text_en, label
_PAGE_BLOCK_DEFAULTS: dict[tuple[str, str], dict] = {
    ("home", "hero_section_visible"): {
        "label": "Hero — видимость",
        "text_ru": "1",
        "text_en": "1",
    },
    ("home", "hero.title"): {
        "label": "Hero — имя",
        "text_ru": "MAISON POLINA",
        "text_en": "MAISON POLINA",
    },
    ("home", "hero.subtitle"): {
        "label": "Hero — подзаголовок",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "hero.lead"): {
        "label": "Hero — текст",
        "text_ru": (
            "Ценю живой разговор, эстетику и подлинный контакт. "
            "Ужины, приёмы, деловые поездки — каждая встреча продумана так, "
            "чтобы стать поводом вернуться."
        ),
        "text_en": (
            "I value real conversation, aesthetics and genuine contact. "
            "Dinners, receptions, business trips — each meeting is arranged "
            "to become a reason to return."
        ),
    },
    ("home", "hero.cta_primary"): {
        "label": "Hero — главная кнопка",
        "text_ru": "Оставить заявку",
        "text_en": "Send a request",
    },
    ("home", "hero.cta_secondary"): {
        "label": "Hero — вторая кнопка",
        "text_ru": "Услуги и цены",
        "text_en": "Services and rates",
    },
    ("home", "hero.tagline"): {
        "label": "Hero — слоган",
        "text_ru": "Independent · Private · Confidence",
        "text_en": "Independent · Private · Confidence",
    },
    ("home", "hero.media"): {
        "label": "Hero — фото",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "about_section_visible"): {
        "label": "Обо мне — видимость",
        "text_ru": "1",
        "text_en": "1",
    },
    ("home", "about.eyebrow"): {
        "label": "Обо мне — надзаголовок",
        "text_ru": "Обо мне",
        "text_en": "About",
    },
    ("home", "about.title"): {
        "label": "Обо мне — заголовок",
        "text_ru": "Восемь лет",
        "text_en": "Eight years",
    },
    ("home", "about.title_accent"): {
        "label": "Обо мне — акцент в заголовке",
        "text_ru": "ярких впечатлений",
        "text_en": "of vivid impressions",
    },
    ("home", "about.body_1"): {
        "label": "Обо мне — абзац 1",
        "text_ru": (
            "За восемь лет я сопровождала дипломатов, промышленников "
            "и людей творческих профессий — на переговорах, приёмах и в долгих "
            "поездках. Каждый раз главным был не повод, а то, каким запомнится вечер."
        ),
        "text_en": (
            "For eight years I have accompanied diplomats, industrialists "
            "and people of creative professions — at negotiations, receptions "
            "and on long journeys. What mattered was never the occasion, "
            "but how the evening would be remembered."
        ),
    },
    ("home", "about.body_2"): {
        "label": "Обо мне — абзац 2",
        "text_ru": (
            "Я легко подстраиваюсь под шаблон встречи. Слушаю, что нужно именно "
            "в этот вечер: лёгкий разговор, тишина рядом или уверенное присутствие "
            "за столом переговоров."
        ),
        "text_en": (
            "I easily adapt to the meeting. I listen to what this evening needs: "
            "light conversation, quiet presence, or confident company "
            "at the negotiating table."
        ),
    },
    ("home", "about.body_3"): {
        "label": "Обо мне — абзац 3",
        "text_ru": (
            "Приглашений в месяц немного — ровно столько, чтобы каждой встрече "
            "хватало внимания. Имена гостей остаются между нами."
        ),
        "text_en": (
            "There are few invitations each month — just enough for every meeting "
            "to receive full attention. Guest names stay between us."
        ),
    },
    ("home", "about.quote"): {
        "label": "Обо мне — цитата",
        "text_ru": "Хорошее общество не нуждается в объяснениях.",
        "text_en": "Good company needs no explanation.",
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
        "text_ru": "встреч и приёмов",
        "text_en": "meetings and receptions",
    },
    ("home", "about.stat_3_value"): {
        "label": "Обо мне — цифра 3",
        "text_ru": "6",
        "text_en": "6",
    },
    ("home", "about.stat_3_label"): {
        "label": "Обо мне — подпись 3",
        "text_ru": "приглашений в месяц",
        "text_en": "invitations per month",
    },
    ("home", "about.cta"): {
        "label": "Обо мне — кнопка",
        "text_ru": "Написать мне",
        "text_en": "Write to me",
    },
    ("home", "about.portrait"): {
        "label": "Обо мне — портрет",
        "text_ru": "Полина — выступление на мероприятии",
        "text_en": "Polina — speaking at an event",
    },
    ("home", "personality_section_visible"): {
        "label": "Личность — видимость",
        "text_ru": "1",
        "text_en": "1",
    },
    ("home", "personality.eyebrow"): {
        "label": "Личность — надзаголовок",
        "text_ru": "Обо мне",
        "text_en": "About me",
    },
    ("home", "personality.title"): {
        "label": "Личность — заголовок (светлое слово)",
        "text_ru": "Дополнительная",
        "text_en": "Additional",
    },
    ("home", "personality.title_accent"): {
        "label": "Личность — акцент в заголовке",
        "text_ru": "информация",
        "text_en": "information",
    },
    ("home", "personality.facts_title"): {
        "label": "Личность — подзаголовок параметров",
        "text_ru": "Внешность",
        "text_en": "Appearance",
    },
    ("home", "personality.age"): {
        "label": "Личность — возраст",
        "text_ru": "32",
        "text_en": "32",
    },
    ("home", "personality.eyes"): {
        "label": "Личность — глаза",
        "text_ru": "серые",
        "text_en": "gray",
    },
    ("home", "personality.hair"): {
        "label": "Личность — волосы",
        "text_ru": "русые",
        "text_en": "light brown",
    },
    ("home", "personality.height"): {
        "label": "Личность — рост",
        "text_ru": "174",
        "text_en": "174",
    },
    ("home", "personality.weight"): {
        "label": "Личность — вес",
        "text_ru": "59",
        "text_en": "59",
    },
    ("home", "personality.measurements"): {
        "label": "Личность — параметры",
        "text_ru": "90-60-94",
        "text_en": "90-60-94",
    },
    ("home", "personality.shoes"): {
        "label": "Личность — обувь",
        "text_ru": "39",
        "text_en": "39",
    },
    ("home", "personality.clothing"): {
        "label": "Личность — одежда",
        "text_ru": "38",
        "text_en": "38",
    },
    ("home", "personality.zodiac"): {
        "label": "Личность — зодиак",
        "text_ru": "Водолей",
        "text_en": "Aquarius",
    },
    ("home", "personality.tattoo"): {
        "label": "Личность — тату",
        "text_ru": "нет",
        "text_en": "none",
    },
    ("home", "personality.piercing"): {
        "label": "Личность — пирсинг",
        "text_ru": "нет",
        "text_en": "none",
    },
    ("home", "personality.flowers"): {
        "label": "Личность — цветы",
        "text_ru": "Орхидеи, Лилии",
        "text_en": "Orchids, lilies",
    },
    ("home", "personality.cuisine"): {
        "label": "Личность — кухня",
        "text_ru": "Итальянская",
        "text_en": "Italian",
    },
    ("home", "personality.alcohol"): {
        "label": "Личность — алкоголь",
        "text_ru": "уточнять",
        "text_en": "upon request",
    },
    ("home", "personality.smoking"): {
        "label": "Личность — курение",
        "text_ru": "Не курю",
        "text_en": "Non-smoker",
    },
    ("home", "personality.extra_title"): {
        "label": "Личность — подзаголовок дополнительного (не используется)",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "personality.extra_1"): {
        "label": "Личность — пункт 1",
        "text_ru": "мастер спорта",
        "text_en": "Master of Sport",
    },
    ("home", "personality.extra_2"): {
        "label": "Личность — пункт 2",
        "text_ru": "профессиональная модель",
        "text_en": "professional model",
    },
    ("home", "personality.extra_3"): {
        "label": "Личность — пункт 3",
        "text_ru": "фешн-журналист",
        "text_en": "fashion journalist",
    },
    ("home", "personality.languages"): {
        "label": "Личность — мови",
        "text_ru": (
            "Языки: английский, русский, украинский. Знание делового этикета, "
            "культурные различия стран."
        ),
        "text_en": (
            "Languages: English, Russian, Ukrainian. Business etiquette "
            "and cultural differences across countries."
        ),
    },
    ("home", "personality.respect"): {
        "label": "Личность — повес до культур",
        "text_ru": "Уважаю любую культуру, религию, традиции.",
        "text_en": "I respect every culture, religion, and tradition.",
    },
    ("home", "personality.education"): {
        "label": "Личность — образование",
        "text_ru": "Два высших образования.",
        "text_en": "Two higher-education degrees.",
    },
    ("home", "personality.travel"): {
        "label": "Личность — путешествия",
        "text_ru": "Посетила 20+ стран.",
        "text_en": "Visited 20+ countries.",
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
        "text_ru": "Кадры разных",
        "text_en": "Frames from different",
    },
    ("home", "gallery.title_accent"): {
        "label": "Галерея — акцент",
        "text_ru": "вечеров",
        "text_en": "evenings",
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
        "text_en": "Three formats",
    },
    ("home", "formats.title_accent"): {
        "label": "Форматы — акцент",
        "text_ru": "сопровождения",
        "text_en": "of companionship",
    },
    ("home", "formats.note"): {
        "label": "Форматы — примечание",
        "text_ru": (
            "Стоимость поездок за пределы города и особых форматов обсуждается отдельно. "
            "Половина суммы вносится при подтверждении даты, остаток — по завершении встречи."
        ),
        "text_en": (
            "Travel outside the city and special formats are discussed separately. "
            "Half the fee is paid when the date is confirmed, the rest after the meeting."
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
        "text_ru": "до разговора",
        "text_en": "before we speak",
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
        "text_ru": "Начнём с разговора",
        "text_en": "Let's start with a conversation",
    },
    ("home", "contacts.title_accent"): {
        "label": "Контакты — акцент",
        "text_ru": "без обязательств",
        "text_en": "without obligation",
    },
    ("home", "contacts.lead"): {
        "label": "Контакты — текст",
        "text_ru": (
            "Оставьте заявку — я отвечу лично в течение суток "
            "и предложу время для встречи."
        ),
        "text_en": (
            "Leave a request — I will reply personally within a day "
            "and suggest a time to meet."
        ),
    },
    ("home", "contacts.privacy_note"): {
        "label": "Контакты — примечание про конфиденциальность",
        "text_ru": "Все обращения остаются конфиденциальными.",
        "text_en": "All inquiries remain private.",
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
