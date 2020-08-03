import logging

from django.urls import path
from django.views.generic import base


import unu


logger = logging.getLogger(__name__)


class Controller(unu.utils.views.mixins.debug.DebugOnlyMixin, base.TemplateView):
	template_name = 'unu/pages/index.html'

	# Per chance this needs updating, this will serve as template
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({
			'has_closure_compiler': unu.utils.frontend.optimization.closure.has_closure_compiler(),
			'view_choices': unu.utils.django.helper.views.CHOICES,
			'is_unu_development': unu.utils.django.helper.unu.is_unu_development(),
		})
		# Your code here
		return context
