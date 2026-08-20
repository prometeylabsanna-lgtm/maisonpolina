#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

# Prod nginx (443 + Let's Encrypt) only when USE_HTTPS=true in .env,
# or when USE_PROD_COMPOSE=1 is set explicitly.
_use_prod="${USE_PROD_COMPOSE:-}"
if [ -z "${_use_prod}" ]; then
  if [ -f .env ] && grep -qE '^[[:space:]]*USE_HTTPS[[:space:]]*=[[:space:]]*(true|True|1)[[:space:]]*$' .env; then
    _use_prod=1
  else
    _use_prod=0
  fi
fi

COMPOSE=(docker compose -f docker-compose.yml)
if [ -f docker-compose.prod.yml ] && [ "${_use_prod}" = "1" ]; then
  echo "==> Using docker-compose.prod.yml (HTTPS nginx)"
  COMPOSE=(docker compose -f docker-compose.yml -f docker-compose.prod.yml)
else
  echo "==> Using HTTP-only nginx (docker.conf)"
fi

free_host_ports() {
  for port in 80 443; do
    if command -v fuser >/dev/null 2>&1; then
      fuser -k "${port}/tcp" 2>/dev/null || true
    fi
  done
  systemctl stop nginx 2>/dev/null || true
  systemctl disable nginx 2>/dev/null || true
}

echo "==> Freeing host ports 80/443"
free_host_ports

echo "==> Building and starting"
"${COMPOSE[@]}" up -d --build

echo "==> Waiting for healthz"
for i in $(seq 1 30); do
  if curl -sf http://127.0.0.1/healthz/ >/dev/null 2>&1; then
    echo "==> HTTP healthz OK"
    break
  fi
  sleep 2
done

echo "==> Service inventory"
"${COMPOSE[@]}" ps

echo "==> Done"
