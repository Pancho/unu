import logging

from django import views
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import unu


logger = logging.getLogger(__name__)


@method_decorator([csrf_exempt], name="dispatch")
class Controller(views.View, unu.utils.views.mixins.debug.DebugOnlyMixin):
    def post(self, request):
        js_file = request.POST.get("jsFile")
        js_content = request.POST.get("jsContent")
        css_file = request.POST.get("cssFile")
        css_content = request.POST.get("cssContent")

        unu.utils.frontend.optimization.common.optimize_file(css_file, css_content)
        success = unu.utils.frontend.optimization.common.optimize_file(
            js_file,
            js_content,
            unu.utils.frontend.optimization.javascript.optimize,
        )

        ctx = {"status": "ok" if success else "compilationError"}

        return JsonResponse(ctx, encoder=unu.utils.encoders.versatile_json.Encoder)
