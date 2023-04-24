from django import template

register = template.Library()

@register.filter(name='split')
def split(value, arg):
    """
    Split the value by the argument passed to the filter.
    """
    return value.split(arg)
