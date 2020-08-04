import decimal
import logging


from django.db import models


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
