import decimal
import logging
import os


from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils import text
from django.conf import settings


logger = logging.getLogger(__name__)


class AmountField(models.DecimalField):
	def __init__(self, *args, **kwargs):
		kwargs['max_digits'] = 30
		kwargs['decimal_places'] = 8
		kwargs['default'] = decimal.Decimal('0.0')
		super(AmountField, self).__init__(*args, **kwargs)


class PriceField(models.DecimalField):
	def __init__(self, *args, **kwargs):
		kwargs['max_digits'] = 16
		kwargs['decimal_places'] = 8
		kwargs['default'] = decimal.Decimal('0.0')
		super(PriceField, self).__init__(*args, **kwargs)


@deconstructible
class UploadToPathAndRename(object):
	def __init__(self, path, suffix=None, density=None):
		self.sub_path = path
		if suffix is None or suffix.strip() == '':
			self.suffix = ''
		else:
			self.suffix = f'-{suffix}'
		if density is None or density.strip() == '':
			self.density = ''
		else:
			self.density = f'-{density}'

	def __call__(self, instance, filename):
		try:
			filename = f'{text.slugify(instance.get_full_name())}{self.suffix}{self.density}.png'
		except Exception as e:
			logger.exception(f'Could not make a pretty name for image {filename} on class instance {type(instance).__name__} with id {instance.pk}')
		full_path = os.path.join(settings.MEDIA_ROOT, self.sub_path, filename)
		if os.path.exists(full_path):
			os.remove(full_path)
		return os.path.join(self.sub_path, filename)
