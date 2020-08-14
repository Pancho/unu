import os
import hashlib
import logging


import requests
from django.conf import settings


from unu import utils


logger = logging.getLogger(__name__)


def update_file(file_name):
	utils.frontend.optimization.common.update_file(file_name, 'js', minify)


def optimize(js):
	success = True

	if not os.path.exists('/cache/') and settings.UNU_CLOSURE_CACHE == 'true':
		os.mkdir('/cache/')

	js_md5 = hashlib.md5(js.encode('utf-8')).hexdigest()
	if os.path.exists('/cache/{}'.format(js_md5)):
		with open('/cache/{}'.format(js_md5), 'r') as file:
			optimized_js = file.read()
	else:
		endpoint = settings.UNU_CLOSURE_ENDPOINT
		headers = {
			'Content-type': 'application/x-www-form-urlencoded',
		}
		params = {
			'js_code': js,
			'compilation_level': 'ADVANCED_OPTIMIZATIONS',
			'output_format': 'json',
			'output_info': 'compiled_code',
		}

		logger.info('Fetching optimized code from endpoint {}'.format(settings.UNU_CLOSURE_ENDPOINT))
		result = requests.post(endpoint, params, headers=headers).json()
		logger.info('Optimized code arrived, saving.')
		optimized_js = result.get('compiledCode')

		if len(result.get('errors')) > 0:
			success = False
			logger.error(result.get('errors'))

		if settings.UNU_CLOSURE_CACHE == 'true':
			with open('/cache/{}'.format(js_md5), 'w') as file:
				file.write(optimized_js)

	return optimized_js, success


def minify(js):
	return os.linesep.join(
		[
			s for s in
			'\'use strict\';{}'.format(js.replace('"use strict";', '').replace('\'use strict\';', '')).splitlines()
			if s.strip() != ''
		]
	)
