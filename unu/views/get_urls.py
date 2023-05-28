import logging

from django import views
from django.http import JsonResponse
from django.urls import get_resolver

import unu


logger = logging.getLogger(__name__)


class Controller(views.View, unu.utils.views.mixins.debug.DebugOnlyMixin):
    http_method_names = ["get"]

    def get(self, *args, **kwargs):
        urls = []
        apps = unu.utils.django.helper.context.get_apps()
        namespace_dict = get_resolver().namespace_dict
        for app in apps:
            namespace_tuple = namespace_dict.get(app)
            if namespace_tuple is not None:
                resolver = namespace_tuple[1]
                urls.extend([f"{app}:{pattern.name}" for pattern in resolver.url_patterns])

        context = {
            "status": "ok",
            "urlNames": sorted(urls),
        }
        return JsonResponse(context, encoder=unu.utils.encoders.versatile_json.Encoder)
