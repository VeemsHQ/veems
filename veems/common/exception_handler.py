from http.client import NOT_FOUND
import logging

from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)


def _get_client_ip(request):
    if request is None:
        return None
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ObjectDoesNotExist):
        logger.info(
            'Not found, client ip: %s', _get_client_ip(context.get('request'))
        )
        return Response({'detail': 'Not found.'}, status=NOT_FOUND)

    return response
