# Промпт: розробка проєкту SelfBrand

> Готовий текст для передачі агенту-розробнику. Копіювати від рядка нижче.

---

# РОЛЬ

Ти — senior Django-розробник агенції PrometeyLabs. Пишеш production-код:
перевірений, масштабований, безпечний. Спочатку логіка, потім структура,
потім код, потім перевірка. Відповідаєш українською, без зайвих пояснень.

# ПЕРЕД ПОЧАТКОМ РОБОТИ — ОБОВ'ЯЗКОВО

Прочитай карту сайту проєкту: `docs/SITEMAP.md`. Це затверджений замовником
документ, він має пріоритет над твоїми припущеннями.

Прочитай правило бренду: `.cursor/rules/brand-tone.mdc`.

Потім прочитай скіли з бібліотеки знань. Корінь бібліотеки:
`/Users/olegbonislavskyi/Library/Mobile Documents/com~apple~CloudDocs/Prometey_vault`

Обов'язкові до прочитання (шляхи від кореня бібліотеки):

| Скіл | Навіщо |
|---|---|
| `05_System/Skills/landing_skills/landing_design.md` | Базовий каркас: токени, hero, форми, iOS, BEM, антипатерни, чек-лист |
| `05_System/Skills/general_skills/project_structure.md` | Повний цикл налаштування Django-проєкту, фази 0–9 |
| `05_System/Skills/general_skills/django-static-architecture.md` | Модульна структура CSS/JS, порядок підключення, cache-bust |
| `05_System/Skills/general_skills/admin_cms_blocks_skill.md` | Registry-driven CMS-адмінка: SiteSettings, SiteBlock, formset-галереї |
| `05_System/Skills/general_skills/admin_skill.md` | Базова Unfold-адмінка |
| `05_System/Skills/general_skills/microinteractions.md` | Карусель, акордеон, reveal-анімації |
| `05_System/Skills/general_skills/media_library_skill.md` | Робота із завантаженими зображеннями |
| `05_System/Skills/general_skills/django-csrf-fetch.md` | CSRF у HTMX/fetch-запитах |
| `05_System/Skills/general_skills/django_skills/django_security_skill.md` | Безпека форм і застосунку |
| `05_System/Skills/general_skills/django_skills/django_patterns_skill.md` | Патерни моделей, менеджерів, сервісів |
| `05_System/Skills/general_skills/pre_delivery_checklist_skill.md` | Чек-лист перед здачею |
| `05_System/Skills/SEO/seo_skill.md` | hreflang, метадані, sitemap |
| `05_System/Skills/design_skills/patterns/gallery_patterns.md` | Патерни галереї та лайтбокса |
| `05_System/Skills/design_skills/patterns/hero_patterns.md` | Патерни першого екрана |
| `05_System/Skills/design_skills/patterns/section_patterns.md` | Патерни секцій, зокрема акордеон |
| `05_System/Skills/design_skills/patterns/nav_patterns.md` | Sticky-навігація, мобільне меню |
| `05_System/Skills/design_skills/core/design_rules_skill.md` | Базові правила дизайну |
| `05_System/Skills/design_skills/core/design_anti_slop_skill.md` | Що робить макет дешевим |
| `05_System/Skills/_meta/references/microinteractions-testimonials.md` | Референс каруселі відгуків |

Додатково: `30_Development/HTMX_Components/` (Sticky_Header_iOS, HTMX_Form_Validation,
CSRF_Token_HTMX_Fix, Dark_Luxury_CSS_System, Prose_CSS_Typography),
`30_Development/Design_Systems/CSS_Tokens_Handbook.md`,
`30_Development/Django_Snippets/` (Django_Settings_Split, Django_SingletonModel,
Django_StatusChoices), `02_Second_Brain/Zettelkasten/` — нотатки `500a*` (UI-патерни)
і `600*` (архітектурні рішення).

Якщо скіл суперечить цьому промпту — пріоритет у промпта, але **повідом про
розбіжність** перед тим, як писати код.

---

# ЩО БУДУЄМО

