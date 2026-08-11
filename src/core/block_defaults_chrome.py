"""UI chrome / header / footer / chat / errors SiteBlock defaults."""

CHROME_BLOCK_DEFAULTS: dict[tuple[str, str], dict] = {
    ("site", "nav.about"): {
        "label": "Меню — Обо мне",
        "text_ru": "Обо мне",
        "text_en": "About",
    },
    ("site", "nav.gallery"): {
        "label": "Меню — Галерея",
        "text_ru": "Галерея",
        "text_en": "Gallery",
    },
    ("site", "nav.services"): {
        "label": "Меню — Услуги",
        "text_ru": "Услуги",
        "text_en": "Services",
    },
    ("site", "nav.reviews"): {
        "label": "Меню — Отзывы",
        "text_ru": "Отзывы",
        "text_en": "Reviews",
    },
    ("site", "nav.faq"): {
        "label": "Меню — Вопросы",
        "text_ru": "Вопросы",
        "text_en": "FAQ",
    },
    ("site", "nav.contact"): {
        "label": "Меню — Контакты",
        "text_ru": "Контакты",
        "text_en": "Contacts",
    },
    ("site", "header.nav_aria"): {
        "label": "Шапка — aria навигации",
        "text_ru": "Основная навигация",
        "text_en": "Main navigation",
    },
    ("site", "header.menu_aria"): {
        "label": "Шапка — подпись меню (для скринридеров)",
        "text_ru": "Меню",
        "text_en": "Menu",
    },
    ("site", "header.cta"): {
        "label": "Шапка — кнопка заявки",
        "text_ru": "Заявка",
        "text_en": "Request",
    },
    ("site", "header.brand_line_1"): {
        "label": "Шапка — бренд — строка 1",
        "text_ru": "MAISON",
        "text_en": "MAISON",
    },
    ("site", "header.brand_line_2"): {
        "label": "Шапка — бренд — строка 2",
        "text_ru": "POLINA",
        "text_en": "POLINA",
    },
    ("site", "header.brand_aria"): {
        "label": "Шапка — подпись бренда (для скринридеров)",
        "text_ru": "Maison Polina",
        "text_en": "Maison Polina",
    },
    ("site", "footer.brand"): {
        "label": "Подвал — бренд",
        "text_ru": "MAISON POLINA",
        "text_en": "MAISON POLINA",
    },
    ("site", "footer.location_label"): {
        "label": "Подвал — локация",
        "text_ru": "Локация",
        "text_en": "Location",
    },
    ("site", "footer.contact_label"): {
        "label": "Подвал — связь",
        "text_ru": "Связаться",
        "text_en": "Contact",
    },
    ("site", "footer.menu_label"): {
        "label": "Подвал — меню",
        "text_ru": "Меню",
        "text_en": "Menu",
    },
    ("site", "footer.menu_aria"): {
        "label": "Подвал — подпись меню (для скринридеров)",
        "text_ru": "Меню футера",
        "text_en": "Footer menu",
    },
    ("site", "footer.telegram_title"): {
        "label": "Подвал — Telegram заголовок",
        "text_ru": "Telegram",
        "text_en": "Telegram",
    },
    ("site", "footer.telegram_sub"): {
        "label": "Подвал — Telegram подпись",
        "text_ru": "Написать в чат-бот",
        "text_en": "Message the chat bot",
    },
    ("site", "footer.menu_more"): {
        "label": "Подвал — показать ещё",
        "text_ru": "Показать ещё",
        "text_en": "Show more",
    },
    ("site", "footer.privacy_1"): {
        "label": "Подвал — политика 1",
        "text_ru": "Политика",
        "text_en": "Privacy",
    },
    ("site", "footer.privacy_2"): {
        "label": "Подвал — политика 2",
        "text_ru": "конфиденциальности",
        "text_en": "policy",
    },
    ("site", "dock.aria"): {
        "label": "Dock — aria",
        "text_ru": "Мобильная панель",
        "text_en": "Mobile dock",
    },
    ("site", "dock.home"): {
        "label": "Dock — главная",
        "text_ru": "Главная",
        "text_en": "Home",
    },
    ("site", "dock.gallery"): {
        "label": "Dock — галерея",
        "text_ru": "Галерея",
        "text_en": "Gallery",
    },
    ("site", "dock.contacts"): {
        "label": "Dock — контакты",
        "text_ru": "Контакты",
        "text_en": "Contacts",
    },
    ("site", "mobile.nav_aria"): {
        "label": "Мобильное меню — aria",
        "text_ru": "Мобильная навигация",
        "text_en": "Mobile navigation",
    },
    ("site", "mobile.close"): {
        "label": "Мобильное меню — закрыть",
        "text_ru": "Закрыть",
        "text_en": "Close",
    },
    ("site", "lang.aria"): {
        "label": "Переключатель языка — aria",
        "text_ru": "Язык",
        "text_en": "Language",
    },
    ("site", "ui.close"): {
        "label": "UI — закрыть",
        "text_ru": "Закрыть",
        "text_en": "Close",
    },
    ("site", "form.name"): {
        "label": "Форма — имя",
        "text_ru": "Имя",
        "text_en": "Name",
    },
    ("site", "form.contact"): {
        "label": "Форма — контакт",
        "text_ru": "Телефон или e-mail",
        "text_en": "Phone or e-mail",
    },
    ("site", "form.message"): {
        "label": "Форма — коментар",
        "text_ru": "Комментарий",
        "text_en": "Comment",
    },
    ("site", "form.consent_prefix"): {
        "label": "Форма — согласие (начало фразы)",
        "text_ru": "Согласен на обработку персональных данных и принимаю",
        "text_en": "I agree to personal data processing and accept the",
    },
    ("site", "form.privacy_link"): {
        "label": "Форма — ссылка на политику",
        "text_ru": "политику конфиденциальности",
        "text_en": "privacy policy",
    },
    ("site", "form.submit"): {
        "label": "Форма — отправить",
        "text_ru": "Отправить",
        "text_en": "Send",
    },
    ("site", "form.service_hint"): {
        "label": "Форма — обрана послуга",
        "text_ru": "Выбранная услуга:",
        "text_en": "Selected service:",
    },
    ("site", "form.honeypot"): {
        "label": "Форма — скрытое поле (антиспам)",
        "text_ru": "Сайт",
        "text_en": "Website",
    },
    ("site", "lead.modal_title"): {
        "label": "Заявка — заголовок модалки",
        "text_ru": "Оставить заявку",
        "text_en": "Send a request",
    },
    ("site", "lead.success_title"): {
        "label": "Заявка — успех — заголовок",
        "text_ru": "Благодарю вас",
        "text_en": "Thank you",
    },
    ("site", "lead.success_text"): {
        "label": "Заявка — успех — текст",
        "text_ru": "Я получу заявку и отвечу лично в течение суток.",
        "text_en": "I will receive your request and reply personally within a day.",
    },
    ("site", "review.modal_title"): {
        "label": "Отзыв — заголовок модалки",
        "text_ru": "Оставить отзыв",
        "text_en": "Leave a review",
    },
    ("site", "review.form_name"): {
        "label": "Отзыв — имя",
        "text_ru": "Имя",
        "text_en": "Name",
    },
    ("site", "review.form_rating"): {
        "label": "Отзыв — оценка",
        "text_ru": "Оценка",
        "text_en": "Rating",
    },
    ("site", "review.form_text"): {
        "label": "Отзыв — текст",
        "text_ru": "Отзыв",
        "text_en": "Review",
    },
    ("site", "review.submit"): {
        "label": "Отзыв — отправить",
        "text_ru": "Отправить",
        "text_en": "Send",
    },
    ("site", "review.success_title"): {
        "label": "Отзыв — успех — заголовок",
        "text_ru": "Благодарю вас",
        "text_en": "Thank you",
    },
    ("site", "review.success_text"): {
        "label": "Отзыв — успех — текст",
        "text_ru": "Отзыв отправлен на модерацию и появится после проверки.",
        "text_en": "Your review was submitted for moderation and will appear after review.",
    },
    ("site", "review.cta"): {
        "label": "Отзывы — кнопка залишити",
        "text_ru": "Оставить отзыв",
        "text_en": "Leave a review",
    },
    ("site", "formats.featured_badge"): {
        "label": "Форматы — значок",
        "text_ru": "Чаще всего",
        "text_en": "Most chosen",
    },
    ("site", "formats.includes"): {
        "label": "Форматы — що входить",
        "text_ru": "Что входит",
        "text_en": "What's included",
    },
    ("site", "formats.order_cta"): {
        "label": "Форматы — заказать",
        "text_ru": "Заказать",
        "text_en": "Book",
    },
    ("site", "contacts.telegram_title"): {
        "label": "Контакты — Telegram заголовок",
        "text_ru": "Telegram",
        "text_en": "Telegram",
    },
    ("site", "contacts.telegram_sub"): {
        "label": "Контакты — Telegram подпись",
        "text_ru": "Написать в чат-бот",
        "text_en": "Message the chat bot",
    },
    ("site", "contacts.form_label"): {
        "label": "Контакты — подпись формы",
        "text_ru": "Заявка",
        "text_en": "Request",
    },
    ("site", "contacts.bg"): {
        "label": "Контакты — фон",
        "text_ru": "",
        "text_en": "",
    },
    ("site", "gallery.open"): {
        "label": "Галерея — открыть",
        "text_ru": "Открыть фото",
        "text_en": "Open photo",
    },
    ("site", "gallery.prev"): {
        "label": "Галерея — назад",
        "text_ru": "Предыдущие фото",
        "text_en": "Previous photos",
    },
    ("site", "gallery.next"): {
        "label": "Галерея — вперед",
        "text_ru": "Следующие фото",
        "text_en": "Next photos",
    },
    ("site", "lightbox.close"): {
        "label": "Lightbox — закрыть",
        "text_ru": "Закрыть",
        "text_en": "Close",
    },
    ("site", "lightbox.prev"): {
        "label": "Lightbox — назад",
        "text_ru": "Предыдущее",
        "text_en": "Previous",
    },
    ("site", "lightbox.next"): {
        "label": "Lightbox — вперед",
        "text_ru": "Следующее",
        "text_en": "Next",
    },
    ("site", "carousel.prev"): {
        "label": "Карусель — назад",
        "text_ru": "Предыдущий отзыв",
        "text_en": "Previous review",
    },
    ("site", "carousel.next"): {
        "label": "Карусель — вперед",
        "text_ru": "Следующий отзыв",
        "text_en": "Next review",
    },
    ("site", "personality.label_age"): {
        "label": "Личность — подпись «возраст»",
        "text_ru": "Возраст",
        "text_en": "Age",
    },
    ("site", "personality.label_eyes"): {
        "label": "Личность — подпись «глаза»",
        "text_ru": "Глаза",
        "text_en": "Eyes",
    },
    ("site", "personality.label_hair"): {
        "label": "Личность — подпись «волосы»",
        "text_ru": "Волосы",
        "text_en": "Hair",
    },
    ("site", "personality.label_height"): {
        "label": "Личность — подпись «рост»",
        "text_ru": "Рост",
        "text_en": "Height",
    },
    ("site", "personality.label_weight"): {
        "label": "Личность — подпись «вес»",
        "text_ru": "Вес",
        "text_en": "Weight",
    },
    ("site", "personality.label_measurements"): {
        "label": "Личность — подпись «параметры»",
        "text_ru": "Параметры",
        "text_en": "Measurements",
    },
    ("site", "personality.label_shoes"): {
        "label": "Личность — подпись «обувь»",
        "text_ru": "Обувь",
        "text_en": "Shoes",
    },
    ("site", "personality.label_clothing"): {
        "label": "Личность — подпись «одежда»",
        "text_ru": "Размер одежды",
        "text_en": "Clothing size",
    },
    ("site", "personality.label_zodiac"): {
        "label": "Личность — подпись «зодиак»",
        "text_ru": "Зодиак",
        "text_en": "Zodiac",
    },
    ("site", "personality.label_tattoo"): {
        "label": "Личность — подпись «тату»",
        "text_ru": "Тату",
        "text_en": "Tattoo",
    },
    ("site", "personality.label_piercing"): {
        "label": "Личность — подпись «пирсинг»",
        "text_ru": "Пирсинг",
        "text_en": "Piercing",
    },
    ("site", "personality.label_flowers"): {
        "label": "Личность — подпись «цветы»",
        "text_ru": "Цветы",
        "text_en": "Flowers",
    },
    ("site", "personality.label_cuisine"): {
        "label": "Личность — подпись «кухня»",
        "text_ru": "Кухня",
        "text_en": "Cuisine",
    },
    ("site", "personality.label_alcohol"): {
        "label": "Личность — подпись «алкоголь»",
        "text_ru": "Алкоголь",
        "text_en": "Alcohol",
    },
    ("site", "personality.label_smoking"): {
        "label": "Личность — подпись «курение»",
        "text_ru": "Курение",
        "text_en": "Smoking",
    },
    ("site", "personality.portrait_alt"): {
        "label": "Личность — alt портрета",
        "text_ru": "Портрет",
        "text_en": "Portrait",
    },
    ("site", "chat.title"): {
        "label": "Чат — заголовок",
        "text_ru": "Сообщение",
        "text_en": "Message",
    },
    ("site", "chat.subtitle"): {
        "label": "Чат — подзаголовок",
        "text_ru": "Приватный диалог",
        "text_en": "Private dialogue",
    },
    ("site", "chat.open"): {
        "label": "Чат — открыть",
        "text_ru": "Открыть чат",
        "text_en": "Open chat",
    },
    ("site", "chat.close"): {
        "label": "Чат — закрыть",
        "text_ru": "Закрыть чат",
        "text_en": "Close chat",
    },
    ("site", "chat.panel_aria"): {
        "label": "Чат — подпись панели (для скринридеров)",
        "text_ru": "Чат",
        "text_en": "Chat",
    },
    ("site", "chat.input_label"): {
        "label": "Чат — label поля",
        "text_ru": "Ваше сообщение",
        "text_en": "Your message",
    },
    ("site", "chat.placeholder"): {
        "label": "Чат — placeholder",
        "text_ru": "Введите сообщение…",
        "text_en": "Type a message…",
    },
    ("site", "chat.send"): {
        "label": "Чат — отправить",
        "text_ru": "Отправить",
        "text_en": "Send",
    },
    ("site", "chat.empty"): {
        "label": "Чат — порожньо",
        "text_ru": "Напишите сообщение — ответим в ближайшее время.",
        "text_en": "Write a message — we will reply shortly.",
    },
    ("site", "chat.error_rate"): {
        "label": "Чат — ошибка лимита",
        "text_ru": "Слишком много сообщений. Попробуйте позже.",
        "text_en": "Too many messages. Please try later.",
    },
    ("site", "chat.error_session"): {
        "label": "Чат — ошибка сессии",
        "text_ru": "Сессия недоступна. Обновите страницу.",
        "text_en": "Session unavailable. Refresh the page.",
    },
    ("site", "chat.error_send"): {
        "label": "Чат — ошибка отправки",
        "text_ru": "Не удалось отправить сообщение.",
        "text_en": "Could not send the message.",
    },
    ("site", "error.404_text"): {
        "label": "404 — текст",
        "text_ru": "Страница не найдена. Вернитесь на главную.",
        "text_en": "Page not found. Return to the home page.",
    },
    ("site", "error.404_cta"): {
        "label": "404 — кнопка",
        "text_ru": "На главную",
        "text_en": "Home",
    },
    ("site", "error.500_text"): {
        "label": "500 — текст",
        "text_ru": "Временный сбой. Попробуйте обновить страницу позже.",
        "text_en": "Temporary issue. Please try again later.",
    },
    ("site", "error.500_cta"): {
        "label": "500 — кнопка",
        "text_ru": "На главную",
        "text_en": "Home",
    },
}
