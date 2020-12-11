import os
from functools import wraps
import logging
from uuid import uuid4

from celery import Celery, Task, shared_task
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veems.settings')

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[
        CeleryIntegration(),
        DjangoIntegration(),
        LoggingIntegration(level=logging.INFO, event_level=logging.WARNING),
    ],
)

app = Celery('veems')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
assert 'sqs' not in app.conf.broker_url
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


class NamedTask(Task):
    def _gen_task_id(self):
        id_end = str(uuid4())
        return {'task_id': f'{self.name}-{id_end}'}

    def apply(self, *args, **kwargs):
        kwargs.update(self._gen_task_id())
        return Task.apply(self, *args, **kwargs)

    def apply_async(self, *args, **kwargs):
        kwargs.update(self._gen_task_id())
        return Task.apply_async(self, *args, **kwargs)


def async_task(**kwargs):
    def decorator(func):
        base_kwargs = dict(
            ignore_result=False,
            base=NamedTask,
            autoretry_for=(Exception, ),
            retry_backoff=2,
            retry_kwargs={'max_retries': 3},
            acks_late=True,
            name=func.__name__,
        )
        base_kwargs.update(kwargs)

        @shared_task(**base_kwargs)
        @wraps(func)
        def wrapper(*args, **kwargs):
            logging.info('Celery task %s started', func.__name__)
            try:
                result = func(*args, **kwargs)
            except Exception:
                logging.exception(
                    'Celery task %s raised an unexpected exception',
                    func.__name__,
                )
                raise
            logging.info('Celery task %s ended', func.__name__)
            return result

        return wrapper

    return decorator