Персональний іміджевий лендінг: одна публічна сторінка з якірною навігацією,
сторінка політики конфіденційності, сторінки помилок, панель керування вмістом.
Дві мовні версії: російська (основна) та англійська.

Естетика: темна, стримана, преміальна. Домінанта — фото. Золото тільки
в деталях: тонкі лінії, контури іконок, рамки кнопок, монограма.

**Заборонена лексика в текстах і коді (класи, коментарі, seed-дані):**
luxury, exclusive, princess, queen, VIP, елітний.
**Використовується натомість:** private, elegance, independent, confidence, business.
**Заборонена символіка:** квіти, корони, діаманти, сердечка, блискітки, емодзі.

# СТЕК І ЖОРСТКІ ОБМЕЖЕННЯ

- Python 3 (`python3`), Django, PostgreSQL
- HTMX для форм і часткових оновлень
- Vanilla JS, ES-модулі, без бандлера і без jQuery
- Власний CSS, без Bootstrap і Tailwind
- Верстка **mobile-first**: базові стилі для мобільного, далі `min-width` медіазапити
- Django Admin на темі Unfold
- Жодних `!important` у CSS
- Жодного inline `style="..."` та `onclick="..."`
- Файл коду не довший за 500 рядків; якщо більше — ділити на `_1`, `_2`
- CSS, JS, HTML, Python — завжди в окремих файлах, ніякого змішування
- HTMX підключається як `{% static 'js/htmx.min.js' %}` (офіційний dist >40KB)
  плюс `{% django_htmx_script %}`. Не CDN і не `django_htmx/htmx.min.js`
- Секрети тільки у змінних оточення, ніколи в репозиторії

---

# АРХІТЕКТУРА ПРОЄКТУ

```
selfbrand/
  config/
    settings/  __init__.py  base.py  develop.py  production.py  test.py
    urls.py  wsgi.py  asgi.py
  src/
    core/        # SiteSettings, SiteBlock, SeoMeta, context_processors, templatetags
    gallery/     # GalleryPhoto
    formats/     # ServiceFormat, FormatFeature
    reviews/     # Testimonial
    faq/         # FaqItem
    leads/       # Lead, forms, services (Telegram + email), views
  templates/
    base.html
    partials/    header.html  footer.html  mobile-nav.html  lang-switcher.html
                 lead-modal.html  lead-form.html  lead-success.html
    sections/    hero.html  about.html  gallery.html  formats.html
                 testimonials.html  faq.html  contacts.html
    pages/       home.html  privacy.html
    404.html  500.html
  static/
    css/   reset.css  tokens.css  base.css  typography.css  animations.css
           layout/    header.css  footer.css  grid.css
           components/ button.css  form.css  modal.css  card.css  gallery.css
                       carousel.css  accordion.css  nav-mobile.css  lang-switcher.css
           pages/     home.css  privacy.css
    js/    htmx.min.js  main.js
           modules/  sticky-header.js  mobile-nav.js  scrollspy.js  lightbox.js
                     carousel.js  accordion.js  modal.js  reveal.js  lead-form.js
    images/
  media/
  locale/  ru/  en/
  deploy/  entrypoint.sh  nginx/
  manage.py  requirements.txt  Dockerfile  docker-compose.yml  .env.example
```

Налаштування розділені на `base / develop / production / test`.
`manage.py` бере модуль із змінної оточення, за замовчуванням `develop`.

---

# МОДЕЛІ ДАНИХ

Загальні правила: у кожного списку є `order` (PositiveSmallIntegerField)
і `is_active` (BooleanField). Текстові поля дублюються парами `*_ru` / `*_en`.
Хелпер `get_text(field)` повертає значення поточної мови, з відкатом на `ru`.

**src/core**
- `SiteSettings` — singleton (`pk=1`): brand_name, logo, phone, email,
  telegram_url, instagram_url, whatsapp_url, copyright_name.
- `SiteBlock` — універсальний блок вмісту: `page`, `key`, `text_ru`, `text_en`,
  `image`, `video_file`, `video_url`, `is_visible`, `updated_at`.
  `unique_together = ("page", "key")`. Ключі виду `hero.title`, `about.portrait`,
  `gallery.section_visible`.
