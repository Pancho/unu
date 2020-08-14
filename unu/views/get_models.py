import logging


from django import views
from django.http import JsonResponse


from unu import utils


logger = logging.getLogger(__name__)


class Controller(views.View, utils.views.mixins.debug.DebugOnlyMixin):
	http_method_names = ['get']

	def get(self, request, *args, **kwargs):
		context = {
			'status': 'ok',
			'models': utils.django.helper.context.get_models(request.GET.get('app')),
		}
		return JsonResponse(context, encoder=utils.encoders.versatile_json.Encoder)

