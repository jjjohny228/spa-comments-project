from typing import Any

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_query_params(context: dict[str, Any]) -> dict[str, str]:
    """
    Custom template tag for generating query parameters string excluding the 'page' parameter.

    This function takes a context object as input, extracts the query parameters from the request object,
    removes the 'page' parameter if present, and then returns the query parameters string.
    """
    get_copy = context['request'].GET.copy()
    return get_copy.pop('page', True) and get_copy.urlencode()
