#!/usr/bin/env sh
set -e


# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Launch Gunicorn
exec gunicorn MoneyManager.wsgi:application \
     --bind 0.0.0.0:8000 \
     --workers 3