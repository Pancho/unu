import logging


from django.views.generic import base


import unu


logger = logging.getLogger(__name__)


class Controller(base.RedirectView, unu.utils.views.mixins.debug.DebugOnlyMixin):
	permanent = False
	query_string = False
	pattern_name = 'unu:index'

	def get_redirect_url(self, *args, **kwargs):
		unu.utils.django.helper.unu.toggle_template_static()
		return super().get_redirect_url(*args, **kwargs)
