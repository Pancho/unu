import os
import sys
import inspect
import logging


from django.conf import settings


logger = logging.getLogger(__name__)


def has_models(app):
    return os.path.isdir(f"{settings.UNU_PROJECT_ROOT}/{app}/models")


def get_apps(with_models=False):
    apps = []

    for folder_name in os.listdir(path=settings.UNU_PROJECT_ROOT):
        folder_path = f'{settings.UNU_PROJECT_ROOT}/{folder_name}'
        if os.path.isdir(folder_path) and os.path.isfile(f"{folder_path}/apps.py"):
            with open(f"{folder_path}/apps.py", "r", encoding="utf-8") as file:
                contents = file.read()

                if "name = " in contents:
                    app = contents.split('name = "')[1].split('"')[0]
                    if with_models:
                        if has_models(app):
                            apps.append(app)
                    else:
                        apps.append(app)

    return apps


def get_models(app):
    return [
        name
        for name, obj in inspect.getmembers(sys.modules[f"{app}.models"])
        if inspect.isclass(obj)
    ]
