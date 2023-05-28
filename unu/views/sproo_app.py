import logging

from django.views.generic import base

from unu.utils import views, frontend


logger = logging.getLogger(__name__)


class Controller(base.TemplateView, views.mixins.debug.DebugOnlyMixin):
    template_name = "unu/pages/sproo_app.html"

    # Per chance this needs updating, this will serve as template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            {
                "sproo_apps": frontend.sproo.analyze.get_sproo_apps(),
                "sproo_app_data": frontend.sproo.analyze.get_sproo_app_data(
                    self.kwargs.get("app_folder")
                ),
            }
        )

        return context
