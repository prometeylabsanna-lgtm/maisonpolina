#!/usr/bin/env bash
# Certbot deploy-hook: reload nginx inside Docker after certificate renewal.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

COMPOSE=(docker compose -f docker-compose.yml -f docker-compose.prod.yml)

if ! "${COMPOSE[@]}" ps --status running --services 2>/dev/null | grep -qx nginx; then
  echo "reload-nginx: nginx container not running, skip"
  exit 0
fi

"${COMPOSE[@]}" exec -T nginx nginx -t
"${COMPOSE[@]}" exec -T nginx nginx -s reload
echo "reload-nginx: nginx reloaded with new certificate"
