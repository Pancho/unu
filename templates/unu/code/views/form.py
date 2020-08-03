import logging


from django import forms


logger = logging.getLogger(__name__)


class {{ form }}(forms.Form):
	# Your form fields here

	def __init__(self, *args, **kwargs):
		super({{ form }}, self).__init__(*args, **kwargs)
		# Your field and form update code here

	def process_form(self):
		cleaned_data = self.cleaned_data
		# Your save code here
