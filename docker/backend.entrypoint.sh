#!/bin/sh
set -e

# Optional: wait for Postgres using simple TCP check
if [ -n "$DATABASE_URL" ]; then
  # If DB_HOST/DB_PORT provided, use them, else fall back to service default
  DB_HOST="${DB_HOST:-db}"
  DB_PORT="${DB_PORT:-5432}"
  echo "Waiting for Postgres at $DB_HOST:$DB_PORT ..."
  until nc -z "$DB_HOST" "$DB_PORT"; do
    sleep 1
    echo "  still waiting..."
  done
  echo "Postgres is up!"
fi

# Run migrations & (optionally) collect static
python manage.py migrate --noinput
# Not strictly needed in dev:
python manage.py collectstatic --noinput || true

# Dev server (auto-reload)
python manage.py runserver 0.0.0.0:8000
