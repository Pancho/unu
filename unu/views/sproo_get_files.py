import logging

from django import views
from django.http import JsonResponse

import unu


logger = logging.getLogger(__name__)


class Controller(views.View, unu.utils.views.mixins.debug.DebugOnlyMixin):
    http_method_names = ["get"]

    def get(self, *args, **kwargs):
        unu.utils.frontend.sproo.package.get_sproo_files(kwargs.get("app"))
        context = {
            "status": "ok",
        }
        return JsonResponse(context, encoder=unu.utils.encoders.versatile_json.Encoder)
