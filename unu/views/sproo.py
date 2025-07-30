import logging

from django.views.generic import base

from unu import utils


logger = logging.getLogger(__name__)


class Controller(base.TemplateView, utils.views.mixins.debug.DebugOnlyMixin):
    template_name = "unu/pages/sproo.html"

    # Per chance this needs updating, this will serve as a template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "apps_with_sproo": utils.frontend.sproo.analyze.apps_with_sproo(),
                "sproo_apps": utils.frontend.sproo.analyze.get_sproo_apps(),
                "apps": utils.django.helper.context.get_apps(),
            }
        )
        return context
