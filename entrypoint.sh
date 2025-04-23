#!/usr/bin/env sh
set -e

# Wait for DB (optional, you could use proper healthchecks)
# sleep 10

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Launch Gunicorn
exec gunicorn MoneyManager.wsgi:application \
     --bind 0.0.0.0:8000 \
     --workers 3