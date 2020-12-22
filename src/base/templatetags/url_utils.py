from django import template
from base.utils import absolute_static_path

register = template.Library()


@register.simple_tag(takes_context=True)
def abs_static(context, url, *args, **kwargs):
    return absolute_static_path(url)
