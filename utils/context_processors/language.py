from django.utils.translation import LANGUAGE_SESSION_KEY


def execute(request):
	language = request.session.get(LANGUAGE_SESSION_KEY)
	
	if language is None or language.strip() == '':
		language = 'en'
	
	return {
		'language': language,
	}
