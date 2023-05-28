import logging


from django import views
from django.http import JsonResponse


import unu


logger = logging.getLogger(__name__)


class Controller(views.View, unu.utils.views.mixins.debug.DebugOnlyMixin):
    http_method_names = ["post"]

    def post(self, *args, **kwargs):
        result = unu.utils.django.helper.fixer.fix_views(self.request.POST.get("app"))

        context = {
            "status": "ok",
            "result": result,
        }
        return JsonResponse(context, encoder=unu.utils.encoders.versatile_json.Encoder)
