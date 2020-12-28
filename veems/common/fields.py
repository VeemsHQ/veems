import base64
import uuid

from django.db.models import CharField


def _default():
    return (
        base64.urlsafe_b64encode(uuid.uuid4().bytes)
        .rstrip(b'=')
        .decode('ascii')
        .replace('/', '')
        .replace('-', '')
        .replace('_', '')
    )[:12]


class ShortUUIDField(CharField):
    """
    UUIDField stored in 21 Chars
    Example: uuid = UUIDField(editable=False)
    """

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 12)
        kwargs['default'] = _default
        CharField.__init__(self, *args, **kwargs)
