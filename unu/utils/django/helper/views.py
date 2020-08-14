import collections
import logging
import os


from django.conf import settings
from django.template import loader
from django.urls import reverse_lazy
from django.utils import text


logger = logging.getLogger(__name__)


def fix_views_imports(context):
	log = []

	app = context.get('app')
	log.append('Fixing imports for views in app {}'.format(app))
	if os.path.isdir('{}/{}/views'.format(settings.UNU_PROJECT_ROOT, app)):
		file_names = []
		for file in os.listdir('{}/{}/views'.format(settings.UNU_PROJECT_ROOT, app)):
			if file.endswith('.py') and '__init__.py' not in file:
				file_names.append(file.replace('.py', ''))

		with open('{}/{}/views/__init__.py'.format(settings.UNU_PROJECT_ROOT, app), 'w') as file:
			for module_name in file_names:
				file.write('from . import {}\n'.format(module_name))
			file.write('\n\n')
			file.write('__all__ = [\n')
			for module_name in file_names:
				file.write('\t\'{}\',\n'.format(module_name))
			file.write(']\n')
	else:
		raise Exception('Folder views does not exist for the app {}. Fix the app first.'.format(app))

	log.append('Imports for views in app {} fixed.'.format(app))

	return log


def fix_forms_imports(context):
	log = []

	forms_folder = '{}/{}/forms'.format(
		settings.UNU_PROJECT_ROOT,
		context.get('app')
	)

	file_names = {}
	for file in os.listdir(forms_folder):
		if file.endswith('.py') and '__init__.py' not in file:
			classes = []
			with open('{}/{}'.format(forms_folder, file)) as form_file:
				for line in form_file.readlines():
					if line.startswith('class '):
						classes.append(line.split('(')[0].replace('class ', ''))
			file_names[file.replace('.py', '')] = classes

	with open('{}/__init__.py'.format(forms_folder), 'w') as file:
		for file_name, classes in file_names.items():
			file.write('from .{} import {}\n'.format(file_name, ', '.join(classes)))

		file.write('\n\n')
		file.write('__all__ = [\n')
		for file_name, classes in file_names.items():
			file.write('\t{}, \n'.format(', '.join(['\'{}\''.format(name) for name in classes])))
		file.write(']\n')

	log.append('Form imports fixed')

	return log


def add_file_to_views(context):
	log = []

	if not os.path.isdir('{}/{}/views'.format(settings.UNU_PROJECT_ROOT, context.get('app'))):
		raise Exception('{}/{}/views is not a folder. Fix app "{}" before you continue.'.format(
			settings.UNU_PROJECT_ROOT,
			context.get('app'),
			context.get('app')
		))

	if os.path.isfile('{}/{}/views/{}.py'.format(settings.UNU_PROJECT_ROOT, context.get('app'), context.get('view_name'))):
		raise Exception('File {}/{}/views/{}.py already exists. Will not create new view.'.format(
			settings.UNU_PROJECT_ROOT, context.get('app'),
			context.get('view_name')
		))

	log.append('Creating file for view {}'.format(context.get('view_name')))
	with open('{}/{}/views/{}.py'.format(settings.UNU_PROJECT_ROOT, context.get('app'), context.get('view_name')), 'w') as file:
		file.write(loader.render_to_string('unu/code/views/{}.py'.format(context.get('view_template')), context))

	log.append('File {}/{}/views/{}.py for view created.'.format(settings.UNU_PROJECT_ROOT, context.get('app'), context.get('view_name')))

	return log


def add_url(context):
	log = []

	app = context.get('app')
	view_name = context.get('view_name')
	kwarg_name = context.get('kwarg_name')
	kwarg_type = context.get('kwarg_type')

	log.append('Adding url for view {} in app {}'.format(view_name, app))

	with open('{}/{}/urls.py'.format(settings.UNU_PROJECT_ROOT, app), 'r') as f:
		urls_content = f.read()

	urls_split = urls_content.split(']')
	url = context.get('url')

	if kwarg_name is not None:
		url = '{}/<{}{}>'.format(
			url,
			'{}:'.format(kwarg_type) if kwarg_type is not None else '',
			kwarg_name,
		)

	url_path = '\tpath(\'{}\', views.{}.Controller.as_view(), name=\'{}\'),'.format(
		url,
		view_name,
		view_name,
	)

	with open('{}/urls.py'.format(app), 'r') as file:
		if url_path in file.read():
			raise Exception('Will not add an existing url to urls.py for app {}.'.format(app))

	with open('{}/urls.py'.format(app), 'w') as file:
		file.write('{}{}\n]\n'.format(
			urls_split[0],
			url_path,
		))

	log.append('Added new path to urls.py for app {}: {}'.format(
		app,
		url_path
	))

	return log


