import logging
import os
from collections import OrderedDict


import yaml
import yamlordereddictloader
from django.conf import settings
from django.template import loader


logger = logging.getLogger(__name__)
TEMPLATE = OrderedDict([
	('closure', OrderedDict([
		('build', 'tools/closure'),
		('restart', 'always'),
		('command', 'bash -c "python app.py"'),
		('ports', ['5000:5000/tcp'])
	]))
])


def fix_list_indentation(yaml_text):
	result = ''
	for line in yaml_text.split('\n'):
		if '- ' in line:
			line = '  {}'.format(line)

		result = '{}\n{}'.format(result, line)

	return result


def get_docker_compose():
	with open('{}/docker-compose.yml'.format(settings.UNU_PROJECT_ROOT), 'r') as file:
		return file.read()


def has_closure_compiler():
	docker_compose = yaml.load(get_docker_compose(), Loader=yamlordereddictloader.Loader)
	return 'closure' in docker_compose.get('services')


def add_closure_compiler():
	if not has_closure_compiler():
		# Update the docker-compose.yml file
		docker_compose = yaml.load(get_docker_compose(), Loader=yamlordereddictloader.Loader)
		services = docker_compose.get('services')
		services.update(TEMPLATE)
		services = OrderedDict(sorted(services.items()))
		docker_compose['services'] = services
		with open('{}/docker-compose.yml'.format(settings.UNU_PROJECT_ROOT), 'w') as file:
			file.write(fix_list_indentation(yaml.dump(docker_compose, Dumper=yamlordereddictloader.Dumper, width=1024, indent=2)))

		# Ensure folders
		if not os.path.isdir('{}/tools'.format(settings.UNU_PROJECT_ROOT)):
			os.mkdir('{}/tools'.format(settings.UNU_PROJECT_ROOT))
		if not os.path.isdir('{}/tools/closure'.format(settings.UNU_PROJECT_ROOT)):
			os.mkdir('{}/tools/closure'.format(settings.UNU_PROJECT_ROOT))

		# Render the template files
		with open('{}/tools/closure/Dockerfile'.format(settings.UNU_PROJECT_ROOT), 'w') as file:
			file.write(loader.render_to_string('unu/code/closure/Dockerfile', {}))

		with open('{}/tools/closure/app.py'.format(settings.UNU_PROJECT_ROOT), 'w') as file:
			file.write(loader.render_to_string('unu/code/closure/app.py', {}))


