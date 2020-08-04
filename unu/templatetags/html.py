import logging


from django import template
from django.utils import text
from django.utils.safestring import mark_safe


register = template.Library()
logger = logging.getLogger(__name__)


@register.filter(name='dict_to_data')
def dict_to_data(data_dict):
	return ' {}'.format(' '.join('data-{}={}'.format(
		text.slugify(key),
		mark_safe(value)
	) for key, value in data_dict.items()))
