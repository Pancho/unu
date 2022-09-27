import logging
import os


from django.conf import settings


import unu


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

	for app in unu.utils.django.helper.context.get_apps():
		has_folder = os.path.isdir(f'{settings.UNU_PROJECT_ROOT}/{app}/views')
		has_file = os.path.isfile(f'{settings.UNU_PROJECT_ROOT}/{app}/views.py')

		if not has_folder and has_file:
			result.append({
				'app': app,
				'recommendation': 'views-fix',
				'text': f'App {app} still doesn\'t have views as a module. Recommending views fix.'
			})

	return result


def analyze_models():
	result = []

	for app in unu.utils.django.helper.context.get_apps():
		has_folder = os.path.isdir(f'{settings.UNU_PROJECT_ROOT}/{app}/models')
		has_file = os.path.isfile(f'{settings.UNU_PROJECT_ROOT}/{app}/models.py')

		if not has_folder and has_file:
			result.append({
				'app': app,
				'recommendation': 'models-fix',
				'text': f'App {app} still doesn\'t have models as a module. Recommending models fix.'
			})

	return result


def analyze_urls():
	result = []

	for app in unu.utils.django.helper.context.get_apps():
		has_views_folder = os.path.isdir(f'{settings.UNU_PROJECT_ROOT}/{app}/views')
		has_views_file = os.path.isfile(f'{settings.UNU_PROJECT_ROOT}/{app}/views.py')
		has_urls_file = os.path.isfile(f'{settings.UNU_PROJECT_ROOT}/{app}/urls.py')

		if (has_views_folder or has_views_file) and not has_urls_file:
			result.append({
				'app': app,
				'recommendation': 'urls-fix',
				'text': f'App {app} still doesn\'t have own urls.py file. Recommending urls fix.'
			})

	return result


def analyze_js_namespaces():
	result = []

	project_name = settings.WSGI_APPLICATION.split('.')[0]
	if not os.path.isfile(f'''{settings.UNU_FRONTEND_MEDIA_PATH}/js/{'-'.join(project_name.split('_'))}.js'''):
		result.append({
			'app': project_name,
			'recommendation': 'js-namespace-fix',
			'text': 'Project still doesn\'t have JavaScript namespaces. Recommending JS namespace fix.'
		})

	for app in unu.utils.django.helper.context.get_apps():
		js_app_name = '-'.join(app.split('_'))

		has_views_folder = os.path.isdir(f'{settings.UNU_PROJECT_ROOT}/{app}/views')
		has_views_file = os.path.isfile(f'{settings.UNU_PROJECT_ROOT}/{app}/views.py')
		has_app_js_namespace = os.path.isfile(f'{settings.UNU_FRONTEND_MEDIA_PATH}/js/{js_app_name}/{js_app_name}.js')

		if (has_views_folder or has_views_file) and not has_app_js_namespace:
			result.append({
				'app': app,
				'recommendation': 'urls-fix',
				'text': f'App {app} still doesn\'t have JavaScript namespaces. Recommending JS namespace fix.'
			})

	return result
