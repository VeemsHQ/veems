#!/bin/sh
python manage.py migrate --noinput
celery -A veems.celery worker --loglevel=info --autoscale=1,5
