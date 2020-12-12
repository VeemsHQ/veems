#!/bin/sh
python manage.py migrate --noinput
celery -A veems.celery beat --loglevel=info --pidfile=celerybeat.pid --scheduler django_celery_beat.schedulers:DatabaseScheduler --max-interval=5
