from django.utils.translation import LANGUAGE_COOKIE_NAME


def execute(request):
	language = request.cookies.get(LANGUAGE_COOKIE_NAME)

	if language is None or language.strip() == '':
		language = 'en'

	return {
		'language': language,
	}
