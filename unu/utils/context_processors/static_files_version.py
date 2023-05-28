from django.conf import settings


def execute(request):
    return {
        "static_files_version": settings.STATIC_FILES_VERSION,
    }
