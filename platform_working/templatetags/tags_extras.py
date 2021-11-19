from django import template

register = template.Library()


@register.filter(name='time')
def time(value):
    return value.strftime("%H:%M:%S")
