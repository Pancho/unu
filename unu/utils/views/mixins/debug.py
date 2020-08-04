import logging


from django.conf import settings


logger = logging.getLogger(__name__)


class DebugOnlyMixin:
	def dispatch(self, request, *args, **kwargs):
		if not settings.DEBUG:
			logger.error('Attempt at calling a DEBUG only view while it\'s set to False')
			raise Exception('This view can be run only during debug phase.')
		return super().dispatch(request, *args, **kwargs)
