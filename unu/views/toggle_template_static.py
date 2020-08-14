import logging


from django.views.generic import base


from unu import utils


logger = logging.getLogger(__name__)


class Controller(base.RedirectView, utils.views.mixins.debug.DebugOnlyMixin):
	permanent = False
	query_string = False
	pattern_name = 'unu:index'

	def get_redirect_url(self, *args, **kwargs):
		utils.django.helper.unu.toggle_template_static()
		return super().get_redirect_url(*args, **kwargs)
