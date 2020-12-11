import sys
import logging


def configure_logging():
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(handler)
    google_logger = logging.getLogger('googleapiclient.http')
    google_logger.setLevel(logging.ERROR)
    google_logger.addHandler(handler)
    urllib_logger = logging.getLogger('urllib3.connectionpool')
    urllib_logger.setLevel(logging.ERROR)
    urllib_logger.addHandler(handler)
    newrelic_logger = logging.getLogger('newrelic.core.data_collector')
    newrelic_logger.setLevel(logging.ERROR)
    newrelic_logger.addHandler(handler)
    logging.info('Configured logging')
