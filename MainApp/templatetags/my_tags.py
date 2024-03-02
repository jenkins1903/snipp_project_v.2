from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='convert_newlines')
def convert_newlines(value):
    return mark_safe(value.replace('\n', '<br>'))