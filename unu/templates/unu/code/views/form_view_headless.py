import logging


from django import views
from django.http import JsonResponse{% for import in imports %}
{{ import }}{% endfor %}


from {{ app }} import forms


logger = logging.getLogger(__name__)


class Controller(views.View{% if class_extensions %}, {{ class_extensions }}{% endif %}):
    http_method_names = ["post"]
{% if 'UserPassesTestMixin' in mixins %}
    def test_func(self):
        return self.request.user.is_superuser
{% endif %}
    def get_initial(self, *args, **kwargs):
        initial = {}
        # Your code here
        return initial

    def post(self, *args, **kwargs):
        form = forms.{{ form }}(
            data=self.request.POST,
            files=self.request.FILES,
            initial=self.get_initial()
        )

        if form.is_valid():
            form.process_form()
            context = {
                "status": "ok",
            }
        else:
            context = {
                "status": "error",
                "errors": form.errors,
            }

        return JsonResponse(context)