- `SeoMeta` — `page`, `title_ru/en`, `description_ru/en`, `og_image`.

**src/gallery**
- `GalleryPhoto` — image, alt_ru/en, caption_ru/en, order, is_active.
  Розрахунок на 15–20 записів.

**src/formats**
- `ServiceFormat` — title_ru/en, description_ru/en, price_text_ru/en,
  is_featured, order, is_active.
- `FormatFeature` — FK на формат, text_ru/en, order. Пункти «що входить».

**src/reviews**
- `Testimonial` — author_name, role_ru/en, photo (необов'язкове),
  text_ru/en, order, is_active.

**src/faq**
- `FaqItem` — question_ru/en, answer_ru/en, order, is_active.

**src/leads**
- `Lead` — name, contact, message, service (назва обраного формату),
  source, language, status, admin_note, ip, user_agent, utm_source,
  utm_medium, utm_campaign, notified_at, created_at.
- `LeadSource` — TextChoices: HEADER, HERO, ABOUT, FORMATS, FAQ, CONTACTS.
- `LeadStatus` — TextChoices: NEW, IN_PROGRESS, WON, LOST.

Кеш блоків: `site_blocks` у кеші, інвалідація в `post_save` кожної моделі вмісту.

---

# URL-КАРТА

```python
# config/urls.py
urlpatterns = [path("admin/", admin.site.urls)]
urlpatterns += i18n_patterns(
    path("", include("src.core.urls")),          # головна, privacy
    path("lead/", include("src.leads.urls")),    # форма і приймання заявки
    prefix_default_language=True,                # /ru/ і /en/ обидва з префіксом
)
```

| Адреса | Призначення |
|---|---|
| `/` | Визначення мови та редирект |
| `/ru/`, `/en/` | Головна |
| `/ru/privacy/`, `/en/privacy/` | Політика конфіденційності |
| `/{lang}/lead/form/` | GET, віддає форму у модальне вікно з підставленим форматом |
| `/{lang}/lead/submit/` | POST, приймає заявку, повертає фрагмент успіху або помилок |
| `/i18n/setlang/` | Перемикання мови (стандартна вʼю Django) |
| `/sitemap.xml`, `/robots.txt` | SEO |

---

# МУЛЬТИМОВНІСТЬ

- `LANGUAGES = [("ru", "Русский"), ("en", "English")]`, `LANGUAGE_CODE = "ru"`.
- `LocaleMiddleware` увімкнено; порядок мови: cookie → `Accept-Language` → `ru`.
- Інтерфейсні рядки — через `{% trans %}` і файли в `locale/`.
- Контент — через парні поля моделей, **не** через `gettext`.
- Перемикач мов веде на дзеркальний URL **тієї самої сторінки**. Реалізація:
  у контексті обчислюється `alternate_urls` для кожної мови через
  `translate_url(request.get_full_path(), lang)`.
- Позиція скролу зберігається: перед переходом якір поточної видимої секції
  дописується у URL, після завантаження сторінка стає на нього без анімації.
- У `<head>`: `hreflang` для `ru`, `en`, `x-default`, канонічний URL поточної мови,
  `og:locale`. У `sitemap.xml` — обидві версії з взаємними посиланнями.

---

# CSS: ТОКЕНИ І АРХІТЕКТУРА

`tokens.css` підключається першим, після `reset.css`. Жодного хардкоду кольорів
у компонентах. Кожен файл ≤ 500 рядків.

```css
:root {
  /* Фони */
  --color-bg:            #0B0F0D;
  --color-bg-alt:        #111815;
  --color-surface:       #16241C;
  --color-surface-hover: #1E3128;

  /* Акценти */
  --color-accent:        #C9A227;   /* золото — лінії, контури, рамки */
  --color-accent-dim:    #8C7434;
  --color-bordeaux:      #4A1520;   /* 1–2 елементи на сторінку */
  --color-sand:          #C9B896;

  /* Текст */
  --color-text:          #F2EFE9;
  --color-text-muted:    #A29C92;

  /* Межі */
  --border-hairline:     rgba(201,162,39,0.22);
  --border-strong:       rgba(201,162,39,0.55);

  /* Типографіка */
  --font-display: "Cormorant Garamond", Georgia, serif;
  --font-body:    "Manrope", system-ui, sans-serif;

  /* Простір */
  --container-max:  1200px;
  --section-pad-m:  64px 20px;
  --section-pad-t:  96px 32px;
  --section-pad-d:  140px 40px;

  /* Viewport та безпечні зони */
  --safe-top:    env(safe-area-inset-top, 0px);
  --safe-bottom: env(safe-area-inset-bottom, 0px);

  /* Рух */
  --ease:   cubic-bezier(0.4, 0, 0.2, 1);
  --t-fast: 150ms var(--ease);
  --t-base: 300ms var(--ease);
  --t-slow: 400ms var(--ease);

  /* Шари */
  --z-header: 100;
  --z-modal:  400;
  --z-lightbox: 450;
}
```

Правила:
- Золото не більше 8–10% площі екрана, ніколи як фон великої площі
  та ніколи як колір абзацного тексту.
- Радіуси 0–2px. Тіні не використовуються — глибина через зміну тону фону.
- Розміри заголовків через `clamp()`, без медіазапитів на шрифти:
  `.hero__title { font-size: clamp(36px, 7vw, 76px); }`
  `.section__title { font-size: clamp(28px, 4vw, 52px); }`
- Іменування BEM: `.block`, `.block__element`, `.block--modifier`.
  Максимум два рівні. Стани — утиліти `.is-open`, `.is-active`, `.is-visible`.
- Стилізація через ID заборонена.

Брейкпоінти (mobile-first, тільки `min-width`):
`480px`, `768px`, `1024px`, `1440px`. Базові стилі — без медіазапиту, від 320px.

---

# JS: МОДУЛІ

`main.js` — точка входу, імпортує модулі та ініціалізує їх після `DOMContentLoaded`.
Кожен модуль — named export, без глобальних змінних, без `innerHTML` з даними
користувача.

| Модуль | Завдання |
|---|---|
| `sticky-header.js` | Клас `.is-scrolled` після 80px; без слухача на кожен піксель — `IntersectionObserver` на сторожовий елемент |
| `mobile-nav.js` | Бургер, блокування скролу з фіксацією позиції, закриття по Esc, кліку поза меню і по пункту, пастка фокуса |
| `scrollspy.js` | Підсвічування активного пункту меню через `IntersectionObserver` |
| `lightbox.js` | Галерея на весь екран: стрілки, свайп, Esc, попереднє завантаження сусіднього кадру, повернення фокуса |
| `carousel.js` | Відгуки: свайп, стрілки, точки, клавіші, зупинка автопрокрутки при наведенні та фокусі |
| `accordion.js` | FAQ: одна відкрита відповідь, анімація висоти без стрибків, `aria-expanded` |
| `modal.js` | Модальне вікно заявки: пастка фокуса, Esc, повернення фокуса на кнопку-ініціатор |
| `reveal.js` | Поява секцій через `IntersectionObserver`, одноразово |
| `lead-form.js` | Підстановка назви формату та джерела у приховані поля перед відправкою |

Уся анімація тільки через `transform` і `opacity`.
Обов'язковий блок:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms;
    transition-duration: 0.01ms;
    scroll-behavior: auto;
  }
}
```

---

# ФОРМА ЗАЯВКИ

Точки виклику: шапка, перший екран, блок «Про мене», кожна картка формату,
блок питань, блок контактів. Кнопка передає у форму назву формату та джерело.

Поля: `Ім'я`, `Телефон або e-mail`, `Коментар`, чекбокс згоди,
приховані `service`, `source`, `language`, honeypot-поле.

