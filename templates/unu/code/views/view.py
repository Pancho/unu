import logging

from django import views
from django.http import JsonResponse{% for import in imports %}
{{ import }}{% endfor %}


logger = logging.getLogger(__name__)


class Controller(views.View{% if class_extensions %}, {{ class_extensions }}{% endif %}):
	http_method_names = [{{ http_methods|safe }}]
{% if 'UserPassesTestMixin' in mixins %}
	def test_func(self):
		# Change this test to suit your needs
		return self.request.user.is_superuser
{% endif %}{% for method in methods %}
	def {{ method|lower }}(self, request, *args, **kwargs):
		context = {
			# Result for {{ method }}
		}
		return JsonResponse(context, encoder=unu.utils.encoders.versatile_json.Encoder)
{% endfor %}
