from django import template

register = template.Library()

@register.filter
def split(value, delimiter=','):
    """Split a string by delimiter and return list"""
    if value:
        # Clean up the string and split
        return [item.strip() for item in str(value).split(delimiter) if item.strip()]
    return []