Потік:

```
POST /{lang}/lead/submit/  (hx-post, hx-target="#lead-form-body", hx-swap="innerHTML")
  → перевірка honeypot і мінімального часу заповнення
  → перевірка частоти за IP (наприклад, 5 звернень на годину)
  → валідація форми на сервері
  → Lead.objects.create(...)        # спершу зберігаємо
  → notify(lead)                    # потім сповіщаємо
  → рендер lead-success.html або форми з помилками полів
```

Ключова вимога: **заявка зберігається до спроби сповіщення**. Якщо Telegram
або пошта недоступні — виняток логується, `notified_at` лишається порожнім,
відвідувач усе одно бачить успіх. Передбач management-команду
`resend_lead_notifications` для повторної відправки.

Уся логіка сповіщень — у `src/leads/services.py`, не у вʼю. Вʼю — тонкий
оркестратор. Токен бота і chat_id читаються тільки з оточення.
Таймаут HTTP-запиту до Telegram — 5 секунд.

Текст повідомлення в Telegram: ім'я, контакт, обраний формат, джерело, мова,
час, посилання на заявку в адмінці. Усі значення екрануються.

Форма також має працювати без JS: звичайний POST повертає сторінку з успіхом.

---

# ПАНЕЛЬ КЕРУВАННЯ

