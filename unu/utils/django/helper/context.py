import inspect
import logging
import os
import sys


from django.conf import settings


logger = logging.getLogger(__name__)


def has_models(app):
	return os.path.isdir('{}/{}/models'.format(settings.UNU_PROJECT_ROOT, app))


def get_apps(with_models=False):
	apps = []

	for folder in os.listdir(path=settings.UNU_PROJECT_ROOT):
		if os.path.isdir(folder) and os.path.isfile('{}/apps.py'.format(folder)):
			with open('{}/apps.py'.format(folder)) as file:
				contents = file.read()

				if 'name = ' in contents:
					app = contents.split('name = \'')[1].split('\'')[0]
					if with_models:
						if has_models(app):
							apps.append(app)
					else:
						apps.append(app)

	return apps


def get_models(app):
	return [name for name, obj in inspect.getmembers(sys.modules['{}.models'.format(app)]) if inspect.isclass(obj)]
