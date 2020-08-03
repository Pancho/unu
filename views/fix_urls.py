import logging

from django import views
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


import unu


logger = logging.getLogger(__name__)


@method_decorator([csrf_exempt], name='dispatch')
class Controller(views.View, unu.utils.views.mixins.debug.DebugOnlyMixin):
	http_method_names = ['post']

	def post(self, request, *args, **kwargs):
		result = unu.utils.django.helper.fixer.fix_urls()

		context = {
			'status': 'ok',
			'result': result,
		}
		return JsonResponse(context, encoder=unu.utils.encoders.versatile_json.Encoder)