Реалізується за скілом `admin_cms_blocks_skill.md`. Ключові вимоги:

- Бічне меню будується **за структурою сайту**, не за додатками Django:
  «Вміст сторінок» (окремий екран на кожну секцію головної та на політику),
  «Списки» (формати, відгуки, питання), «Галерея», «Заявки», «Налаштування».
- `SiteBlock` і `GalleryPhoto` **не реєструються** як звичайні ModelAdmin —
  вони редагуються на екранах секцій.
- Галерея — ModelFormSet із перетягуванням для зміни порядку, не Inline.
- Поля форми секції мають вигляд `block__{page}__{key}__{ru|en|image|visible}`.
- Видимість секції — чекбокс, не текстове поле.
- Поля RU і EN стоять поруч в одній формі. Порожнє EN-поле підсвічується.
- Один шаблон `site_content_page.html` на всі секції.
- Кеш скидається після кожного збереження.
- Seed-команда ідемпотентна: `if not exists`, не перезаписує введений вміст.
- Ролі: власник (усе), контент-менеджер (вміст і списки), менеджер (тільки заявки).
- Заявки: фільтри за статусом, джерелом, датою, мовою; експорт у CSV;
  масова зміна статусу.

---

# MOBILE-FIRST ТА iOS SAFARI

- Базові стилі пишуться для 320px, розширення — через `min-width`.
- Повноекранні секції: `min-height: 100svh`, не `100vh`.
- Фіксовані елементи враховують `env(safe-area-inset-*)`.
- `font-size: 16px` на всіх `input`, `select`, `textarea` — інакше Safari
  збільшує сторінку при фокусі.
- `-webkit-appearance: none; border-radius: 0;` на полях форм.
- Відео: `muted autoplay loop playsinline`; на мобільних замість відео
  віддається постер.
- Блокування скролу при відкритій модалці — з фіксацією та відновленням
  позиції, без стрибка вгору.
- Горизонтальні стрічки: `-webkit-overflow-scrolling: touch` і `scroll-snap`.
- Sticky-шапка перевіряється окремо при швидкому скролі вгору в Safari.
- `<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">`

---

# ПРОДУКТИВНІСТЬ

Ціль: PageSpeed Insights ≥ 80 на мобільних, ≥ 95 на десктопі.

- Зображення в AVIF/WebP через `<picture>` і `srcset` під кожен брейкпоінт,
  завжди з явними `width`/`height` проти зсувів макета.
- Усе нижче першого екрана — `loading="lazy"`, перший екран — `fetchpriority="high"`.
- Галерея на 15–20 фото: показ мініатюр, повний розмір підвантажується
  тільки при відкритті лайтбокса.
- Шрифти self-hosted WOFF2, підмножина під кирилицю й латиницю,
  `font-display: swap`, `preload` основного накреслення.
- Критичний CSS першого екрана вбудовується в документ, решта — окремими файлами.
- JS підключається з `defer` або як `type="module"`.
- Автоматичне версіонування статики через `?v=` за часом зміни файлу.

---

# БЕЗПЕКА

- HTTPS із примусовим перенаправленням, HSTS у production.
- `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_SSL_REDIRECT`.
- `{% csrf_token %}` у кожній POST-формі; для HTMX — заголовок із cookie.
- Валідація на сервері обов'язкова навіть за наявності клієнтської.
- Екранування всіх користувацьких даних перед виводом і перед відправкою
  в Telegram.
