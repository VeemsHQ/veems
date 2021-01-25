import json

from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe

register = template.Library()

"""
A template filter to display data in JSON format - useful when debugging the UI.

Usage:
    {% data|to_json %}
"""


@register.filter
def to_json(data, indent=None):
    return mark_safe(
        json.dumps(data, sort_keys=True, indent=indent, cls=DjangoJSONEncoder).replace("'", '&#39;'),
    )
