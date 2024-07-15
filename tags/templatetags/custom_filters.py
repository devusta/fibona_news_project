from django import template

register = template.Library()


@register.filter
def add_slashes(value):
    if not value.startswith('/'):
        value = '/' + value
    if not value.endswith('/'):
        value = value + '/'
    return value


@register.filter
def add_lang_code(path, lang_code):
    return f'/{lang_code}{path}'