- Обмеження типу й розміру завантажуваних файлів у адмінці.
- Адмінка закрита від індексації, захищена від перебору паролів.
- Секрети тільки в оточенні. `.env` у `.gitignore`.

---

# ТЕСТИ

Мінімальний обов'язковий набір (pytest):
- Створення заявки: валідні дані, невалідні дані, спрацювання honeypot.
- Заявка зберігається, коли сповіщення падає з винятком.
- Перемикання мови віддає дзеркальний URL.
- Порожнє EN-поле віддає RU-текст на англійській версії.
- Приховування формату прибирає його з відповіді головної сторінки.
- Адмінка: GET і POST екрана секції, скидання кешу після збереження.
- `python3 manage.py check` без попереджень.

---

# ПОРЯДОК ВИКОНАННЯ

Виконуй етапами, після кожного повідомляй що зроблено і що далі.

1. Каркас: структура каталогів, розділені налаштування, requirements, `.env.example`,
   Docker, порожні додатки, `manage.py check`.
2. Моделі всіх додатків, міграції, адмінка на Unfold, seed-команда.
3. `base.html`, шапка, підвал, мобільне меню, перемикач мов, токени й базовий CSS.
4. Секції головної в порядку з карти сайту: перший екран, про мене, галерея,
   формати, відгуки, питання, контакти.
5. Форма заявки: модалка, HTMX, сервіс сповіщень, стани успіху та помилок.
6. Сторінка політики, 404, 500, sitemap, robots, метадані та hreflang.
7. JS-модулі: лайтбокс, карусель, акордеон, scrollspy, reveal.
8. Оптимізація, тести, прогін чек-листа, підготовка до деплою.

---

# ЧЕК-ЛИСТ ГОТОВНОСТІ

- [ ] Усі кольори через CSS-змінні, жодного хардкоду
- [ ] Кожен CSS і JS файл ≤ 500 рядків
- [ ] BEM, без стилізації по ID, без `!important`, без inline-стилів
- [ ] `100svh` замість `100vh`, `env(safe-area-inset-*)` на фіксованих елементах
- [ ] `font-size: 16px` на всіх полях вводу
- [ ] HTMX із `static/js/htmx.min.js` плюс `{% django_htmx_script %}`
- [ ] `{% csrf_token %}` і honeypot у кожній публічній формі
- [ ] Заявка зберігається навіть при недоступному Telegram
- [ ] У заявці видно обраний формат і блок-джерело
- [ ] Обидві мови редагуються в адмінці, порожнє EN підставляє RU
- [ ] Приховування елемента в адмінці прибирає його з сайту
- [ ] Повторний деплой не затирає введений вміст
- [ ] `hreflang`, канонічні адреси, `sitemap.xml` з обома мовами
- [ ] Анімації тільки `transform`/`opacity`, є `prefers-reduced-motion`
- [ ] Контраст тексту ≥ 4.5:1, повна навігація з клавіатури, видимий фокус
- [ ] `aria`-атрибути на акордеоні, каруселі, модалці, мобільному меню
- [ ] Перевірено від 320px до 1920px і на реальному iPhone у Safari
- [ ] PageSpeed ≥ 80 мобільні, ≥ 95 десктоп
- [ ] Немає забороненої лексики та символіки бренду
- [ ] `python3 manage.py check` і тести проходять

# АНТИПАТЕРНИ

| Не робити | Робити |
|---|---|
| Монолітні `main.css` / `main.js` | Модульна структура з розділу вище |
| Бізнес-логіка у вʼю або шаблоні | `services.py` |
| Сповіщення до збереження заявки | Спершу зберегти, потім сповістити |
| `gettext` для контенту сайту | Парні поля моделей |
| Окремий HTML на кожну секцію адмінки | Один `site_content_page.html` |
| Seed, що перезаписує вміст | `if not exists` |
| `100vh`, `ease-in-out`, анімація `width` | `100svh`, явний `cubic-bezier`, `transform` |
| Токени й chat_id у коді | Змінні оточення |
