import os
import logging


from django.conf import settings


logger = logging.getLogger(__name__)


def is_unu_development():
	return os.path.isdir(f'{settings.UNU_PROJECT_ROOT}/unu')


def insert_style(template_content, style):
	new_content = f'''{template_content.split('{% block style %}')[0]}{{% block style %}}{style}{{% endblock style %}}{template_content.split('{% endblock style %}')[1]}'''

	return new_content


def insert_script(template_content, script):
	new_content = f'''{template_content.split('{% block script %}')[0]}{{% block script %}}{script}{{% endblock script %}}{template_content.split('{% endblock script %}')[1]}'''

	return new_content


def toggle_template_static():
	skeleton_path = f'{settings.UNU_PROJECT_ROOT}/unu/templates/unu/skeleton.html'
	new_skeleton = ''
	with open(skeleton_path, 'r') as skeleton_file:
		for line in skeleton_file.readlines():
			if '{% block script %}{% endblock script %}' in line:
				if '{% optimize %}' in line:
					line = line.replace('{% optimize %}', '')
				else:
					line = line.replace('{% block script %}{% endblock script %}', '{% block script %}{% endblock script %}{% optimize %}')

			new_skeleton += f'{line}'

	with open(skeleton_path, 'w') as skeleton_file:
		skeleton_file.write(new_skeleton)

	pages_folder = f'{settings.UNU_PROJECT_ROOT}/unu/templates/unu/pages'

	for file in os.listdir(pages_folder):
		stem = file.replace('.html', '')
		static_path = f'''unu/{'-'.join(stem.split('_'))}'''
		opt_file_path = f'''{settings.UNU_PROJECT_ROOT}/media/dist/unu-{'-'.join(stem.split('_'))}.opt'''

		with open(f'{settings.UNU_PROJECT_ROOT}/unu/templates/unu/pages/{file}', 'r') as template_file:
			template_content = template_file.read()

			style_contents = template_content.split('{% block style %}')[1].split('{% endblock style %}')[0]
			script_contents = template_content.split('{% block script %}')[1].split('{% endblock script %}')[0]

			if style_contents == f'{{% css \'{static_path}\' %}}':
				with open(f'{opt_file_path}.css', 'r') as style_file:
					template_content = insert_style(
						template_content,
						f'<style>{style_file.read()}</style>'
					)
			else:
				template_content = insert_style(
					template_content,
					f'{{% css \'{static_path}\' %}}'
				)

			if script_contents == f'{{% javascript \'{static_path}\' %}}':
				with open(f'{opt_file_path}.js', 'r') as script_file:
					template_content = insert_script(
						template_content,
						f'<script type="text/javascript">{script_file.read()}</script>'
					)
			else:
				template_content = insert_script(
					template_content,
					f'{{% javascript \'{static_path}\' %}}'
				)

		with open(f'{settings.UNU_PROJECT_ROOT}/unu/templates/unu/pages/{file}', 'w') as file:
			file.write(template_content)
