#!/usr/bin/env bash
set -e
echo "Running migrations"
python manage.py migrate --noinput
echo "Collecting static files"
python manage.py collectstatic --noinput
echo "Running web service"
python manage.py runserver
