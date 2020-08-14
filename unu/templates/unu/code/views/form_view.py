import logging


from django.views.generic import edit
from django.urls import reverse_lazy{% for import in imports %}
{{ import }}{% endfor %}


from {{ app }} import forms


logger = logging.getLogger(__name__)


class Controller(edit.FormView{% if class_extensions %}, {{ class_extensions }}{% endif %}):
	template_name = '{{ template_name }}'
	success_url = reverse_lazy('{{ success_pattern }}')
	form = forms.{{ form }}
{% if 'UserPassesTestMixin' in mixins %}
	def test_func(self):
		return self.request.user.is_superuser
{% endif %}
	def get_initial(self, *args, **kwargs):
		initial = {}
		# Your code here
		return initial

	def get_form(self, form_class=None):
		return forms.{{ form }}(**self.get_form_kwargs())

	def form_valid(self, form):
		form.process_form()
		return super().form_valid(form)

	# Per chance this needs updating, this will serve as template
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# Your code here
		return context
