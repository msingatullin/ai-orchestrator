#!/bin/bash
# Issue Let's Encrypt certificates using Certbot in a Docker container.
# Usage: DOMAIN=example.com EMAIL=admin@example.com ./scripts/certbot.sh

set -e
if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
  echo "Usage: DOMAIN=example.com EMAIL=user@example.com ./scripts/certbot.sh"
  exit 1
fi

docker run --rm -v "$(pwd)/nginx/tls:/etc/letsencrypt" -p 80:80 \
  certbot/certbot certonly --standalone --non-interactive \
  --agree-tos -m "$EMAIL" -d "$DOMAIN"
