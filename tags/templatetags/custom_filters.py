from django import template

register = template.Library()


@register.filter
def add_slashes(value):
    if not value.startswith('/'):
        value = '/' + value
    if not value.endswith('/'):
        value = value + '/'
    return value

