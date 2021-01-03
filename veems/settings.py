"""
Django settings for veems project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import sys
from datetime import timedelta
import os
from pathlib import Path

from veems import log

log.configure_logging()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ['DEBUG'].lower() == 'true'

ALLOWED_HOSTS = []

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'django_celery_beat',
    'django_celery_results',
    'rest_framework',
    'veems.common',
    'veems.user',
    'veems.media',
    'veems.home',
    'veems.channel_manager',
    'veems.channel',
]

AUTH_USER_MODEL = 'user.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'veems.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            Path(__file__).parent.parent / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'veems.common.context_processors.global_context'
            ],
        },
    },
]

WSGI_APPLICATION = 'veems.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASS'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT'],
    }
}

AWS_REGION = os.environ['AWS_REGION']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_S3_USE_SSL = False
AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL')
# Default bucket settings
AWS_STORAGE_BUCKET_NAME = os.environ['BUCKET_STATIC']
AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')
BUCKET_MEDIA = os.environ['BUCKET_MEDIA']
AWS_DEFAULT_ACL = 'public-read'
# Media bucket settings
BUCKET_MEDIA_CUSTOM_DOMAIN = os.environ.get('BUCKET_MEDIA_CUSTOM_DOMAIN')
BUCKET_MEDIA_DEFAULT_ACL = None
BUCKET_STATIC_CUSTOM_DOMAIN = os.environ.get('BUCKET_STATIC_CUSTOM_DOMAIN')

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_ROOT = Path(__file__).parent.parent / 'staticfiles'
STATICFILES_DIRS = (
    Path(__file__).parent.parent / 'static',
    Path(__file__).parent.parent / 'react-components/dist/',
)

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': (
        'veems.common.exception_handler.api_exception_handler'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.NumericPasswordValidator'
        ),
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

ACTIVE_EXECUTOR = 'ffmpeg'

RABBITMQ_USER = os.environ['RABBITMQ_USER']
RABBITMQ_PASS = os.environ['RABBITMQ_PASS']
RABBITMQ_PORT = os.environ['RABBITMQ_PORT']
RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
RABBITMQ_VHOST = os.environ['RABBITMQ_VHOST']
CELERY_BROKER_URL = (
    f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@'
    f'{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}'
)
BROKER_URL = CELERY_BROKER_URL
CELERY_IGNORE_RESULT = False
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_AMQP_TASK_RESULT_EXPIRES = 18000  # 5 hours.
CELERY_BROKER_HEARTBEAT = 30
CELERY_BROKER_HEARTBEAT_CHECKRATE = 2
CELERY_TASK_ALWAYS_EAGER = (
    os.environ.get('CELERY_TASK_ALWAYS_EAGER') or 'false'
).lower() == 'true'
CELERY_BEAT_SCHEDULE = {
    'periodic-heartbeat': {
        'task': 'veems.tasks.task_heartbeat',
        'schedule': timedelta(seconds=30),
    },
}
CELERY_IMPORTS = [
    'veems.tasks',
    'veems.media.upload_manager',
    'veems.media.transcoder.manager',
]

DEFAULT_POST_SIGNUP_REDIRECT_VIEW_NAME = 'index'
LOGIN_REDIRECT_URL = 'index'
DEFAULT_POST_LOGOUT_REDIRECT_VIEW_NAME = 'index'
