import logging


from django.http import JsonResponse
from django import views
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


import unu


logger = logging.getLogger(__name__)


@method_decorator([csrf_exempt], name='dispatch')
class Controller(unu.utils.views.mixins.debug.DebugOnlyMixin, views.View):
	http_method_names = ['post']

	def post(self, request, *args, **kwargs):
		unu.utils.frontend.optimization.closure.add_closure_compiler()

		context = {
			'status': 'ok',
		}
		return JsonResponse(context, encoder=unu.utils.encoders.versatile_json.Encoder)
