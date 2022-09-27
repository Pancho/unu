import os
import logging

from django.conf import settings
logger = logging.getLogger(__name__)
EXTENSION_COMMENTS = {
	'js': '//',
	'css': '/*',
}


def optimize_file(file_name, contents, optimize_function=None):
	optimized_file_name = '.opt.'.join(file_name.split('.'))

	success = True

	if optimize_function is not None:
		optimized_contents, success = optimize_function(contents)
	else:
		optimized_contents = contents

	with open(f'{settings.UNU_FRONTEND_MEDIA_PATH}dist/{optimized_file_name}', 'w') as file:
		file.write(optimized_contents)

	return success


def update_file(file_name, extension, minify_function):
	if not os.path.exists(f'{settings.UNU_FRONTEND_MEDIA_PATH}dist/'):
		os.mkdir(f'{settings.UNU_FRONTEND_MEDIA_PATH}dist/')

	file_path = f'{settings.UNU_FRONTEND_MEDIA_PATH}{extension}/{file_name}.{extension}'
	with open(file_path, 'r') as file:
		file_contents = file.read()

	includes = deduplicate_list(gather_includes(file_contents, extension))
	cleaned_file = clean_file(file_contents, extension)

	dist_file_contents = minify_function('{}\n{}\n'.format(
		'\n'.join(includes),
		cleaned_file
	))

	with open(f'''{settings.UNU_FRONTEND_MEDIA_PATH}dist/{file_name.replace('/', '-')}.{extension}''', 'w') as file:
		file.write(dist_file_contents)


def deduplicate_list(seq):
	seen = set()
	seen_add = seen.add
	return [item for item in seq if not (item in seen or seen_add(item))]


def clean_file(file_contents, extension):
	result = ''

	for line in file_contents.split('\n'):
		if f'{EXTENSION_COMMENTS.get(extension)} include:' not in line:
			result = f'{result}\n{line}'

	return result


def gather_includes(file_contents, extension):
	result = []

	for line in file_contents.split('\n'):
		if f'{EXTENSION_COMMENTS.get(extension)} include:' in line:
			include = line.split('include:')[1].split(' ')[0]
			with open(include, 'r') as file:
				contents = file.read()

				if 'include:' in contents:
					extra_includes = gather_includes(contents, extension)
					result.extend(extra_includes)

				result.append(clean_file(contents, extension))

	return result
