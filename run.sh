#!/usr/bin/env bash

set -e

# python manage.py compress
echo "Collecting static files"
python manage.py collectstatic --noinput
echo "Running migrations"
python manage.py migrate --noinput
echo "Running web service"
uwsgi --ini uwsgi.ini
