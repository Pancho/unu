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
			line = f'  {line}'

		result = f'{result}\n{line}'

	return result


def get_docker_compose():
	with open(f'{settings.UNU_PROJECT_ROOT}/docker-compose.yml', 'r') as file:
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
		with open(f'{settings.UNU_PROJECT_ROOT}/docker-compose.yml', 'w') as file:
			file.write(fix_list_indentation(yaml.dump(docker_compose, Dumper=yamlordereddictloader.Dumper, width=1024, indent=2)))

		# Ensure folders
		if not os.path.isdir(f'{settings.UNU_PROJECT_ROOT}/tools'):
			os.mkdir(f'{settings.UNU_PROJECT_ROOT}/tools')
		if not os.path.isdir(f'{settings.UNU_PROJECT_ROOT}/tools/closure'):
			os.mkdir(f'{settings.UNU_PROJECT_ROOT}/tools/closure')

		# Render the template files
		with open(f'{settings.UNU_PROJECT_ROOT}/tools/closure/Dockerfile', 'w') as file:
			file.write(loader.render_to_string('unu/code/closure/Dockerfile', {}))

		with open(f'{settings.UNU_PROJECT_ROOT}/tools/closure/app.py', 'w') as file:
			file.write(loader.render_to_string('unu/code/closure/app.py', {}))


