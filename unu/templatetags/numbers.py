import logging


from django import template


register = template.Library()
logger = logging.getLogger(__name__)


def to_percent(value, decimal_places):
    return "{{:.{}%}}".format(decimal_places).format(value)
