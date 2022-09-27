import logging


from django.views.generic import base
import unu


logger = logging.getLogger(__name__)


class Controller(base.TemplateView, unu.utils.views.mixins.debug.DebugOnlyMixin):
	template_name = 'unu/pages/fiu_app.html'

	# Per chance this needs updating, this will serve as template
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		logger.info(unu.utils.frontend.fiu.analyze.get_fiu_apps())
		context.update({
			'fiu_apps': unu.utils.frontend.fiu.analyze.get_fiu_apps(),
			'fiu_app_data': unu.utils.frontend.fiu.analyze.get_fiu_app_data(self.kwargs.get('app_folder')),
		})
		return context
