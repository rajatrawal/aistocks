from django import template

register =template.Library()

@register.filter
def get(value,key):
    return value.get(key, '')
