#!/usr/bin/env bash
# One-time setup on the DigitalOcean droplet:
# - webroot for ACME challenges (no downtime)
# - switch renewal from standalone → webroot if needed
# - deploy-hook to reload Docker nginx
# - enable certbot.timer (every ~12h; renews when <30 days left ≈ every 60–90 days)
set -euo pipefail

DOMAIN="${SSL_DOMAIN:-maisonpolina.com.ua}"
WEBROOT="${SSL_WEBROOT:-/var/www/certbot}"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
RENEWAL="/etc/letsencrypt/renewal/${DOMAIN}.conf"
HOOK_DIR="/etc/letsencrypt/renewal-hooks/deploy"
HOOK="${HOOK_DIR}/01-reload-docker-nginx.sh"

if [ "$(id -u)" -ne 0 ]; then
  echo "Run as root: sudo bash deploy/ssl/install-renewal.sh"
  exit 1
fi

apt-get update -qq
apt-get install -y -qq certbot

mkdir -p "${WEBROOT}/.well-known/acme-challenge"
chmod -R a+rX "${WEBROOT}"

# Symlink project hook so it survives certbot upgrades
mkdir -p "${HOOK_DIR}"
cat > "${HOOK}" <<EOF
#!/usr/bin/env bash
set -euo pipefail
exec bash "${ROOT}/deploy/ssl/reload-nginx.sh"
EOF
chmod +x "${HOOK}"
chmod +x "${ROOT}/deploy/ssl/reload-nginx.sh"

if [ -f "${RENEWAL}" ]; then
  echo "==> Updating ${RENEWAL} authenticator → webroot"
  # Prefer webroot so renew works while Docker nginx holds :80
  if grep -qE '^[[:space:]]*authenticator[[:space:]]*=' "${RENEWAL}"; then
    sed -i 's/^[[:space:]]*authenticator[[:space:]]*=.*/authenticator = webroot/' "${RENEWAL}"
  else
    printf '\nauthenticator = webroot\n' >> "${RENEWAL}"
  fi

  if grep -qE '^[[:space:]]*webroot_path[[:space:]]*=' "${RENEWAL}"; then
    sed -i "s|^[[:space:]]*webroot_path[[:space:]]*=.*|webroot_path = ${WEBROOT}|" "${RENEWAL}"
  else
    # Place under [renewalparams] if present, else append
    if grep -q '^\[renewalparams\]' "${RENEWAL}"; then
      sed -i "/^\[renewalparams\]/a webroot_path = ${WEBROOT}" "${RENEWAL}"
    else
      printf '\nwebroot_path = %s\n' "${WEBROOT}" >> "${RENEWAL}"
    fi
  fi

  # Remove standalone-only options that break webroot renew
  sed -i '/^[[:space:]]*http01_port[[:space:]]*=/d' "${RENEWAL}" || true
else
  echo "==> Warning: ${RENEWAL} not found. Issue the cert first, then re-run this script."
fi

# Built-in systemd timer (Ubuntu packaging) — twice daily, renews when due
if systemctl list-unit-files | grep -q '^certbot.timer'; then
  systemctl enable --now certbot.timer
  systemctl restart certbot.timer
  echo "==> certbot.timer enabled"
  systemctl list-timers certbot.timer --no-pager || true
else
  # Fallback cron if timer package missing
  CRON_FILE=/etc/cron.d/certbot-selfbrand
  cat > "${CRON_FILE}" <<'CRON'
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
0 3,15 * * * root certbot renew --quiet
CRON
  chmod 644 "${CRON_FILE}"
  echo "==> Installed cron fallback ${CRON_FILE}"
fi

echo "==> Dry-run renew (safe; does not replace live cert unless due)"
certbot renew --dry-run

echo "==> Done. Certificates will auto-renew; nginx reloads via deploy-hook."
echo "    Check: systemctl list-timers | grep certbot"
echo "    Logs:  journalctl -u certbot.service -n 50"
