import logging

from django import views
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import unu


logger = logging.getLogger(__name__)


@method_decorator([csrf_exempt], name="dispatch")
class Controller(views.View, unu.utils.views.mixins.debug.DebugOnlyMixin):
    http_method_names = ["post"]

    def post(self, *args, **kwargs):
        log = unu.utils.frontend.sproo.package.create_sproo_component(
            self.request.POST.get("component-app"),
            self.request.POST.get("component-app-slug"),
            self.request.POST.get("component-name"),
            self.request.POST.get("component-use-store") is not None,
            self.request.POST.get("component-include-stylesheet") is not None,
        )
        context = {
            "status": "ok",
            "log": log,
        }
        return JsonResponse(context, encoder=unu.utils.encoders.versatile_json.Encoder)
