import logging


from django import views
from django.http import JsonResponse


from unu import utils


logger = logging.getLogger(__name__)


class Controller(utils.views.mixins.debug.DebugOnlyMixin, views.View):
	http_method_names = ['post']

	def post(self, request, *args, **kwargs):
		context = {
			'status': 'ok',
			'log': utils.django.helper.views.get_new(self.kwargs.get('view'), self.request),
		}
		return JsonResponse(context, encoder=utils.encoders.versatile_json.Encoder)
