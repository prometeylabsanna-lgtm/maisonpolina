#!/usr/bin/env bash
set -euo pipefail

echo "==> Entrypoint started"
cd /app

echo "==> Waiting for PostgreSQL..."
python <<'WAIT_DB'
import os, sys, time
import psycopg2

db_url = os.environ.get("DATABASE_URL", "")
if not db_url:
    print("==> DATABASE_URL not set, skipping DB wait")
    sys.exit(0)

for attempt in range(30):
    try:
        conn = psycopg2.connect(db_url)
        conn.close()
        print(f"==> Database ready (attempt {attempt + 1})")
        sys.exit(0)
    except psycopg2.OperationalError:
        time.sleep(2)

print("==> FATAL: Database not ready after 60s")
sys.exit(1)
WAIT_DB

if [ "${DJANGO_SETTINGS_MODULE:-}" = "config.settings.production" ] || [ "${DJANGO_SETTINGS_MODULE:-}" = "config.settings.docker" ]; then
    echo "==> Running Django security checks..."
    python manage.py check --deploy || true
fi

echo "==> Running migrations..."
python manage.py migrate --noinput --verbosity 1

if python manage.py help compilemessages &>/dev/null; then
    echo "==> Compiling messages..."
    python manage.py compilemessages -l en -l ru 2>/dev/null || true
fi

if [ "${DJANGO_SETTINGS_MODULE:-}" = "config.settings.production" ] || [ "${DJANGO_SETTINGS_MODULE:-}" = "config.settings.docker" ]; then
    echo "==> Collecting static files..."
    python manage.py collectstatic --noinput --verbosity 0
    _count=$(find "${STATIC_ROOT:-/app/staticfiles}" -type f 2>/dev/null | wc -l | tr -d ' ')
    echo "==> Static files collected: ${_count}"
    if [ "${_count:-0}" -lt 10 ]; then
        echo "==> WARNING: Low static file count"
    fi
fi

mkdir -p /app/staticfiles /app/media
touch /app/staticfiles/.keep /app/media/.keep

echo "==> Starting: $*"
exec "$@"
