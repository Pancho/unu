import os
import logging


from django.conf import settings


logger = logging.getLogger(__name__)


def is_unu_development():
	return os.path.isdir('{}/unu'.format(settings.UNU_PROJECT_ROOT))


def insert_style(template_content, style):
	new_content = '{}{{% block style %}}{}{{% endblock style %}}{}'.format(
		template_content.split('{% block style %}')[0],
		style,
		template_content.split('{% endblock style %}')[1]
	)

	return new_content


def insert_script(template_content, script):
	new_content = '{}{{% block script %}}{}{{% endblock script %}}{}'.format(
		template_content.split('{% block script %}')[0],
		script,
		template_content.split('{% endblock script %}')[1]
	)

	return new_content


def toggle_template_static():
	skeleton_path = '{}/unu/templates/unu/skeleton.html'.format(settings.UNU_PROJECT_ROOT)
	new_skeleton = ''
	with open(skeleton_path, 'r') as skeleton_file:
		for line in skeleton_file.readlines():
			if '</main>' in line:
				if '{% optimize %}' in line:
					line = line.replace('{% optimize %}', '')
				else:
					line = line.replace('</main>', '</main>{% optimize %}')

			new_skeleton += '{}'.format(line)

	with open(skeleton_path, 'w') as skeleton_file:
		skeleton_file.write(new_skeleton)

	pages_folder = '{}/unu/templates/unu/pages'.format(settings.UNU_PROJECT_ROOT)

	for file in os.listdir(pages_folder):
		stem = file.replace('.html', '')
		static_path = 'unu/{}'.format('-'.join(stem.split('_')))
		opt_file_path = '{}/media/dist/unu-{}.opt'.format(settings.UNU_PROJECT_ROOT, '-'.join(stem.split('_')))

		with open('{}/unu/templates/unu/pages/{}'.format(settings.UNU_PROJECT_ROOT, file), 'r') as template_file:
			template_content = template_file.read()

			style_contents = template_content.split('{% block style %}')[1].split('{% endblock style %}')[0]
			script_contents = template_content.split('{% block script %}')[1].split('{% endblock script %}')[0]

			if style_contents == '{{% css \'{}\' %}}'.format(static_path):
				with open('{}.css'.format(opt_file_path), 'r') as style_file:
					template_content = insert_style(
						template_content,
						'<style>{}</style>'.format(style_file.read())
					)
			else:
				template_content = insert_style(
					template_content,
					'{{% css \'{}\' %}}'.format(static_path)
				)

			if script_contents == '{{% javascript \'{}\' %}}'.format(static_path):
				with open('{}.js'.format(opt_file_path), 'r') as script_file:
					template_content = insert_script(
						template_content,
						'<script type="text/javascript">{}</script>'.format(script_file.read())
					)
			else:
				template_content = insert_script(
					template_content,
					'{{% javascript \'{}\' %}}'.format(static_path)
				)

		with open('{}/unu/templates/unu/pages/{}'.format(settings.UNU_PROJECT_ROOT, file), 'w') as file:
			file.write(template_content)
