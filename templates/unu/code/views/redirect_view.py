import logging

from django.views.generic import base{% for import in imports %}
{{ import }}{% endfor %}


logger = logging.getLogger(__name__)


class Controller(base.RedirectView{% if class_extensions %}, {{ class_extensions }}{% endif %}):
	permanent = {{ permanent }}
	query_string = {{ query_string }}
	pattern_name = '{{ pattern_name }}'
{% if 'UserPassesTestMixin' in mixins %}
	def test_func(self):
		return self.request.user.is_superuser
{% endif %}
	def get_redirect_url(self, *args, **kwargs):
		# Your code here
		return super().get_redirect_url(*args, **kwargs)
