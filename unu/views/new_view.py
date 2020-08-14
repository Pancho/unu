import logging


from django.views.generic import base


from unu import utils


logger = logging.getLogger(__name__)


class Controller(utils.views.mixins.debug.DebugOnlyMixin, base.TemplateView):
	template_name = 'unu/pages/new_view.html'

	# Per chance this needs updating, this will serve as template
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context.update({
			'view': self.kwargs.get('view'),
			'selected_view': utils.django.helper.views.CHOICES.get(self.kwargs.get('view')),
		})

		return context
