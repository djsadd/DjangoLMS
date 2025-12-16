#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/app"
SQLITE_PATH="${SQLITE_PATH:-/data/db.sqlite3}"
SQLITE_SEED_PATH="${SQLITE_SEED_PATH:-${APP_DIR}/db.sqlite3}"

# Copy the project SQLite DB into the mounted volume only on first run
if [ ! -f "$SQLITE_PATH" ] && [ -f "$SQLITE_SEED_PATH" ]; then
  echo "Seeding SQLite database from ${SQLITE_SEED_PATH} to ${SQLITE_PATH}"
  mkdir -p "$(dirname "$SQLITE_PATH")"
  cp "$SQLITE_SEED_PATH" "$SQLITE_PATH"
fi

python manage.py migrate --noinput
python manage.py migrate_sqlite_to_postgres || true

exec "$@"
