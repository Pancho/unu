import logging


from django import views
from django.http import JsonResponse


import unu


logger = logging.getLogger(__name__)


class Controller(unu.utils.views.mixins.debug.DebugOnlyMixin, views.View):
	http_method_names = ['post']

	def post(self, request, *args, **kwargs):
		context = {
			'status': 'ok',
			'log': unu.utils.django.helper.views.get_new(self.kwargs.get('view'), self.request),
		}
		return JsonResponse(context, encoder=unu.utils.encoders.versatile_json.Encoder)
