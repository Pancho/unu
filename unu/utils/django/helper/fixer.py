import os
import re
import ast
import logging

from django.conf import settings
from django.template import loader
import isort
import black
import autoflake

import unu

logger = logging.getLogger(__name__)
BLACK_MODE = black.Mode(line_length=140)


def handle_imports_and_classes(app, module, default_class_name=None):
    module_folder_path = f"{settings.UNU_PROJECT_ROOT}/{app}/{module}"
    if not os.path.exists(f"{module_folder_path}.py"):
        return False
    if not os.path.exists(module_folder_path):
        os.mkdir(module_folder_path)
    with open(f"{settings.UNU_PROJECT_ROOT}/{app}/{module}.py", "r", encoding="utf-8") as views_file:
        preface = []
        classes = []
        for element in ast.parse(views_file.read()).body:
            if isinstance(element, ast.ClassDef):
                classes.append(element)

            if not classes:
                preface.append(element)

        preface_string = "\n".join([ast.unparse(part) for part in preface])
        for module_class in classes:
            file_name = pascal_to_snake_case(module_class.name)
            if default_class_name is not None:
                module_class.name = default_class_name
            file_path = f"{module_folder_path}/{file_name}.py"
            with open(file_path, "w", encoding="utf-8") as class_file:
                class_contents = f"{preface_string}\n{ast.unparse(module_class)}"
                class_contents = isort.code(class_contents, profile="black")
                class_contents = autoflake.fix_code(
                    class_contents, remove_all_unused_imports=True, remove_duplicate_keys=True, remove_unused_variables=True
                )
                class_contents = black.format_file_contents(class_contents, fast=False, mode=BLACK_MODE)
                class_file.write(class_contents)

    os.remove(f"{settings.UNU_PROJECT_ROOT}/{app}/{module}.py")
    return True


def fix_views(selected_app):
    fixed = []
    result = []
    if selected_app == "all":
        apps = unu.utils.django.helper.context.get_apps()
    else:
        apps = [selected_app]

    for app in apps:
        if handle_imports_and_classes(app, "views", "Controller"):
            fixed.append(app)

    for app in apps:
        views_folder = f"{settings.UNU_PROJECT_ROOT}/{app}/views"

        if not os.path.isdir(views_folder):
            continue

        file_names = []
        for file in os.listdir(views_folder):
            if file.endswith(".py") and "__init__.py" not in file:
                file_names.append(file.replace(".py", ""))

        with open(f"{views_folder}/__init__.py", "w", encoding="utf-8") as file:
            for file_name in file_names:
                file.write(f"from . import {file_name}\n")

            file.write("\n\n")
            file.write("__all__ = [\n")
            for file_name in file_names:
                file.write(f"""\t"{file_name}", \n""")
            file.write("]\n")

    if len(fixed) > 0:
        result.append(
            f"""Views for app{'s' if len(fixed) > 1 else ''}
            {', '.join(fixed)} fixed."""
        )

    return result


def fix_models(selected_app):
    fixed = []
    result = []
    if selected_app == "all":
        apps = unu.utils.django.helper.context.get_apps()
    else:
        apps = [selected_app]

    for app in apps:
        if handle_imports_and_classes(app, "models"):
            fixed.append(app)

    for app in apps:
        models_folder = f"{settings.UNU_PROJECT_ROOT}/{app}/models"

        if not os.path.isdir(models_folder):
            continue

        file_names = {}
        for file in os.listdir(models_folder):
            if file.endswith(".py") and "__init__.py" not in file:
                classes = []
                with open(f"{models_folder}/{file}", encoding="utf-8") as form_file:
                    for line in form_file.readlines():
                        if line.startswith("class "):
                            classes.append(line.split("(")[0].replace("class ", ""))
                file_names[file.replace(".py", "")] = classes

        with open(f"{models_folder}/__init__.py", "w", encoding="utf-8") as file:
            for file_name, classes in file_names.items():
                file.write(f"""from .{file_name} import {', '.join(classes)}\n""")

            file.write("\n\n")
            file.write("__all__ = [\n")
            for file_name, classes in file_names.items():
                file.write(f"""\t{", ".join([f"'{name}'" for name in classes])}, \n""")
            file.write("]\n")

    result.append("Fixed imports for all models.")

    return result


def fix_urls(selected_app):
    fixed = []
    skipped = []
    result = []
    if selected_app == "all":
        apps = unu.utils.django.helper.context.get_apps()
    else:
        apps = [selected_app]

    for app in apps:
        if not os.path.isfile(f"{settings.UNU_PROJECT_ROOT}/{app}/urls.py"):
            with open(
                f"{settings.UNU_PROJECT_ROOT}/{app}/urls.py",
                "w",
                encoding="utf-8",
            ) as file:
                file.write(
                    loader.render_to_string(
                        "unu/code/helper/urls.py",
                        {
                            "app": app,
                        },
                    )
                )
            fixed.append(app)
        else:
            skipped.append(app)

    if len(fixed) > 0:
        result.append(
            f"""URLs for app{'s' if len(fixed) > 1 else ''}
            {', '.join(fixed)} fixed."""
        )

    if len(skipped) > 0:
        result.append(
            f"""URLs for app{'s' if len(skipped) > 1 else ''}
            {', '.join(skipped)} skipped."""
        )

    return result


def extract_apps(selection):
    if selection == "all":
        return unu.utils.django.helper.context.get_apps()
    return [selection]


def pascal_to_snake_case(identifier):
    return re.findall('[A-Z][a-z]+|[0-9A-Z]+(?=[A-Z][a-z])|[0-9A-Z]{2,}|[a-z0-9]{2,}|[a-zA-Z0-9]', identifier)
