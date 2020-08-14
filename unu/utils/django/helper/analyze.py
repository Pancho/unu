import logging
import os


from django.conf import settings


from unu import utils


logger = logging.getLogger(__name__)


def analyze():
	result = []

	result.extend(analyze_views())
	result.extend(analyze_models())
	result.extend(analyze_urls())
	result.extend(analyze_js_namespaces())

	if len(result) == 0:
		result.append({
			'app': 'Project',
			'recommendation': None,
			'text': 'Everything seems to be in order.'
		})

	return result


def analyze_views():
	result = []

	for app in utils.django.helper.context.get_apps():
		has_folder = os.path.isdir('{}/{}/{}'.format(settings.UNU_PROJECT_ROOT, app, 'views'))
		has_file = os.path.isfile('{}/{}/{}.py'.format(settings.UNU_PROJECT_ROOT, app, 'views'))

		if not has_folder and has_file:
			result.append({
				'app': app,
				'recommendation': 'views-fix',
				'text': 'App {} still doesn\'t have views as a module. Recommending views fix.'.format(app)
			})

	return result


def analyze_models():
	result = []

	for app in utils.django.helper.context.get_apps():
		has_folder = os.path.isdir('{}/{}/{}'.format(settings.UNU_PROJECT_ROOT, app, 'models'))
		has_file = os.path.isfile('{}/{}/{}.py'.format(settings.UNU_PROJECT_ROOT, app, 'models'))

		if not has_folder and has_file:
			result.append({
				'app': app,
				'recommendation': 'models-fix',
				'text': 'App {} still doesn\'t have models as a module. Recommending models fix.'.format(app)
			})

	return result


def analyze_urls():
	result = []

	for app in utils.django.helper.context.get_apps():
		has_views_folder = os.path.isdir('{}/{}/{}'.format(settings.UNU_PROJECT_ROOT, app, 'views'))
		has_views_file = os.path.isfile('{}/{}/{}.py'.format(settings.UNU_PROJECT_ROOT, app, 'views'))
		has_urls_file = os.path.isfile('{}/{}/{}'.format(settings.UNU_PROJECT_ROOT, app, 'urls.py'))

		if (has_views_folder or has_views_file) and not has_urls_file:
			result.append({
				'app': app,
				'recommendation': 'urls-fix',
				'text': 'App {} still doesn\'t have own urls.py file. Recommending urls fix.'.format(app)
			})

	return result


def analyze_js_namespaces():
	result = []

	project_name = settings.WSGI_APPLICATION.split('.')[0]
	if not os.path.isfile('{}/js/{}.js'.format(settings.UNU_FRONTEND_MEDIA_PATH, '-'.join(project_name.split('_')))):
		result.append({
			'app': project_name,
			'recommendation': 'js-namespace-fix',
			'text': 'Project still doesn\'t have JavaScript namespaces. Recommending JS namespace fix.'
		})

	for app in utils.django.helper.context.get_apps():
		js_app_name = '-'.join(app.split('_'))

		has_views_folder = os.path.isdir('{}/{}/{}'.format(settings.UNU_PROJECT_ROOT, app, 'views'))
		has_views_file = os.path.isfile('{}/{}/{}.py'.format(settings.UNU_PROJECT_ROOT, app, 'views'))
		has_app_js_namespace = os.path.isfile('{}/js/{}/{}.js'.format(settings.UNU_FRONTEND_MEDIA_PATH, js_app_name, js_app_name))

		if (has_views_folder or has_views_file) and not has_app_js_namespace:
			result.append({
				'app': app,
				'recommendation': 'urls-fix',
				'text': 'App {} still doesn\'t have JavaScript namespaces. Recommending JS namespace fix.'.format(app)
			})

	return result
