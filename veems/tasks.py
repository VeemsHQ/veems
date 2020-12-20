import logging

from veems.celery import app

logger = logging.getLogger(__name__)


@app.task(bind=False)
def task_heartbeat():
    logger.info('Heartbeat task executed')
