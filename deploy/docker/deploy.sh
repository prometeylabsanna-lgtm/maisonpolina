#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

COMPOSE=(docker compose -f docker-compose.yml)
if [ -f docker-compose.prod.yml ] && [ "${USE_PROD_COMPOSE:-1}" = "1" ]; then
  COMPOSE=(docker compose -f docker-compose.yml -f docker-compose.prod.yml)
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
