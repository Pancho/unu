from django.conf import settings


def execute(request):
    language = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)

    if language is None or language.strip() == "":
        language = "en"

    return {
        "language": language,
    }
