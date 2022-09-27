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
		authentication_url,
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
			f'/{settings.UNU_FRONTEND_MEDIA_PATH}fiu/css/meta',
			f'/{settings.UNU_FRONTEND_MEDIA_PATH}fiu/css/normalize',
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
		'authentication_url': authentication_url,
		'authentication_class': authentication_class,
		'root_stylesheets': root_stylesheets,
		'routes': routes,
		'on_app_ready': on_app_ready,
		'providers': providers,
		'logger_config': logger_config,
		'imports': imports,
	}

	target_file_name = f'{settings.UNU_FRONTEND_MEDIA_PATH}{app_path}/index.js'
	target_folder_name = '/'.join(target_file_name.split('/')[:-1])
	if not os.path.exists(target_folder_name):
		os.makedirs(target_folder_name)

	with open(target_file_name, 'w') as file:
		file.write(loader.render_to_string('unu/code/fiu/index.js', context))

	log.append(f'Index file for the app "{app_name}" is now updated')
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

	log.append(f'Creating new {log_entity}')

	component_name = component_name.lower()
	component_name = component_name.replace('page', '')
	component_name = component_name.replace('component', '')
	component_name = component_name.strip()
	class_name = f'''{''.join([part.capitalize() for part in component_name.split(' ')])}{component_name_suffix}Component'''
	log.append(f'New {log_entity} class name: {class_name}')

	path_stub = '-'.join([part.lower() for part in component_name.split(' ')])
	component_path = f'{path_stub}/{path_stub}'
	app_path = '-'.join([part.lower() for part in app_name.split(' ')])
	log.append(f'{log_entity.capitalize()} paths assembled')

	tag_name = f'{app_path}-{path_stub}'
	log.append(f'{log_entity.capitalize()} tag name: {tag_name}')

	component_folder = f'{media_path}{app_path}/{component_type}/{path_stub}'
	component_js = f'{component_folder}/{path_stub}.js'
	component_html = f'{component_folder}/{path_stub}.html'
	component_css = f'{component_folder}/{path_stub}.css'
	log.append(f'{log_entity.capitalize()} file paths created')

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
		'include_stylesheet': include_stylesheet,
	}

	if not os.path.exists(component_folder):
		os.makedirs(component_folder)

	with open(component_js, 'w') as file:
		file.write(loader.render_to_string('unu/code/fiu/component.js', context))
		log.append(f'{log_entity.capitalize()} js (class) file created')

	with open(component_html, 'w') as file:
		file.write(loader.render_to_string('unu/code/fiu/component.html', context))
		log.append(f'{log_entity.capitalize()} html file created')

	if include_stylesheet:
		with open(component_css, 'w') as file:
			file.write(loader.render_to_string('unu/code/fiu/component.css', context))
			log.append(f'{log_entity.capitalize()} css file created')

	return class_name, f'/{component_type}/{component_path}.js', log
