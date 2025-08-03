import logging

from django.views.generic import base

import unu


logger = logging.getLogger(__name__)


class Controller(base.TemplateView, unu.utils.views.mixins.debug.DebugOnlyMixin):
    template_name = "unu/pages/new_view.html"

    # Per chance this needs updating, this will serve as a template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            {
                "view": self.kwargs.get("view"),
                "selected_view": unu.utils.django.helper.views.CHOICES.get(self.kwargs.get("view")),
            }
        )

        return context
