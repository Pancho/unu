import io
import logging
import os
import zipfile

import requests
from django.conf import settings

import unu


logger = logging.getLogger(__name__)


def get_fiu_files():
	response = requests.get(settings.UNU_FIU_LOCATION, stream=True)
	zip_file = zipfile.ZipFile(io.BytesIO(response.content))
	for zip_info in zip_file.filelist:
		if zip_info.filename.endswith('.js') or zip_info.filename.endswith('.css'):
			target_file_name = '{}fiu/{}'.format(
				settings.UNU_FRONTEND_MEDIA_PATH,
				zip_info.filename.split('fiu/')[1]
			)
			target_folder_name = '/'.join(target_file_name.split('/')[:-1])
			if not os.path.exists(target_folder_name):
				os.makedirs(target_folder_name)

			with open(target_file_name, 'w') as target_file:
				target_file.write(zip_file.read(zip_info.filename).decode())


def create_fiu_app(app_name, router_root_url, http_endpoint_stub, enable_logging):
	log = []

	if app_name in ['css', 'dist', 'fiu', 'img', 'js', 'webfonts']:
		log.append('Appending "-app" to the app\'s name, since it\'s using a reserved word as a name')
		app_name = '{} app'.format(app_name)

	index_page_class, index_page_path, index_page_log = unu.utils.frontend.fiu.helper.create_fiu_page(
		'index',
		app_name,
		settings.UNU_FRONTEND_MEDIA_PATH,
		False,
		enable_logging,
		[],
		True,
	)
	log.extend(index_page_log)

	not_found_page_class, not_found_page_path, not_found_page_log = unu.utils.frontend.fiu.helper.create_fiu_page(
		'not found',
		app_name,
		settings.UNU_FRONTEND_MEDIA_PATH,
		False,
		enable_logging,
		[],
		True,
	)
	log.extend(not_found_page_log)

	create_kwargs = {
		'app_name': app_name,
		'router_root_url': router_root_url,
		'index_page': index_page_class,
		'not_found_page': not_found_page_class,
		'routes': [],
		'root_stylesheets': [
			'/{}fiu/css/meta'.format(settings.UNU_FRONTEND_MEDIA_PATH),
			'/{}fiu/css/normalize'.format(settings.UNU_FRONTEND_MEDIA_PATH),
		],
		'authentication_class': None,
		'http_endpoint_stub': http_endpoint_stub,
		'on_app_ready': None,
		'providers': [],
		'logger_config': 'level: LogLevels.TRACE,' if enable_logging else '',
		'imports': {
			index_page_class: index_page_path,
			not_found_page_class: not_found_page_path,
		},
	}

	index_log = unu.utils.frontend.fiu.helper.create_fiu_index(**create_kwargs)
	log.extend(index_log)

	return log


def create_fiu_component(component_name, use_store, include_stylesheet):
	log = []

	app_data = unu.utils.frontend.fiu.analyze.get_fiu_app_data()
	index = app_data.get('index')
	app_name = index.get('app_name')
	enable_logging = index.get('logger_config') is not None

	component_class, component_path, component_log = unu.utils.frontend.fiu.helper.create_fiu_component(
		component_name,
		app_name,
		settings.UNU_FRONTEND_MEDIA_PATH,
		use_store,
		enable_logging,
		include_stylesheet,
	)
	log.extend(component_log)

	return log


def create_fiu_page(component_name, url_pattern, use_store):
	log = []

	app_data = unu.utils.frontend.fiu.analyze.get_fiu_app_data()
	index = app_data.get('index')
	app_name = index.get('app_name')
	enable_logging = index.get('logger_config') is not None
	params = [param.replace(':', '') for param in url_pattern.split('/') if param.startswith(':')]

	page_class, page_path, page_log = unu.utils.frontend.fiu.helper.create_fiu_page(
		component_name,
		app_name,
		settings.UNU_FRONTEND_MEDIA_PATH,
		use_store,
		enable_logging,
		params,
		True,
	)
	log.extend(page_log)

	index['routes'].append({
		'class_name': page_class,
		'path': url_pattern,
	})
	log.append('Added route {}'.format({
		'class_name': page_class,
		'path': url_pattern,
	}))
	if use_store:
		index['providers'].append('{}.STORE_PROVIDER'.format(page_class))
		log.append('Adding provider {}.STORE_PROVIDER'.format(page_class))
	index['imports'].update({
		page_class: page_path,
	})
	log.append('Adding import {}:{}'.format(
		page_class,
		page_path,
	))

	index_log = unu.utils.frontend.fiu.helper.create_fiu_index(**index)
	log.extend(index_log)

	return log
