import logging

from django.views.generic import base

import unu


logger = logging.getLogger(__name__)


class Controller(base.TemplateView, unu.utils.views.mixins.debug.DebugOnlyMixin):
    template_name = "unu/pages/index.html"

    # Per chance this needs updating, this will serve as a template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "view_choices": unu.utils.django.helper.views.CHOICES,
                "apps": unu.utils.django.helper.context.get_apps(),
            }
        )
        # Your code here
        return context