def add_template(context):
	log = []

	log.append('Adding template for view {}.'.format(context.get('view_name')))

	folder_path = '{}/{}/templates/{}/pages'.format(
		settings.UNU_PROJECT_ROOT,
		context.get('app'),
		context.get('app')
	)

	if not os.path.isdir(folder_path):
		log.append('Creating folder {}.'.format(folder_path))
		os.makedirs(folder_path)

	template_path = '{}/{}.html'.format(
		folder_path,
		context.get('view_name'),
	)

	if os.path.isfile(template_path):
		raise Exception('Template at {} already exists.'.format(template_path))

	with open(template_path, 'w') as file:
		file.write(loader.render_to_string('unu/code/views/generic_view.html', context))

	log.append('Template for view {} added.'.format(context.get('view_name')))

	return log


def add_static_files(context):
	log = []

	js_file_path = '{}/{}js/{}.js'.format(
		settings.UNU_PROJECT_ROOT,
		settings.UNU_FRONTEND_MEDIA_PATH,
		context.get('static_path'),
	)

	log.append('Adding JS file for view {}.'.format(context.get('view_name')))

	if os.path.isfile(js_file_path):
		raise Exception('JS at {} already exists.'.format(js_file_path))

	with open(js_file_path, 'w') as file:
		file.write(loader.render_to_string('unu/code/views/generic_view.js', context))

	log.append('JS file for view {} added.'.format(context.get('view_name')))
	log.append('Adding CSS file for view {}.'.format(context.get('view_name')))

	css_folder = '{}/{}css/{}'.format(
		settings.UNU_PROJECT_ROOT,
		settings.UNU_FRONTEND_MEDIA_PATH,
		context.get('app')
	)

	if not os.path.isdir(css_folder):
		os.mkdir(css_folder)
		log.append('Created folder {}.'.format(css_folder))

	css_file_path = '{}/{}css/{}.css'.format(
		settings.UNU_PROJECT_ROOT,
		settings.UNU_FRONTEND_MEDIA_PATH,
		context.get('static_path'),
	)

	if os.path.isfile(css_file_path):
		raise Exception('CSS at {} already exists.'.format(css_file_path))

	with open(css_file_path, 'w') as file:
		file.write(loader.render_to_string('unu/code/views/generic_view.css', context))

	log.append('CSS file for view {} added.'.format(context.get('view_name')))

	return log


def add_form(context):
	log = []

	forms_path = '{}/{}/forms'.format(
		settings.UNU_PROJECT_ROOT,
		context.get('app')
	)
	if not os.path.isdir(forms_path):
		os.mkdir(forms_path)

	form_path = '{}/{}.py'.format(
		forms_path,
		context.get('view_name')
	)
	with open(form_path, 'w') as file:
		file.write(loader.render_to_string('unu/code/views/form.py', context))

	log.append('Added form class {} to file {}.'.format(
		context.get('form'),
		forms_path
	))

	return log


