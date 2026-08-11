"""Default SiteBlock values. No model imports — safe at import time."""

from src.core.block_defaults_chrome import CHROME_BLOCK_DEFAULTS

# (page, key) -> dict with text_ru, text_en, label, is_visible
_PAGE_BLOCK_DEFAULTS: dict[tuple[str, str], dict] = {
    ("home", "hero_section_visible"): {
        "label": "Hero — видимість",
        "text_ru": "1",
        "text_en": "1",
        "is_visible": True,
    },
    ("home", "hero.title"): {
        "label": "Hero — ім'я",
        "text_ru": "MAISON POLINA",
        "text_en": "MAISON POLINA",
    },
    ("home", "hero.subtitle"): {
        "label": "Hero — підзаголовок",
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
        "label": "Hero — основна кнопка",
        "text_ru": "Оставить заявку",
        "text_en": "Send a request",
    },
    ("home", "hero.cta_secondary"): {
        "label": "Hero — друга кнопка",
        "text_ru": "Услуги и цены",
        "text_en": "Services and rates",
    },
    ("home", "hero.tagline"): {
        "label": "Hero — теглайн",
        "text_ru": "Independent · Private · Confidence",
        "text_en": "Independent · Private · Confidence",
    },
    ("home", "hero.media"): {
        "label": "Hero — фото/відео",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "about_section_visible"): {
        "label": "Про мене — видимість",
        "text_ru": "1",
        "text_en": "1",
        "is_visible": True,
    },
    ("home", "about.eyebrow"): {
        "label": "Про мене — надзаголовок",
        "text_ru": "Обо мне",
        "text_en": "About",
    },
    ("home", "about.title"): {
        "label": "Про мене — заголовок",
        "text_ru": "Восемь лет",
        "text_en": "Eight years",
    },
    ("home", "about.title_accent"): {
        "label": "Про мене — акцент у заголовку",
        "text_ru": "ярких впечатлений",
        "text_en": "of vivid impressions",
    },
    ("home", "about.body_1"): {
        "label": "Про мене — абзац 1",
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
        "label": "Про мене — абзац 2",
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
        "label": "Про мене — абзац 3",
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
        "label": "Про мене — цитата",
        "text_ru": "Хорошее общество не нуждается в объяснениях.",
        "text_en": "Good company needs no explanation.",
    },
    ("home", "about.stat_1_value"): {
        "label": "Про мене — цифра 1",
        "text_ru": "8",
        "text_en": "8",
    },
    ("home", "about.stat_1_label"): {
        "label": "Про мене — підпис 1",
        "text_ru": "лет практики",
        "text_en": "years of practice",
    },
    ("home", "about.stat_2_value"): {
        "label": "Про мене — цифра 2",
        "text_ru": "200+",
        "text_en": "200+",
    },
    ("home", "about.stat_2_label"): {
        "label": "Про мене — підпис 2",
        "text_ru": "встреч и приёмов",
        "text_en": "meetings and receptions",
    },
    ("home", "about.stat_3_value"): {
        "label": "Про мене — цифра 3",
        "text_ru": "6",
        "text_en": "6",
    },
    ("home", "about.stat_3_label"): {
        "label": "Про мене — підпис 3",
        "text_ru": "приглашений в месяц",
        "text_en": "invitations per month",
    },
    ("home", "about.cta"): {
        "label": "Про мене — кнопка",
        "text_ru": "Написать мне",
        "text_en": "Write to me",
    },
    ("home", "about.portrait"): {
        "label": "Про мене — портрет",
        "text_ru": "Полина — выступление на мероприятии",
        "text_en": "Polina — speaking at an event",
    },
    ("home", "personality_section_visible"): {
        "label": "Особистість — видимість",
        "text_ru": "1",
        "text_en": "1",
        "is_visible": True,
    },
    ("home", "personality.eyebrow"): {
        "label": "Особистість — надзаголовок",
        "text_ru": "Обо мне",
        "text_en": "About me",
    },
    ("home", "personality.title"): {
        "label": "Особистість — заголовок (світле слово)",
        "text_ru": "Дополнительная",
        "text_en": "Additional",
    },
    ("home", "personality.title_accent"): {
        "label": "Особистість — акцент у заголовку",
        "text_ru": "информация",
        "text_en": "information",
    },
    ("home", "personality.facts_title"): {
        "label": "Особистість — підзаголовок параметрів",
        "text_ru": "Внешность",
        "text_en": "Appearance",
    },
    ("home", "personality.age"): {
        "label": "Особистість — вік",
        "text_ru": "32",
        "text_en": "32",
    },
    ("home", "personality.eyes"): {
        "label": "Особистість — очі",
        "text_ru": "серые",
        "text_en": "gray",
    },
    ("home", "personality.hair"): {
        "label": "Особистість — волосся",
        "text_ru": "русые",
        "text_en": "light brown",
    },
    ("home", "personality.height"): {
        "label": "Особистість — зріст",
        "text_ru": "174",
        "text_en": "174",
    },
    ("home", "personality.weight"): {
        "label": "Особистість — вага",
        "text_ru": "59",
        "text_en": "59",
    },
    ("home", "personality.measurements"): {
        "label": "Особистість — параметри",
        "text_ru": "90-60-94",
        "text_en": "90-60-94",
    },
    ("home", "personality.shoes"): {
        "label": "Особистість — взуття",
        "text_ru": "39",
        "text_en": "39",
    },
    ("home", "personality.clothing"): {
        "label": "Особистість — одяг",
        "text_ru": "38",
        "text_en": "38",
    },
    ("home", "personality.zodiac"): {
        "label": "Особистість — зодіак",
        "text_ru": "Водолей",
        "text_en": "Aquarius",
    },
    ("home", "personality.tattoo"): {
        "label": "Особистість — тату",
        "text_ru": "нет",
        "text_en": "none",
    },
    ("home", "personality.piercing"): {
        "label": "Особистість — пірсинг",
        "text_ru": "нет",
        "text_en": "none",
    },
    ("home", "personality.flowers"): {
        "label": "Особистість — квіти",
        "text_ru": "Орхидеи, Лилии",
        "text_en": "Orchids, lilies",
    },
    ("home", "personality.cuisine"): {
        "label": "Особистість — кухня",
        "text_ru": "Итальянская",
        "text_en": "Italian",
    },
    ("home", "personality.alcohol"): {
        "label": "Особистість — алкоголь",
        "text_ru": "уточнять",
        "text_en": "upon request",
    },
    ("home", "personality.smoking"): {
        "label": "Особистість — куріння",
        "text_ru": "Не курю",
        "text_en": "Non-smoker",
    },
    ("home", "personality.extra_title"): {
        "label": "Особистість — підзаголовок додаткового (не використовується)",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "personality.extra_1"): {
        "label": "Особистість — пункт 1",
        "text_ru": "мастер спорта",
        "text_en": "Master of Sport",
    },
    ("home", "personality.extra_2"): {
        "label": "Особистість — пункт 2",
        "text_ru": "профессиональная модель",
        "text_en": "professional model",
    },
    ("home", "personality.extra_3"): {
        "label": "Особистість — пункт 3",
        "text_ru": "фешн-журналист",
        "text_en": "fashion journalist",
    },
    ("home", "personality.languages"): {
        "label": "Особистість — мови",
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
        "label": "Особистість — повага до культур",
        "text_ru": "Уважаю любую культуру, религию, традиции.",
        "text_en": "I respect every culture, religion, and tradition.",
    },
    ("home", "personality.education"): {
        "label": "Особистість — освіта",
        "text_ru": "Два высших образования.",
        "text_en": "Two higher-education degrees.",
    },
    ("home", "personality.travel"): {
        "label": "Особистість — подорожі",
        "text_ru": "Посетила 20+ стран.",
        "text_en": "Visited 20+ countries.",
    },
    ("home", "personality.portrait"): {
        "label": "Особистість — фото",
        "text_ru": "",
        "text_en": "",
    },
    ("home", "gallery_section_visible"): {
        "label": "Галерея — видимість",
        "text_ru": "1",
        "text_en": "1",
        "is_visible": True,
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
        "label": "Формати — видимість",
        "text_ru": "1",
        "text_en": "1",
        "is_visible": True,
    },
    ("home", "formats.eyebrow"): {
        "label": "Формати — надзаголовок",
        "text_ru": "Услуги и цены",
        "text_en": "Services and rates",
    },
    ("home", "formats.title"): {
        "label": "Формати — заголовок",
        "text_ru": "Три формата",
        "text_en": "Three formats",
    },
    ("home", "formats.title_accent"): {
        "label": "Формати — акцент",
        "text_ru": "сопровождения",
        "text_en": "of companionship",
    },
    ("home", "formats.note"): {
        "label": "Формати — примітка",
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
        "label": "Відгуки — видимість",
        "text_ru": "1",
        "text_en": "1",
        "is_visible": True,
    },
    ("home", "testimonials.eyebrow"): {
        "label": "Відгуки — надзаголовок",
        "text_ru": "Отзывы",
        "text_en": "Testimonials",
    },
    ("home", "faq_section_visible"): {
        "label": "Питання — видимість",
        "text_ru": "1",
        "text_en": "1",
        "is_visible": True,
    },
    ("home", "faq.eyebrow"): {
        "label": "Питання — надзаголовок",
        "text_ru": "Вопросы",
        "text_en": "Questions",
    },
    ("home", "faq.title"): {
        "label": "Питання — заголовок",
        "text_ru": "Ответы",
        "text_en": "Answers",
    },
    ("home", "faq.title_accent"): {
        "label": "Питання — акцент",
        "text_ru": "до разговора",
        "text_en": "before we speak",
    },
    ("home", "faq.cta"): {
        "label": "Питання — кнопка",
        "text_ru": "Задать вопрос",
        "text_en": "Ask a question",
    },
    ("home", "contacts_section_visible"): {
        "label": "Контакти — видимість",
        "text_ru": "1",
        "text_en": "1",
        "is_visible": True,
    },
    ("home", "contacts.eyebrow"): {
        "label": "Контакти — надзаголовок",
        "text_ru": "Контакты",
        "text_en": "Contacts",
    },
    ("home", "contacts.title"): {
        "label": "Контакти — заголовок",
        "text_ru": "Начнём с разговора",
        "text_en": "Let's start with a conversation",
    },
    ("home", "contacts.title_accent"): {
        "label": "Контакти — акцент",
        "text_ru": "без обязательств",
        "text_en": "without obligation",
    },
    ("home", "contacts.lead"): {
        "label": "Контакти — текст",
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
        "label": "Контакти — примітка про конфіденційність",
        "text_ru": "Все обращения остаются конфиденциальными.",
        "text_en": "All inquiries remain private.",
    },
    ("privacy", "title"): {
        "label": "Політика — заголовок",
        "text_ru": "Политика конфиденциальности",
        "text_en": "Privacy policy",
    },
    ("privacy", "body"): {
        "label": "Політика — текст",
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


def all_block_keys() -> list[tuple[str, str]]:
    return list(BLOCK_DEFAULTS.keys())
