import logging
import os
import re

from django.conf import settings


logger = logging.getLogger(__name__)
FIU_APP_IMPORT = re.compile(r'(import {)(.*?)(} from \'.)(.*?)(\';)')
FIU_APP_ROUTER_ROOT_URL = re.compile(r'(routeRoot: \')(.*?)(\',)')
FIU_APP_STATIC_ROOT_URL = re.compile(r'(staticRoot: \')(.*?)(\',)')
FIU_APP_INDEX_PAGE = re.compile(r'(homePage: {\s)(.*?\s)(\s},)')
FIU_APP_NOT_FOUND_PAGE = re.compile(r'(notFound: {\s)(.*?\s)(\s},)')
FIU_APP_ROUTES = re.compile(r'(routes: \[)((.*?\s)*?)(\],)')
FIU_APP_ROUTES_INNER = re.compile(r'(\n\s*?)({.+?\1})', re.M | re.S)
FIU_APP_COMPONENT_ENTRY = re.compile(r'(component: )(.*)(,*)')
FIU_APP_PATH_ENTRY = re.compile(r'(path: \')(.*)(\',*)')
FIU_APP_GUARD_ENTRY = re.compile(r'(guard: )(.*)(,*)')
FIU_APP_HOOKS_ENTRY = re.compile(r'(hooks: )((.*?\s)*?})')
FIU_APP_ROOT_STYLESHEETS = re.compile(r'(rootStylesheets: \[\s)((.*?\s)*?)(\])')
FIU_APP_AUTHENTICATION_MODULE = re.compile(r'(authenticationModule: )(.*?)(,)')
FIU_APP_AUTHENTICATION_URL = re.compile(r'(authenticationUrl: \')(.*)(\',*)')
FIU_APP_HTTP_ENDPOINT_STUB = re.compile(r'(httpEndpointStub: \')(.*?)(\',)')
FIU_APP_ON_APP_READY = re.compile(r'(onAppReady: \[\n+?\s+)(.*?)(\n\s\],)', re.M | re.S)
FIU_APP_PROVIDERS = re.compile(r'(providers: \[)(.*?)(])', re.M | re.S)
FIU_APP_LOGGER_CONFIG = re.compile(r'(loggerConfig: {\n+?\s+)(.*?)(\n\s},)', re.M | re.S)


def has_fiu():
	return os.path.isdir(f'{settings.UNU_FRONTEND_MEDIA_PATH}fiu')


def has_fiu_app():
	for folder in os.listdir(settings.UNU_FRONTEND_MEDIA_PATH):
		index_file_path = f'{settings.UNU_FRONTEND_MEDIA_PATH}{folder}/index.js'
		if os.path.exists(index_file_path):
			return True
	return False


def get_fiu_apps():
	apps = []

	for folder in os.listdir(settings.UNU_FRONTEND_MEDIA_PATH):
		index_file_path = f'{settings.UNU_FRONTEND_MEDIA_PATH}{folder}/index.js'
		if os.path.exists(index_file_path):
			apps.append(folder)

	return apps


def get_fiu_app_data(app_folder):
	if not has_fiu_app():
		return {}

	app_file = ''
	index_file_contents = ''
	index_file_path = f'{settings.UNU_FRONTEND_MEDIA_PATH}{app_folder}/index.js'

	if os.path.exists(index_file_path):
		with open(index_file_path, 'r') as index_file:
			index_file_contents = index_file.read()
			app_file = index_file_path

	pages = []
	pages_folder = f'{settings.UNU_FRONTEND_MEDIA_PATH}{app_folder}/pages'
	components = []
	components_folder = f'{settings.UNU_FRONTEND_MEDIA_PATH}{app_folder}/components'

	if os.path.exists(pages_folder):
		for folder in os.listdir(pages_folder):
			pages.append(folder)

	if os.path.exists(components_folder):
		for folder in os.listdir(components_folder):
			components.append(folder)

	index = parse_index(index_file_contents)
	return {
		'index': index,
		'app_file': app_file,
		'app_folder': app_folder,
		'page_folders': pages,
		'component_folders': components,
	}