HTTP_METHODS = [
	'GET',
	'POST',
	'HEAD',
	'DELETE',
	'PUT',
	'OPTIONS',
	'CONNECT',
	'TRACE',
	'PATCH',
]
KWARG_TYPES = {
	'Without Type': None,
	'str': 'str',
	'int': 'int',
	'slug': 'slug',
	'uuid': 'uuid',
	'path': 'path',
}
CONTROLLER_MIXINS = collections.OrderedDict({
	'LoginRequiredMixin': {
		'module_path': 'mixins.LoginRequiredMixin',
		'required_imports': [
			'from django.contrib.auth import mixins',
		],
	},
	'UserPassesTestMixin': {
		'module_path': 'mixins.UserPassesTestMixin',
		'required_imports': [
			'from django.contrib.auth import mixins',
		],
	},
	'PermissionRequiredMixin': {
		'module_path': 'mixins.PermissionRequiredMixin',
		'required_imports': [
			'from django.contrib.auth import mixins',
		],
	},
	'DebugOnlyMixin': {
		'module_path': 'utils.views.mixins.debug.DebugOnlyMixin',
		'required_imports': [
			'from unu import utils',
		],
	},
})
VIEW_CONFIG = {
	'fields': [
		{
			'name': 'app',
			'label': 'Django App',
			'field': 'select',
			'class': 'populate-with-apps',
			'data': {
				'get-apps-url': reverse_lazy('unu:get_apps'),
			},
			'coerce': lambda post: post.get('app'),
		},
		{
			'name': 'name',
			'label': 'View Name',
			'field': 'input',
			'class': 'live-slugify',
			'coerce': lambda post: post.get('name'),
		},
		{
			'name': 'methods',
			'label': 'HTTP Methods',
			'field': 'select-multiple',
			'options': HTTP_METHODS,
			'coerce': lambda post: post.getlist('methods')
		},
		{
			'name': 'mixins',
			'label': 'Controller mixins',
			'field': 'select-multiple',
			'options': CONTROLLER_MIXINS.keys(),
			'coerce': lambda post: post.getlist('mixins')
		}
	],
	'upgrade_context': lambda context: context.update({
		'view_template': 'view',
		'view_name': text.slugify(context.get('name')).replace('-', '_'),
		'url': text.slugify(context.get('name')),
		'http_methods': ', '.join(['\'{}\''.format(method.lower()) for method in context.get('methods')]),
		'class_extensions': ', '.join([
			CONTROLLER_MIXINS.get(mixin).get('module_path') for mixin in context.get('mixins')
		]),
		'imports': sorted(
			set().union(
				*[['from unu import utils']] + [CONTROLLER_MIXINS.get(mixin).get('required_imports') for mixin in context.get('mixins')]
			)
		),
	}),
	'process': [
		add_file_to_views,
		add_url,
		fix_views_imports,
	]
}
TEMPLATE_VIEW_CONFIG = {
	'fields': [
		{
			'name': 'app',
			'label': 'Django App',
			'field': 'select',
			'class': 'populate-with-apps',
			'data': {
				'get-apps-url': reverse_lazy('unu:get_apps'),
			},
			'coerce': lambda post: post.get('app'),
		},
		{
			'name': 'name',
			'label': 'View Name',
			'field': 'input',
			'class': 'live-slugify',
			'coerce': lambda post: post.get('name'),
		},
		{
			'name': 'mixins',
			'label': 'Controller mixins',
			'field': 'select-multiple',
			'options': CONTROLLER_MIXINS.keys(),
			'coerce': lambda post: post.getlist('mixins')
		}
	],
	'upgrade_context': lambda context: context.update({
		'view_template': 'template_view',
		'view_name': text.slugify(context.get('name')).replace('-', '_'),
		'url': text.slugify(context.get('name')),
		'class_extensions': ', '.join([
			CONTROLLER_MIXINS.get(mixin).get('module_path') for mixin in context.get('mixins')
		]),
		'imports': sorted(
			set().union(
				*[CONTROLLER_MIXINS.get(mixin).get('required_imports') for mixin in context.get('mixins')]
			)
		),
		'template_name': '{}/pages/{}.html'.format(
			context.get('app'),
			text.slugify(context.get('name')).replace('-', '_'),
		),
		'static_path': '{}/{}'.format(text.slugify(context.get('app')), text.slugify(context.get('name'))),
		'js_includes': ['{}/{}.js'.format(
			'-'.join(part.lower() for part in context.get('app').split('_')),
			'-'.join(part.lower() for part in context.get('app').split('_'))
		)],
		'js_namespace': '{}.{}.{}'.format(
			''.join(part.capitalize() for part in settings.UNU_PROJECT_NAME.split('_')),
			''.join(part.capitalize() for part in context.get('app').split('_')),
			''.join(part.capitalize() for part in text.slugify(context.get('name')).split('-'))
		),
	}),
	'process': [
		add_file_to_views,
		add_url,
		add_template,
		add_static_files,
		fix_views_imports,
	]
}
REDIRECT_VIEW_CONFIG = {
	'fields': [
		{
			'name': 'app',
			'label': 'Django App',
			'field': 'select',
			'class': 'populate-with-apps',
			'data': {
				'get-apps-url': reverse_lazy('unu:get_apps'),
			},
			'coerce': lambda post: post.get('app'),
		},
		{
			'name': 'name',
			'label': 'View Name',
			'field': 'input',
			'class': 'live-slugify',
			'coerce': lambda post: post.get('name'),
		},
		{
			'name': 'pattern_name',
			'label': 'Pattern Name',
			'field': 'select',
			'class': 'populate-urls',
			'data': {
				'get-urls': reverse_lazy('unu:get_urls'),
			},
			'coerce': lambda post: post.get('pattern_name'),
		},
		{
			'name': 'query_string',
			'label': 'Preserve Querystring',
			'field': 'checkbox',
			'coerce': lambda post: post.get('query_string') == 'on',
		},
		{
			'name': 'permanent',
			'label': 'Permanent Redirect',
			'field': 'checkbox',
			'coerce': lambda post: post.get('permanent') == 'on',
		},
		{
			'name': 'mixins',
			'label': 'Controller mixins',
			'field': 'select-multiple',
			'options': CONTROLLER_MIXINS.keys(),
			'coerce': lambda post: post.getlist('mixins')
		}
	],
	'upgrade_context': lambda context: context.update({
		'view_template': 'redirect_view',
		'view_name': text.slugify(context.get('name')).replace('-', '_'),
		'url': text.slugify(context.get('name')),
		'class_extensions': ', '.join([
			CONTROLLER_MIXINS.get(mixin).get('module_path') for mixin in context.get('mixins')
		]),
		'imports': sorted(
			set().union(
				*[CONTROLLER_MIXINS.get(mixin).get('required_imports') for mixin in context.get('mixins')]
			)
		),
	}),
	'process': [
		add_file_to_views,
		add_url,
		fix_views_imports,
	]
}
FORM_VIEW_CONFIG = {
	'fields': [
		{
			'name': 'app',
			'label': 'Django App',
			'field': 'select',
			'class': 'populate-with-apps',
			'data': {
				'get-apps-url': reverse_lazy('unu:get_apps'),
			},
			'coerce': lambda post: post.get('app'),
		},
		{
			'name': 'name',
			'label': 'View Name',
			'field': 'input',
			'class': 'live-slugify',
			'coerce': lambda post: post.get('name'),
		},
		{
			'name': 'mixins',
			'label': 'Controller mixins',
			'field': 'select-multiple',
			'options': CONTROLLER_MIXINS.keys(),
			'coerce': lambda post: post.getlist('mixins')
		}
	],
	'upgrade_context': lambda context: context.update({
		'view_template': 'form_view',
		'view_name': text.slugify(context.get('name')).replace('-', '_'),
		'url': text.slugify(context.get('name')),
		'class_extensions': ', '.join([
			CONTROLLER_MIXINS.get(mixin).get('module_path') for mixin in context.get('mixins')
		]),
		'imports': sorted(
			set().union(
				*[CONTROLLER_MIXINS.get(mixin).get('required_imports') for mixin in context.get('mixins')]
			)
		),
		'form': '{}Form'.format(''.join([part.capitalize() for part in text.slugify(context.get('name')).split('-')])),
		'success_pattern': '{}:{}'.format(context.get('app'), text.slugify(context.get('name')).replace('-', '_')),
		'template_name': '{}/pages/{}.html'.format(
			context.get('app'),
			text.slugify(context.get('name')).replace('-', '_'),
		),
		'static_path': '{}/{}'.format(text.slugify(context.get('app')), text.slugify(context.get('name'))),
		'js_includes': ['{}/{}.js'.format(
			'-'.join(part.lower() for part in context.get('app').split('_')),
			'-'.join(part.lower() for part in context.get('app').split('_'))
		)],
		'js_namespace': '{}.{}.{}'.format(
			''.join(part.capitalize() for part in settings.UNU_PROJECT_NAME.split('_')),
			''.join(part.capitalize() for part in context.get('app').split('_')),
			''.join(part.capitalize() for part in text.slugify(context.get('name')).split('-'))
		),
	}),
	'process': [
		add_file_to_views,
		add_url,
		add_template,
		add_static_files,
		fix_views_imports,
		add_form,
		fix_forms_imports
	]
}
CHOICES = collections.OrderedDict({
	'view': {
		'name': 'View',
		'config': VIEW_CONFIG,
	},
	'template-view': {
		'name': 'TemplateView',
		'config': TEMPLATE_VIEW_CONFIG,
	},
	'redirect-view': {
		'name': 'RedirectView',
		'config': REDIRECT_VIEW_CONFIG,
	},
	'form-view': {
		'name': 'FormView',
		'config': FORM_VIEW_CONFIG,
	},
})


def get_new(view, request):
	log = ['Creating new view {}.'.format(view)]

	try:
		config = CHOICES.get(view).get('config')
		context = {}

		for field in config.get('fields'):
			context[field.get('name')] = field.get('coerce')(request.POST)

		config.get('upgrade_context')(context)

		for method in config.get('process'):
			log.extend(method(context))
	except Exception as e:
		logger.exception('Could not finish creating a view {}.'.format(view))
		log.append('Exception "{}" happened. See application logs for more information'.format(str(e)))

	return log
