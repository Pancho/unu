import logging


from django.views.generic import base
import unu


logger = logging.getLogger(__name__)


class Controller(base.TemplateView, unu.utils.views.mixins.debug.DebugOnlyMixin):
	template_name = 'unu/pages/fiu.html'

	# Per chance this needs updating, this will serve as template
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({
			'has_fiu': unu.utils.frontend.fiu.analyze.has_fiu(),
			'has_fiu_app': unu.utils.frontend.fiu.analyze.has_fiu_app(),
			'fiu_app_data': unu.utils.frontend.fiu.analyze.get_fiu_app_data(),
		})
		return context
