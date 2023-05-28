import logging


from django import template
from django.utils.safestring import mark_safe


register = template.Library()
logger = logging.getLogger(__name__)


@register.filter(name="str_remove")
def str_remove(value, remove):
    return mark_safe(value.replace(remove, ""))


@register.filter(name="concat")
def concat(value, addition):
    return f"{value}{addition}"
