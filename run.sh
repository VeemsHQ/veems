#!/usr/bin/env sh

set -e

echo "Running createcachetable"
python manage.py createcachetable
# python manage.py compress
echo "Collecting static files"
python manage.py collectstatic --noinput
echo "Running migrations"
python manage.py migrate --noinput
echo "Clearing cache"
python manage.py clear_cache
echo "Running web service"
uwsgi --ini uwsgi.ini
