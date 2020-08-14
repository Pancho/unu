import os
import logging


from django.conf import settings
from django.template import loader


from unu import utils


logger = logging.getLogger(__name__)


def fix_views():
	fixed = []
	skipped = []
	result = []
	apps = utils.django.helper.context.get_apps()

	for app in apps:
		if os.path.isfile('{}/{}/views.py'.format(settings.UNU_PROJECT_ROOT, app)) and not os.path.isdir('{}/{}/views'.format(settings.UNU_PROJECT_ROOT, app)):
			os.remove('{}/{}/views.py'.format(settings.UNU_PROJECT_ROOT, app))
			os.mkdir('{}/{}/views'.format(settings.UNU_PROJECT_ROOT, app))
			with open('{}/{}/views/__init__.py'.format(settings.UNU_PROJECT_ROOT, app), 'w') as file:
				file.write('')
			fixed.append(app)
		else:
			skipped.append(app)

	if len(fixed) > 0:
		result.append('Views for app{} {} fixed.'.format('s' if len(fixed) > 1 else '', ', '.join(fixed)))

	if len(skipped) > 0:
		result.append('Views for app{} {} skipped'.format('s' if len(skipped) > 1 else '', ', '.join(skipped)))

	return result


def fix_models():
	fixed = []
	skipped = []
	result = []
	apps = utils.django.helper.context.get_apps()

	for app in apps:
		if os.path.isfile('{}/{}/models.py'.format(settings.UNU_PROJECT_ROOT, app)) and not os.path.isdir('{}/models'.format(settings.UNU_PROJECT_ROOT, app)):
			os.remove('{}/{}/models.py'.format(settings.UNU_PROJECT_ROOT, app))
			os.mkdir('{}/{}/models'.format(settings.UNU_PROJECT_ROOT, app))
			with open('{}/{}/models/__init__.py'.format(settings.UNU_PROJECT_ROOT, app), 'w') as file:
				file.write('')
			fixed.append(app)
		else:
			skipped.append(app)

	if len(fixed) > 0:
		result.append('Models for app{} {} fixed.'.format('s' if len(fixed) > 1 else '', ', '.join(fixed)))

	if len(skipped) > 0:
		result.append('Models for app{} {} skipped'.format('s' if len(skipped) > 1 else '', ', '.join(skipped)))

	for app in apps:
		models_folder = '{}/{}/models'.format(
			settings.UNU_PROJECT_ROOT,
			app
		)

		if not os.path.isdir(models_folder):
			continue

		file_names = {}
		for file in os.listdir(models_folder):
			if file.endswith('.py') and '__init__.py' not in file:
				classes = []
				with open('{}/{}'.format(models_folder, file)) as form_file:
					for line in form_file.readlines():
						if line.startswith('class '):
							classes.append(line.split('(')[0].replace('class ', ''))
				file_names[file.replace('.py', '')] = classes

		with open('{}/__init__.py'.format(models_folder), 'w') as file:
			for file_name, classes in file_names.items():
				file.write('from .{} import {}\n'.format(file_name, ', '.join(classes)))

			file.write('\n\n')
			file.write('__all__ = [\n')
			for file_name, classes in file_names.items():
				file.write('\t{}, \n'.format(', '.join(['\'{}\''.format(name) for name in classes])))
			file.write(']\n')

	result.append('Fixed imports for all models.')

	return result


def fix_urls():
	fixed = []
	skipped = []
	result = []
	apps = utils.django.helper.context.get_apps()

	for app in apps:
		if not os.path.isfile('{}/{}/urls.py'.format(settings.UNU_PROJECT_ROOT, app)):
			with open('{}/{}/urls.py'.format(settings.UNU_PROJECT_ROOT, app), 'w') as file:
				file.write(loader.render_to_string('unu/code/helper/urls.py', {
					'app': app,
				}))
			fixed.append(app)
		else:
			skipped.append(app)

	if len(fixed) > 0:
		result.append('URLs for app{} {} fixed.'.format('s' if len(fixed) > 1 else '', ', '.join(fixed)))

	if len(skipped) > 0:
		result.append('URLs for app{} {} skipped'.format('s' if len(skipped) > 1 else '', ', '.join(skipped)))

	return result


def fix_js_namespaces():
	fixed = []
	skipped = []
	result = []
	apps = utils.django.helper.context.get_apps()

	root_namespace_path = '{}/media/js/{}.js'.format(
		settings.UNU_PROJECT_ROOT,
		'-'.join(part.lower() for part in settings.UNU_PROJECT_NAME.split('_'))
	)

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
		namespace_folder_path = '{}/media/js/{}'.format(
			settings.UNU_PROJECT_ROOT,
			'-'.join(part.lower() for part in app.split('_')),
		)

		if not os.path.isdir(namespace_folder_path):
			result.append('Created folder for namespace {}'.format(app))
			os.mkdir(namespace_folder_path)

		namespace_file_path = '{}/media/js/{}/{}.js'.format(
			settings.UNU_PROJECT_ROOT,
			'-'.join(part.lower() for part in app.split('_')),
			'-'.join(part.lower() for part in app.split('_'))
		)

		if not os.path.isfile(namespace_file_path):
			ctx = {
				'is_js_root': False,
				'js_includes': ['{}.js'.format('-'.join(part.lower() for part in settings.UNU_PROJECT_NAME.split('_')))],
				'js_namespace': '{}.{}'.format(
					''.join(part.capitalize() for part in settings.UNU_PROJECT_NAME.split('_')),
					''.join(part.capitalize() for part in app.split('_'))
				)
			}

			with open(namespace_file_path, 'w') as file:
				file.write(loader.render_to_string('unu/code/helper/namespace.js', ctx))
			fixed.append(app)
		else:
			skipped.append(app)

	if len(fixed) > 0:
		result.append('URLs for app{} {} fixed.'.format('s' if len(fixed) > 1 else '', ', '.join(fixed)))

	if len(skipped) > 0:
		result.append('URLs for app{} {} skipped'.format('s' if len(skipped) > 1 else '', ', '.join(skipped)))

	return result
