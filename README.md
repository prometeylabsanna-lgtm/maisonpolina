# SelfBrand

Двомовний (RU/EN) персональний лендінг на Django + HTMX + Unfold CMS.

## Локальний запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python3 manage.py migrate
python3 manage.py seed_content
python3 manage.py createsuperuser
python3 manage.py runserver
```

Сайт: `http://127.0.0.1:8000/ru/`  
Адмінка: `http://127.0.0.1:8000/<ADMIN_URL>/` — шлях з `.env`, не `/admin/`

## Тести

```bash
python3 manage.py check
pytest
```

## Docker / DigitalOcean Droplet

1. Ubuntu 24.04, Docker:
   ```bash
   curl -fsSL https://get.docker.com | sh
   ```
2. Клон у `/var/www/selfbrand`, скопіювати `.env.example` → `.env`, задати паролі, `ALLOWED_HOSTS` (домен, IP, `web`, `127.0.0.1`).
3. HTTP-деплой:
   ```bash
   bash deploy/docker/deploy.sh
   curl -sf http://127.0.0.1/healthz/
   ```
4. DNS A-записи `@` і `www` → IP Droplet.
5. SSL (certbot на хості):
   ```bash
   apt install -y certbot
   mkdir -p /var/www/certbot
   docker compose -f docker-compose.yml -f docker-compose.prod.yml stop nginx
   certbot certonly --standalone -d maisonpolina.com.ua -d www.maisonpolina.com.ua --agree-tos -m admin@maisonpolina.com.ua
   ```
   Оновити `deploy/nginx/docker.prod.conf` (домен у `ssl_certificate` шляхах), у `.env`:
   ```
   USE_HTTPS=true
   SITE_URL=https://maisonpolina.com.ua
   CSRF_TRUSTED_ORIGINS=https://maisonpolina.com.ua,https://www.maisonpolina.com.ua
   ALLOWED_HOSTS=maisonpolina.com.ua,www.maisonpolina.com.ua,DROPLET_IP,127.0.0.1,localhost,web
   DJANGO_SETTINGS_MODULE=config.settings.docker
   ```
   Потім знову `bash deploy/docker/deploy.sh`.

6. Автооновлення SSL (раз на ~60–90 днів, без даунтайму):
   ```bash
   # після того як HTTPS уже працює і nginx з docker.prod.conf запущений:
   sudo bash deploy/ssl/install-renewal.sh
   ```
   Скрипт:
   - відкриває ACME webroot `/var/www/certbot` (nginx віддає `/.well-known/acme-challenge/`);
   - перемикає renewal з `standalone` на `webroot` (nginx лишається на :80);
   - ставить deploy-hook → `deploy/ssl/reload-nginx.sh` (reload контейнера після renew);
   - вмикає `certbot.timer` (перевірка двічі на добу; сертифікат оновлюється, коли лишається менше 30 днів).

   Перевірка:
   ```bash
   systemctl list-timers | grep certbot
   sudo certbot renew --dry-run
   ```

### Важливо

- Завжди `up -d --build` після `git pull` (є в `deploy.sh`).
- `SECURE_SSL_REDIRECT = False` у `config/settings/docker.py` — інакше healthcheck ламається.
- `ALLOWED_HOSTS` мусить містити `web`.
- Seed ідемпотентний: `python manage.py seed_content` не перезаписує вміст.
- `ADMIN_URL` у `.env` (і в env хостингу) має бути унікальним; `/admin/` віддає 404.
- Після `git pull` на droplet знову `bash deploy/docker/deploy.sh`, щоб nginx підхопив ACME location і volume webroot.
