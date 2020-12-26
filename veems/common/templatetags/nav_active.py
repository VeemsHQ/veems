from django.urls import resolve
from django.template import Library

register = Library()


@register.simple_tag
def nav_active(request, url):
    """
    In template: {% nav_active request "url_name_here" %}
    """
    url_name = resolve(request.path).url_name
    if url_name == url:
        return 'active'
    return ''
