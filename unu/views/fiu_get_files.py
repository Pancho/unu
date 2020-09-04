import logging


from django import views
from django.http import JsonResponse
import unu


logger = logging.getLogger(__name__)


class Controller(views.View, unu.utils.views.mixins.debug.DebugOnlyMixin):
	http_method_names = ['get']

	def get(self, request, *args, **kwargs):
		unu.utils.frontend.fiu.package.get_fiu_files()
		context = {
			'status': 'ok',
		}
		return JsonResponse(context, encoder=unu.utils.encoders.versatile_json.Encoder)

