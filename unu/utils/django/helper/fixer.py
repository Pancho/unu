import os
import logging


from django.conf import settings
from django.template import loader


import unu


logger = logging.getLogger(__name__)


def fix_views():
	fixed = []
	skipped = []
	result = []
	apps = unu.utils.django.helper.context.get_apps()

	for app in apps:
		if os.path.isfile(f'{settings.UNU_PROJECT_ROOT}/{app}/views.py') and not os.path.isdir(f'{settings.UNU_PROJECT_ROOT}/{app}/views'):
			os.remove(f'{settings.UNU_PROJECT_ROOT}/{app}/views.py')
			os.mkdir(f'{settings.UNU_PROJECT_ROOT}/{app}/views')
			with open(f'{settings.UNU_PROJECT_ROOT}/{app}/views/__init__.py', 'w') as file:
				file.write('')
			fixed.append(app)
		else:
			skipped.append(app)

	if len(fixed) > 0:
		result.append(f'''Views for app{'s' if len(fixed) > 1 else ''} {', '.join(fixed)} fixed.''')

	if len(skipped) > 0:
		result.append(f'''Views for app{'s' if len(skipped) > 1 else ''} {', '.join(skipped)} skipped.''')

	return result


def fix_models():
	fixed = []
	skipped = []
	result = []
	apps = unu.utils.django.helper.context.get_apps()

	for app in apps:
		if os.path.isfile(f'{settings.UNU_PROJECT_ROOT}/{app}/models.py') and not os.path.isdir(f'{settings.UNU_PROJECT_ROOT}/{app}/models'):
			os.remove(f'{settings.UNU_PROJECT_ROOT}/{app}/models.py')
			os.mkdir(f'{settings.UNU_PROJECT_ROOT}/{app}/models')
			with open(f'{settings.UNU_PROJECT_ROOT}/{app}/models/__init__.py', 'w') as file:
				file.write('')
			fixed.append(app)
		else:
			skipped.append(app)

	if len(fixed) > 0:
		result.append(f'''Models for app{'s' if len(fixed) > 1 else ''} {', '.join(fixed)} fixed.''')

	if len(skipped) > 0:
		result.append(f'''Models for app{'s' if len(skipped) > 1 else ''} {', '.join(skipped)} skipped.''')

	for app in apps:
		models_folder = f'{settings.UNU_PROJECT_ROOT}/{app}/models'

		if not os.path.isdir(models_folder):
			continue

		file_names = {}
		for file in os.listdir(models_folder):
			if file.endswith('.py') and '__init__.py' not in file:
				classes = []
				with open(f'{models_folder}/{file}') as form_file:
					for line in form_file.readlines():
						if line.startswith('class '):
							classes.append(line.split('(')[0].replace('class ', ''))
				file_names[file.replace('.py', '')] = classes

		with open(f'{models_folder}/__init__.py', 'w') as file:
			for file_name, classes in file_names.items():
				file.write(f'''from .{file_name} import {', '.join(classes)}\n''')

			file.write('\n\n')
			file.write('__all__ = [\n')
			for file_name, classes in file_names.items():
				file.write('\t{}, \n'.format(', '.join([f'\'{name}\'' for name in classes])))
			file.write(']\n')

	result.append('Fixed imports for all models.')

	return result


def fix_urls():
	fixed = []
	skipped = []
	result = []
	apps = unu.utils.django.helper.context.get_apps()

	for app in apps:
		if not os.path.isfile(f'{settings.UNU_PROJECT_ROOT}/{app}/urls.py'):
			with open(f'{settings.UNU_PROJECT_ROOT}/{app}/urls.py', 'w') as file:
				file.write(loader.render_to_string('unu/code/helper/urls.py', {
					'app': app,
				}))
			fixed.append(app)
		else:
			skipped.append(app)

	if len(fixed) > 0:
		result.append(f'''URLs for app{'s' if len(fixed) > 1 else ''} {', '.join(fixed)} fixed.''')

	if len(skipped) > 0:
		result.append(f'''URLs for app{'s' if len(skipped) > 1 else ''} {', '.join(skipped)} skipped.''')

	return result


def fix_js_namespaces():
	fixed = []
	skipped = []
	result = []
	apps = unu.utils.django.helper.context.get_apps()

	root_namespace_path = f'''{settings.UNU_PROJECT_ROOT}/media/js/{'-'.join(part.lower() for part in settings.UNU_PROJECT_NAME.split('_'))}.js'''

	if not os.path.isfile(root_namespace_path):
		ctx = {
			'is_js_root': True,
			'js_includes': ['mavor.js', 'common.js'],
			'js_namespace': ''.join(part.capitalize() for part in settings.UNU_PROJECT_NAME.split('_'))
		}
		with open(root_namespace_path, 'w') as file:
			file.write(loader.render_to_string('unu/code/helper/namespace.js', ctx))
		fixed.append('root')
	else:
		skipped.append('root')

	for app in apps:
		namespace_folder_path = f'''{settings.UNU_PROJECT_ROOT}/media/js/{'-'.join(part.lower() for part in app.split('_'))}'''

		if not os.path.isdir(namespace_folder_path):
			result.append(f'Created folder for namespace {app}')
			os.mkdir(namespace_folder_path)

		namespace_file_path = f'''{settings.UNU_PROJECT_ROOT}/media/js/{'-'.join(part.lower() for part in app.split('_'))}/{'-'.join(part.lower() for part in app.split('_'))}.js'''

		if not os.path.isfile(namespace_file_path):
			ctx = {
				'is_js_root': False,
				'js_includes': [f'''{'-'.join(part.lower() for part in settings.UNU_PROJECT_NAME.split('_'))}.js'''],
				'js_namespace': f'''{''.join(part.capitalize() for part in settings.UNU_PROJECT_NAME.split('_'))}.{''.join(part.capitalize() for part in app.split('_'))}'''
			}

			with open(namespace_file_path, 'w') as file:
				file.write(loader.render_to_string('unu/code/helper/namespace.js', ctx))
			fixed.append(app)
		else:
			skipped.append(app)

	if len(fixed) > 0:
		result.append(f'''URLs for app{'s' if len(fixed) > 1 else ''} {', '.join(fixed)} fixed.''')

	if len(skipped) > 0:
		result.append(f'''URLs for app{'s' if len(skipped) > 1 else ''} {', '.join(skipped)} skipped.''')

	return result
