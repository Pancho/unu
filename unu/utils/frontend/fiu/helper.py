import logging
import os


from django.conf import settings
from django.template import loader


logger = logging.getLogger(__name__)


def create_fiu_index(
		app_name,
		router_root_url,
		index_page,
		not_found_page,
		routes,
		authentication_class,
		providers,
		root_stylesheets,
		http_endpoint_stub,
		on_app_ready,
		logger_config,
		imports,
):
	log = []

	if root_stylesheets is None:
		log.append('Using default root stylesheets')
		root_stylesheets = [
			'/{}fiu/css/meta'.format(settings.UNU_FRONTEND_MEDIA_PATH),
			'/{}fiu/css/normalize'.format(settings.UNU_FRONTEND_MEDIA_PATH),
		]
	else:
		log.append('Using supplied root stylesheets')

	app_name = ''.join([part.capitalize() for part in app_name.split(' ')])
	app_path = '-'.join([part.lower() for part in app_name.split(' ')])
	log.append('Extracted app name and path')

	context = {
		'router_root_url': router_root_url,
		'http_endpoint_stub': http_endpoint_stub,
		'index_page': index_page,
		'not_found_page': not_found_page,
		'app_name': app_name,
		'authentication_class': authentication_class,
		'root_stylesheets': root_stylesheets,
		'routes': routes,
		'on_app_ready': on_app_ready,
		'providers': providers,
		'logger_config': logger_config,
		'imports': imports,
	}

	target_file_name = '{}{}/index.js'.format(settings.UNU_FRONTEND_MEDIA_PATH, app_path)
	target_folder_name = '/'.join(target_file_name.split('/')[:-1])
	if not os.path.exists(target_folder_name):
		os.makedirs(target_folder_name)

	with open(target_file_name, 'w') as file:
		file.write(loader.render_to_string('unu/code/fiu/index.js', context))

	log.append('Index file for the app "{}" is now updated'.format(app_name))
	return log


def create_fiu_component(
		component_name,
		app_name,
		media_path,
		use_store,
		enable_logging,
		include_stylesheet,
):
	return assemble_fiu_component(
		'components',
		component_name,
		app_name,
		media_path,
		use_store,
		enable_logging,
		[],
		include_stylesheet,
	)


def create_fiu_page(
		page_name,
		app_name,
		media_path,
		provide_store,
		enable_logging,
		params,
		include_stylesheet,
):
	return assemble_fiu_component(
		'pages',
		page_name,
		app_name,
		media_path,
		provide_store,
		enable_logging,
		params,
		include_stylesheet,
	)


def assemble_fiu_component(
		component_type,
		component_name,
		app_name,
		media_path,
		provide_store,
		enable_logging,
		params,
		include_stylesheet,
):
	log = []

	component_name_suffix = 'Page' if component_type == 'pages' else ''
	log_entity = 'page component' if component_type == 'pages' else 'component'

	log.append('Creating new {}'.format(log_entity))

	component_name = component_name.lower()
	component_name = component_name.replace('page', '')
	component_name = component_name.replace('component', '')
	component_name = component_name.strip()
	class_name = '{}{}Component'.format(
		''.join([part.capitalize() for part in component_name.split(' ')]),
		component_name_suffix,
	)
	log.append('New {} class name: {}'.format(log_entity, class_name))

	path_stub = '-'.join([part.lower() for part in component_name.split(' ')])
	component_path = '{}/{}'.format(path_stub, path_stub)
	app_path = '-'.join([part.lower() for part in app_name.split(' ')])
	log.append('{} paths assembled'.format(log_entity.capitalize()))

	tag_name = '{}-{}'.format(app_path, path_stub)
	log.append('{} tag name: {}'.format(log_entity.capitalize(), tag_name))

	component_folder = '{}{}/{}/{}'.format(media_path, app_path, component_type, path_stub)
	component_js = '{}/{}.js'.format(component_folder, path_stub)
	component_html = '{}/{}.html'.format(component_folder, path_stub)
	component_css = '{}/{}.css'.format(component_folder, path_stub)
	log.append('{} file paths created'.format(log_entity.capitalize()))

	context = {
		'class_name': class_name,
		'tag_name': tag_name,
		'media_path': media_path,
		'app_path': app_path,
		'path_stub': path_stub,
		'component_path': component_path,
		'component_type': component_type,
		'provide_store': provide_store,
		'enable_logging': enable_logging,
		'params': ', '.join(params),
	}

	if not os.path.exists(component_folder):
		os.makedirs(component_folder)

	with open(component_js, 'w') as file:
		file.write(loader.render_to_string('unu/code/fiu/component.js', context))
		log.append('{} js (class) file created'.format(log_entity.capitalize()))

	with open(component_html, 'w') as file:
		file.write(loader.render_to_string('unu/code/fiu/component.html', context))
		log.append('{} html file created'.format(log_entity.capitalize()))

	if include_stylesheet:
		with open(component_css, 'w') as file:
			file.write(loader.render_to_string('unu/code/fiu/component.css', context))
			log.append('{} css file created'.format(log_entity.capitalize()))

	return class_name, '/{}/{}.js'.format(
			component_type,
			component_path,
		), log
