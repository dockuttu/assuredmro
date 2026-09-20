#!/usr/bin/env bash
# deploy.sh — git-based deploy for assuredmro.com (runs ON the VPS from /root/assuredmro-src)
set -euo pipefail
SRC="${SRC:-/root/assuredmro-src}"
LIVE="${LIVE:-/root/assuredmro}"
BRANCH="${BRANCH:-main}"
cd "$SRC"
echo "==> Pulling latest ($BRANCH)"
git fetch origin --quiet || { echo "!! git fetch failed — aborting, live site untouched"; exit 1; }
git reset --hard "origin/$BRANCH"
echo "    now at: $(git rev-parse --short HEAD) — $(git log -1 --pretty=%s)"
echo "==> ABIM board-certification badge in every footer"
python3 abim_badge.py site

mkdir -p "$LIVE"
echo "==> Promoting to live ($LIVE/site)"
rm -rf "$LIVE/site.new"; cp -a site "$LIVE/site.new"
rm -rf "$LIVE/site.old"; [ -d "$LIVE/site" ] && mv "$LIVE/site" "$LIVE/site.old"
mv "$LIVE/site.new" "$LIVE/site"
cp -f docker-compose.yml "$LIVE/docker-compose.yml"
cd "$LIVE" && docker compose up -d --force-recreate --remove-orphans
docker ps --format 'table {{.Names}}\t{{.Status}}' | grep assuredmro || true
echo "==> Deploy complete. Rollback: rm -rf $LIVE/site && mv $LIVE/site.old $LIVE/site && cd $LIVE && docker compose up -d --force-recreate"
