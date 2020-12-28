from django.core.exceptions import ValidationError
from iso639 import languages


def validate_language(value):
    try:
        languages.get(alpha2=value)
    except KeyError as exc:
        raise ValidationError('fdf') from exc
