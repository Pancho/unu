import logging


from django.http import JsonResponse
from django import views


import unu


logger = logging.getLogger(__name__)


class Controller(unu.utils.views.mixins.debug.DebugOnlyMixin, views.View):
	http_method_names = ['get']

	def get(self, request, *args, **kwargs):
		recommendations = unu.utils.django.helper.analyze.analyze()

		context = {
			'status': 'ok',
			'recommendations': recommendations,
		}
		return JsonResponse(context, encoder=unu.utils.encoders.versatile_json.Encoder)
