from http.client import NOT_FOUND
import logging

from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ObjectDoesNotExist):
        return Response({'detail': 'Not found.'}, status=NOT_FOUND)

    return response
