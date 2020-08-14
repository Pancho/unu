import logging


from django.http import JsonResponse
from django import views


from unu import utils


logger = logging.getLogger(__name__)


class Controller(utils.views.mixins.debug.DebugOnlyMixin, views.View):
	http_method_names = ['get']

	def get(self, request, *args, **kwargs):
		recommendations = utils.django.helper.analyze.analyze()

		context = {
			'status': 'ok',
			'recommendations': recommendations,
		}
		return JsonResponse(context, encoder=utils.encoders.versatile_json.Encoder)
