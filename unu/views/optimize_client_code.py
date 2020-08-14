import logging


from django import views
from django.http import JsonResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


from unu import utils


logger = logging.getLogger(__name__)


@method_decorator([csrf_exempt], name='dispatch')
class Controller(utils.views.mixins.debug.DebugOnlyMixin, views.View):
	def post(self, request, *args, **kwargs):
		js_file = request.POST.get('jsFile')
		js_content = request.POST.get('jsContent')
		css_file = request.POST.get('cssFile')
		css_content = request.POST.get('cssContent')

		utils.frontend.optimization.common.optimize_file(css_file, css_content)
		success = utils.frontend.optimization.common.optimize_file(js_file, js_content, utils.frontend.optimization.javascript.optimize)

		ctx = {
			'status': 'ok' if success else 'compilationError'
		}

		return JsonResponse(ctx, encoder=utils.encoders.versatile_json.Encoder)
