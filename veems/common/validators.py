from django.core.exceptions import ValidationError
from iso639 import languages


def validate_language(value):
    try:
        languages.get(alpha2=value)
    except KeyError as exc:
        raise ValidationError('Invalid language') from exc


def validate_minimum_size(width=None, height=None):
    def validator(image):
        error = False
        if width is not None and image.width < width:
            error = True
        if height is not None and image.height < height:
            error = True
        if error:
            raise ValidationError(
                [f'Size should be at least {width} x {height} pixels.']
            )

    return validator