def parse_index(index_file_contents):
	router_root_url = parse_router_root_url(index_file_contents)
	static_root_url = parse_static_root_url(index_file_contents)
	index_page = parse_index_page(index_file_contents)
	not_found_page = parse_not_found_page(index_file_contents)
	routes, routes_imports = parse_routes(index_file_contents)
	root_stylesheets = parse_root_stylesheets(index_file_contents)
	authentication_url = parse_authentication_url(index_file_contents)
	authentication_module = parse_authentication_module(index_file_contents)
	http_endpoint_stub = parse_http_endpoint_stub(index_file_contents)
	on_app_ready = parse_on_app_ready(index_file_contents)
	providers = parse_providers(index_file_contents)
	logger_config = parse_logger_config(index_file_contents)

	return {
		'router_root_url': router_root_url,
		'static_root_url': static_root_url,
		'index_page': index_page,
		'not_found_page': not_found_page,
		'routes': routes,
		'root_stylesheets': root_stylesheets,
		'authentication_url': authentication_url,
		'authentication_module': authentication_module,
		'http_endpoint_stub': http_endpoint_stub,
		'on_app_ready': on_app_ready,
		'providers': providers,
		'logger_config': logger_config,
	}


def parse_router_root_url(index_file_contents):
	match = FIU_APP_ROUTER_ROOT_URL.search(index_file_contents)
	if match is not None:
		return match.group(2).strip()


def parse_static_root_url(index_file_contents):
	match = FIU_APP_STATIC_ROOT_URL.search(index_file_contents)
	if match is not None:
		return match.group(2).strip()


def parse_index_page(index_file_contents):
	match = FIU_APP_INDEX_PAGE.search(index_file_contents)

	if match is not None:
		for line in match.group(2).split(','):
			if line.strip() == '':
				continue
			component_match = FIU_APP_COMPONENT_ENTRY.search(line)
			class_name = component_match.group(2).strip()
			return class_name


def parse_not_found_page(index_file_contents):
	match = FIU_APP_NOT_FOUND_PAGE.search(index_file_contents)

	if match is not None:
		for line in match.group(2).split(','):
			if line.strip() == '':
				continue
			component_match = FIU_APP_COMPONENT_ENTRY.search(line)
			class_name = component_match.group(2).strip()
			return class_name


def parse_routes(index_file_contents):
	result = []
	imports = set()

	match = FIU_APP_ROUTES.search(index_file_contents)

	if match is not None:
		for blob in FIU_APP_ROUTES_INNER.split(match.group(2)):
			if blob.strip() == ',' or blob.strip() == '':
				continue
			component_match = FIU_APP_COMPONENT_ENTRY.search(blob)
			path_match = FIU_APP_PATH_ENTRY.search(blob)
			guard_match = FIU_APP_GUARD_ENTRY.search(blob)
			hooks_match = FIU_APP_HOOKS_ENTRY.search(blob)
			class_name = component_match.group(2).replace(',', '').strip()
			path = path_match.group(2).replace(',', '').strip()
			guard = ''
			if guard_match is not None:
				guard = guard_match.group(2).replace(',', '').strip()
			hooks = ''
			if hooks_match is not None:
				hooks = hooks_match.group(2)  # This one we leave as-is
			result.append({
				'class_name': class_name,
				'path': path,
				'guard': guard,
				'hooks': hooks,
			})
			imports.add(class_name)
			if guard != '':
				imports.add(guard)

	return result, imports


def parse_root_stylesheets(index_file_contents):
	result = []

	match = FIU_APP_ROOT_STYLESHEETS.search(index_file_contents)

	if match is not None:
		for stylesheet_import in match.group(2).split(','):
			if stylesheet_import.strip() == '':
				continue
			result.append(stylesheet_import.strip().replace('\'', ''))

	return result


def parse_authentication_url(index_file_contents):
	match = FIU_APP_AUTHENTICATION_URL.search(index_file_contents)
	if match is not None:
		class_name = match.group(2).strip()
		return class_name


def parse_authentication_module(index_file_contents):
	match = FIU_APP_AUTHENTICATION_MODULE.search(index_file_contents)
	if match is not None:
		class_name = match.group(2).strip()
		return class_name


def parse_http_endpoint_stub(index_file_contents):
	match = FIU_APP_HTTP_ENDPOINT_STUB.search(index_file_contents)
	if match is not None:
		return match.group(2).strip()


def parse_on_app_ready(index_file_contents):
	match = FIU_APP_ON_APP_READY.search(index_file_contents)
	if match is not None:
		return match.group(2).strip()


def parse_providers(index_file_contents):
	result = []

	match = FIU_APP_PROVIDERS.search(index_file_contents)

	if match is not None:
		for stylesheet_import in match.group(2).split(','):
			if stylesheet_import.strip() == '':
				continue
			result.append(stylesheet_import.strip())

	return result


def parse_logger_config(index_file_contents):
	match = FIU_APP_LOGGER_CONFIG.search(index_file_contents)
	if match is not None:
		return match.group(2).strip()
