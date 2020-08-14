import logging


from django.http import JsonResponse
from django import views


import unu


logger = logging.getLogger(__name__)


class Controller(unu.utils.views.mixins.debug.DebugOnlyMixin, views.View):
	http_method_names = ['get']

	def get(self, request, *args, **kwargs):
		context = {
			'status': 'ok',
			'apps': unu.utils.django.helper.context.get_apps(request.GET.get('withModels') == 'true'),
		}
		return JsonResponse(context, encoder=unu.utils.encoders.versatile_json.Encoder)
