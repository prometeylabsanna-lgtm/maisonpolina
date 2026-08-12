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
   docker compose -f docker-compose.yml -f docker-compose.prod.yml stop nginx
   certbot certonly --standalone -d example.com -d www.example.com --agree-tos -m admin@example.com
   ```
   Оновити `deploy/nginx/docker.prod.conf` (домен у `ssl_certificate` шляхах), у `.env`:
   ```
   USE_HTTPS=true
   SITE_URL=https://example.com
   CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
   ALLOWED_HOSTS=example.com,www.example.com,DROPLET_IP,127.0.0.1,localhost,web
   DJANGO_SETTINGS_MODULE=config.settings.docker
   ```
   Потім знову `bash deploy/docker/deploy.sh`.

### Важливо

- Завжди `up -d --build` після `git pull` (є в `deploy.sh`).
- `SECURE_SSL_REDIRECT = False` у `config/settings/docker.py` — інакше healthcheck ламається.
- `ALLOWED_HOSTS` мусить містити `web`.
- Seed ідемпотентний: `python manage.py seed_content` не перезаписує вміст.
- `ADMIN_URL` у `.env` (і в env хостингу) має бути унікальним; `/admin/` віддає 404.
