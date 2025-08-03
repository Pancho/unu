import logging


from django.views.generic import base{% for import in imports %}
{{ import }}{% endfor %}


logger = logging.getLogger(__name__)


class Controller(base.TemplateView{% if class_extensions %}, {{ class_extensions }}{% endif %}):
	template_name = '{{ template_name|safe }}'
{% if 'UserPassesTestMixin' in mixins %}
	def test_func(self):
		return self.request.user.is_superuser
{% endif %}
	# Per chance this needs updating, this will serve as a template
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# Your code here
		return context
