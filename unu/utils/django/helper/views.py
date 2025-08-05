import collections
import logging
import os
import re
import pathlib

from django.conf import settings
from django.template import loader
from django.urls import reverse_lazy
from django.utils import text
import isort
import black
import autoflake


logger = logging.getLogger(__name__)
BLACK_MODE = black.Mode(line_length=140)


def fix_views_imports(context):
    log = []

    app = context.get("app")
    log.append(f"Fixing imports for views in app {app}")
    if os.path.isdir(f"{settings.UNU_PROJECT_ROOT}/{app}/views"):
        file_names = []
        for file in os.listdir(f"{settings.UNU_PROJECT_ROOT}/{app}/views"):
            if file.endswith(".py") and "__init__.py" not in file:
                file_names.append(file.replace(".py", ""))

        with open(
            f"{settings.UNU_PROJECT_ROOT}/{app}/views/__init__.py",
            "w",
            encoding="utf-8",
        ) as file:
            for module_name in sorted(file_names):
                file.write(f"from . import {module_name}\n")
            file.write("\n\n")
            file.write("__all__ = [\n")
            for module_name in sorted(file_names):
                file.write(f"\t'{module_name}',\n")
            file.write("]\n")
    else:
        raise ValueError(f"Folder views does not exist for the app {app}. Fix the app first.")
    log.append(f"Imports for views in app {app} fixed.")

    return log


def fix_forms_imports(context):
    log = []

    forms_folder = f"""{settings.UNU_PROJECT_ROOT}/{context.get('app')}/forms"""

    file_names = collections.OrderedDict()
    for file in os.listdir(forms_folder):
        if file.endswith(".py") and "__init__.py" not in file:
            classes = []
            with open(f"{forms_folder}/{file}", encoding="utf-8") as form_file:
                for line in form_file.readlines():
                    if line.startswith("class "):
                        classes.append(line.split("(")[0].replace("class ", ""))
            file_names[file.replace(".py", "")] = sorted(classes)

    with open(f"{forms_folder}/__init__.py", "w", encoding="utf-8") as file:
        for file_name, classes in file_names.items():
            file.write(f"""from .{file_name} import {', '.join(classes)}\n""")

        file.write("\n\n")
        file.write("__all__ = [\n")
        for file_name, classes in file_names.items():
            file.write(f"""\t{", ".join([f"'{name}'" for name in classes])}, \n""")
        file.write("]\n")

    log.append("Form imports fixed")

    return log


def add_file_to_views(context):
    log = []

    if not os.path.isdir(f"""{settings.UNU_PROJECT_ROOT}/{context.get('app')}/views"""):
        raise ValueError(
            (
                f"""{settings.UNU_PROJECT_ROOT}/{context.get('app')}/views is not a folder. """
                f"""Fix app "{context.get('app')}" before you continue."""
            )
        )

    if os.path.isfile(f"""{settings.UNU_PROJECT_ROOT}/{context.get('app')}/views/{context.get('view_name')}.py"""):
        raise ValueError(
            (
                f"""File {settings.UNU_PROJECT_ROOT}/{context.get('app')}"""
                f"""/views/{context.get('view_name')}.py already exists. Will not create new view."""
            )
        )

    log.append(f"""Creating file for view {context.get('view_name')}""")
    with open(
        f"""{settings.UNU_PROJECT_ROOT}/{context.get('app')}/views/{context.get('view_name')}.py""",
        "w",
        encoding="utf-8",
    ) as file:
        file_contents = loader.render_to_string(f"""unu/code/views/{context.get('view_template')}.py""", context)
        file_contents = isort.code(file_contents, profile="black")
        file_contents = autoflake.fix_code(
            file_contents, remove_all_unused_imports=True, remove_duplicate_keys=True, remove_unused_variables=True
        )
        file_contents = black.format_file_contents(file_contents, fast=False, mode=BLACK_MODE)
        file.write(file_contents)

    log.append(f"""File {settings.UNU_PROJECT_ROOT}/{context.get('app')}/views/{context.get('view_name')}.py for view created.""")

    return log


def add_url(context):
    log = []

    app = context.get("app")
    view_name = context.get("view_name")
    kwarg_name = context.get("kwarg_name")
    kwarg_type = context.get("kwarg_type")
    url_prefix = context.get("url_prefix")

    log.append(f"Adding url for view {view_name} in app {app}")

    with open(f"{settings.UNU_PROJECT_ROOT}/{app}/urls.py", "r", encoding="utf-8") as file:
        urls_content = file.read()

    urls_split = urls_content.split("]", 1)
    url = context.get("url")

    if kwarg_name is not None:
        url = f"""{url}/<{f'{kwarg_type}:' if kwarg_type is not None else ''}""" "{kwarg_name}>"

    url_path = f"\tpath('{f'{url_prefix}/' if url_prefix is not None else ''}{url}', views.{view_name}.Controller.as_view(), name='{app}.{view_name}'),"

    with open(f"{app}/urls.py", "r", encoding="utf-8") as file:
        if url_path in file.read():
            raise ValueError(f"Will not add an existing url to urls.py for app {app}.")

    with open(f"{app}/urls.py", "w", encoding="utf-8") as file:
        file.write(f"{urls_split[0]}{url_path}\n]{urls_split[1]}")

    log.append(f"Added new path to urls.py for app {app}: {url_path}")

    return log


def ensure_skeleton(template_path, context):
    skeleton_path = f"{template_path}/skeleton.html"

    if not os.path.exists(skeleton_path):
        with open(skeleton_path, "w", encoding="utf-8") as file:
            file.write(loader.render_to_string("unu/code/views/skeleton.html", context))


def add_template(context):
    log = []

    log.append(f"""Adding template for view {context.get('view_name')}.""")

    folder_path = f"""{settings.UNU_PROJECT_ROOT}/{context.get('app')}/templates/{context.get('app')}"""
    if not os.path.isdir(folder_path):
        log.append(f"Creating folder {folder_path}.")
        os.makedirs(folder_path)

    # Ensure skeleton_exists
    ensure_skeleton(folder_path, context)

    pages_folder_path = f"{folder_path}/pages"

    if not os.path.isdir(pages_folder_path):
        log.append(f"Creating folder {pages_folder_path}.")
        os.makedirs(pages_folder_path)

    template_path = f"""{pages_folder_path}/{context.get('view_name')}.html"""

    if os.path.isfile(template_path):
        raise ValueError(f"Template at {template_path} already exists.")

    with open(template_path, "w", encoding="utf-8") as file:
        file.write(loader.render_to_string("unu/code/views/generic_view.html", context))

    log.append(f"""Template for view {context.get('view_name')} added.""")

    return log


def add_static_files(context):
    log = []

    static_folder = f"""{settings.UNU_PROJECT_ROOT}/{context.get('app')}/static/{context.get('app')}"""
    js_folder = f"{static_folder}/js"
    css_folder = f"{static_folder}/css"
    pathlib.Path(js_folder).mkdir(parents=True, exist_ok=True)
    pathlib.Path(css_folder).mkdir(parents=True, exist_ok=True)

    js_file_path = f"""{js_folder}/{context.get('static_name')}.js"""

    log.append(f"""Adding JS file for view {context.get('view_name')}.""")

    if os.path.isfile(js_file_path):
        raise ValueError(f"JS at {js_file_path} already exists.")

    with open(js_file_path, "w", encoding="utf-8") as file:
        file.write(loader.render_to_string("unu/code/views/generic_view.js", context))

    log.append(f"""JS file for view {context.get('view_name')} added.""")
    log.append(f"""Adding CSS file for view {context.get('view_name')}.""")

    css_file_path = f"""{css_folder}/{context.get('static_name')}.css"""

    if os.path.isfile(css_file_path):
        raise ValueError(f"CSS at {css_file_path} already exists.")

    with open(css_file_path, "w", encoding="utf-8") as file:
        file.write(loader.render_to_string("unu/code/views/generic_view.css", context))

    log.append(f"""CSS file for view {context.get('view_name')} added.""")

    return log


def add_form(context):
    log = []

    forms_path = f"""{settings.UNU_PROJECT_ROOT}/{context.get('app')}/forms"""
    if not os.path.isdir(forms_path):
        os.mkdir(forms_path)

    form_path = f"""{forms_path}/{context.get('view_name')}.py"""
    with open(form_path, "w", encoding="utf-8") as file:
        file.write(loader.render_to_string("unu/code/views/form.py", context))

    log.append(f"""Added form class {context.get('form')} to file {forms_path}.""")

    return log


def camel_case_split(identifier):
    return re.findall('[A-Z][a-z]+|[0-9A-Z]+(?=[A-Z][a-z])|[0-9A-Z]{2,}|[a-z0-9]{2,}|[a-zA-Z0-9]', identifier)


HTTP_METHODS = [
    "GET",
    "POST",
    "HEAD",
    "DELETE",
    "PUT",
    "OPTIONS",
    "CONNECT",
    "TRACE",
    "PATCH",
]
KWARG_TYPES = {
    "Without Type": None,
    "str": "str",
    "int": "int",
    "slug": "slug",
    "uuid": "uuid",
    "path": "path",
}
CONTROLLER_MIXINS = collections.OrderedDict(
    {
        "LoginRequiredMixin": {
            "module_path": "mixins.LoginRequiredMixin",
            "required_imports": [
                "from django.contrib.auth import mixins",
            ],
        },
        "UserPassesTestMixin": {
            "module_path": "mixins.UserPassesTestMixin",
            "required_imports": [
                "from django.contrib.auth import mixins",
            ],
        },
        "PermissionRequiredMixin": {
            "module_path": "mixins.PermissionRequiredMixin",
            "required_imports": [
                "from django.contrib.auth import mixins",
            ],
        },
        "DebugOnlyMixin": {
            "module_path": "unu.utils.views.mixins.debug.DebugOnlyMixin",
            "required_imports": [
                "import unu",
            ],
        },
    }
)
VIEW_CONFIG = {
    "fields": [
        {
            "name": "app",
            "label": "Django App",
            "field": "select",
            "class": "populate-with-apps",
            "data": {
                "get-apps-url": reverse_lazy("unu:get_apps"),
            },
            "coerce": lambda post: post.get("app"),
        },
        {
            "name": "name",
            "label": "View Name",
            "field": "input",
            "class": "live-slugify",
            "coerce": lambda post: post.get("name"),
        },
        {
            "name": "methods",
            "label": "HTTP Methods",
            "field": "select-multiple",
            "options": HTTP_METHODS,
            "coerce": lambda post: post.getlist("methods"),
        },
        {
            "name": "mixins",
            "label": "Controller mixins",
            "field": "select-multiple",
            "options": CONTROLLER_MIXINS.keys(),
            "coerce": lambda post: post.getlist("mixins"),
        },
    ],
    "upgrade_context": lambda context: context.update(
        {
            "view_template": "view",
            "view_name": '_'.join([part.lower() for part in camel_case_split(context.get('name'))]),
            "url": text.slugify(camel_case_split(context.get('name'))),
            "http_methods": ", ".join([f"'{method.lower()}'" for method in context.get("methods")]),
            "class_extensions": ", ".join([CONTROLLER_MIXINS.get(mixin).get("module_path") for mixin in context.get("mixins")]),
            "imports": sorted(
                set().union(*[["import unu"]] + [CONTROLLER_MIXINS.get(mixin).get("required_imports") for mixin in context.get("mixins")])
            ),
        }
    ),
    "process": [
        add_file_to_views,
        add_url,
        fix_views_imports,
    ],
}
TEMPLATE_VIEW_CONFIG = {
    "fields": [
        {
            "name": "app",
            "label": "Django App",
            "field": "select",
            "class": "populate-with-apps",
            "data": {
                "get-apps-url": reverse_lazy("unu:get_apps"),
            },
            "coerce": lambda post: post.get("app"),
        },
        {
            "name": "name",
            "label": "View Name",
            "field": "input",
            "class": "live-slugify",
            "coerce": lambda post: post.get("name"),
        },
        {
            "name": "mixins",
            "label": "Controller mixins",
            "field": "select-multiple",
            "options": CONTROLLER_MIXINS.keys(),
            "coerce": lambda post: post.getlist("mixins"),
        },
    ],
    "upgrade_context": lambda context: context.update(
        {
            "view_template": "template_view",
            "view_name": '_'.join([part.lower() for part in camel_case_split(context.get('name'))]),
            "url": text.slugify(camel_case_split(context.get('name'))),
            "class_extensions": ", ".join([CONTROLLER_MIXINS.get(mixin).get("module_path") for mixin in context.get("mixins")]),
            "imports": sorted(set().union(*[CONTROLLER_MIXINS.get(mixin).get("required_imports") for mixin in context.get("mixins")])),
            "template_name": (f"""{context.get('app')}/pages/{text.slugify(context.get('name')).replace('-', '_')}""" ".html"),
            "static_name": text.slugify(camel_case_split(context.get('name'))),
            "js_namespace": (
                f"""{"".join(part.capitalize() for part in settings.UNU_PROJECT_NAME.split("_"))}"""
                f"""{"".join(part.capitalize() for part in context.get("app").split("_"))}"""
                f"""{"".join(part.capitalize() for part in text.slugify(context.get("name")).split("-"))}"""
            ),
        }
    ),
    "process": [
        add_file_to_views,
        fix_views_imports,
        add_template,
        add_static_files,
        add_url,
    ],
}
REDIRECT_VIEW_CONFIG = {
    "fields": [
        {
            "name": "app",
            "label": "Django App",
            "field": "select",
            "class": "populate-with-apps",
            "data": {
                "get-apps-url": reverse_lazy("unu:get_apps"),
            },
            "coerce": lambda post: post.get("app"),
        },
        {
            "name": "name",
            "label": "View Name",
            "field": "input",
            "class": "live-slugify",
            "coerce": lambda post: post.get("name"),
        },
        {
            "name": "pattern_name",
            "label": "Pattern Name",
            "field": "select",
            "class": "populate-urls",
            "data": {
                "get-urls": reverse_lazy("unu:get_urls"),
            },
            "coerce": lambda post: post.get("pattern_name"),
        },
        {
            "name": "query_string",
            "label": "Preserve Querystring",
            "field": "checkbox",
            "coerce": lambda post: post.get("query_string") == "on",
        },
        {
            "name": "permanent",
            "label": "Permanent Redirect",
            "field": "checkbox",
            "coerce": lambda post: post.get("permanent") == "on",
        },
        {
            "name": "mixins",
            "label": "Controller mixins",
            "field": "select-multiple",
            "options": CONTROLLER_MIXINS.keys(),
            "coerce": lambda post: post.getlist("mixins"),
        },
    ],
    "upgrade_context": lambda context: context.update(
        {
            "view_template": "redirect_view",
            "view_name": '_'.join([part.lower() for part in camel_case_split(context.get('name'))]),
            "url": text.slugify(camel_case_split(context.get('name'))),
            "class_extensions": ", ".join([CONTROLLER_MIXINS.get(mixin).get("module_path") for mixin in context.get("mixins")]),
            "imports": sorted(set().union(*[CONTROLLER_MIXINS.get(mixin).get("required_imports") for mixin in context.get("mixins")])),
        }
    ),
    "process": [
        add_file_to_views,
        add_url,
        fix_views_imports,
    ],
}
FORM_VIEW_CONFIG = {
    "fields": [
        {
            "name": "app",
            "label": "Django App",
            "field": "select",
            "class": "populate-with-apps",
            "data": {
                "get-apps-url": reverse_lazy("unu:get_apps"),
            },
            "coerce": lambda post: post.get("app"),
        },
        {
            "name": "name",
            "label": "View Name",
            "field": "input",
            "class": "live-slugify",
            "coerce": lambda post: post.get("name"),
        },
        {
            "name": "mixins",
            "label": "Controller mixins",
            "field": "select-multiple",
            "options": CONTROLLER_MIXINS.keys(),
            "coerce": lambda post: post.getlist("mixins"),
        },
    ],
    "upgrade_context": lambda context: context.update(
        {
            "view_template": "form_view",
            "view_name": '_'.join([part.lower() for part in camel_case_split(context.get('name'))]),
            "url": text.slugify(camel_case_split(context.get('name'))),
            "class_extensions": ", ".join([CONTROLLER_MIXINS.get(mixin).get("module_path") for mixin in context.get("mixins")]),
            "imports": sorted(set().union(*[CONTROLLER_MIXINS.get(mixin).get("required_imports") for mixin in context.get("mixins")])),
            "form": f"""{''.join(
                [
                    part.capitalize() for part in camel_case_split(
                        context.get('name')
                    )
                ]
            )}Form""",
            "success_pattern": (f"""{context.get('app')}:{text.slugify(context.get('name')).replace('-', '_')}"""),
            "template_name": (
                f"""{context.get('app')}/pages/{'_'.join([part.lower() for part in camel_case_split(context.get('name'))])}.html"""
            ),
            "static_name": text.slugify(camel_case_split(context.get('name'))),
            "js_namespace": (
                f"""{"".join(part.capitalize() for part in settings.UNU_PROJECT_NAME.split("_"))}"""
                f"""{"".join(part.capitalize() for part in context.get("app").split("_"))}"""
                f"""{"".join(part.capitalize() for part in text.slugify(context.get("name")).split("-"))}"""
            ),
        }
    ),
    "process": [
        add_form,
        fix_forms_imports,
        add_file_to_views,
        add_template,
        fix_views_imports,
        add_url,
        add_static_files,
    ],
}
HEADLESS_FORM_VIEW_CONFIG = {
    "fields": [
        {
            "name": "app",
            "label": "Django App",
            "field": "select",
            "class": "populate-with-apps",
            "data": {
                "get-apps-url": reverse_lazy("unu:get_apps"),
            },
            "coerce": lambda post: post.get("app"),
        },
        {
            "name": "name",
            "label": "View Name",
            "field": "input",
            "class": "live-slugify",
            "coerce": lambda post: post.get("name"),
        },
        {
            "name": "url_prefix",
            "label": "URL Prefix",
            "field": "input",
            "coerce": lambda post: post.get("url_prefix"),
        },
        {
            "name": "mixins",
            "label": "Controller mixins",
            "field": "select-multiple",
            "options": CONTROLLER_MIXINS.keys(),
            "coerce": lambda post: post.getlist("mixins"),
        },
    ],
    "upgrade_context": lambda context: context.update(
        {
            "view_template": "form_view_headless",
            "view_name": '_'.join([part.lower() for part in camel_case_split(context.get('name'))]),
            "url": text.slugify(camel_case_split(context.get('name'))),
            "class_extensions": ", ".join([CONTROLLER_MIXINS.get(mixin).get("module_path") for mixin in context.get("mixins")]),
            "imports": sorted(set().union(*[CONTROLLER_MIXINS.get(mixin).get("required_imports") for mixin in context.get("mixins")])),
            "form": f"""{''.join(
                [
                    part.capitalize() for part in camel_case_split(
                        context.get('name')
                    )
                ]
            )}Form""",
        }
    ),
    "process": [
        add_form,
        fix_forms_imports,
        add_file_to_views,
        fix_views_imports,
        add_url,
    ],
}
CHOICES = collections.OrderedDict(
    {
        "view": {
            "name": "View",
            "config": VIEW_CONFIG,
        },
        "template-view": {
            "name": "TemplateView",
            "config": TEMPLATE_VIEW_CONFIG,
        },
        "redirect-view": {
            "name": "RedirectView",
            "config": REDIRECT_VIEW_CONFIG,
        },
        "form-view": {
            "name": "FormView",
            "config": FORM_VIEW_CONFIG,
        },
        "headless-form-view": {
            "name": "Headless FormView",
            "config": HEADLESS_FORM_VIEW_CONFIG,
        },
    }
)


def get_new(view, request):
    log = [f"Creating new view {view}."]

    config = CHOICES.get(view).get("config")
    context = {}

    for field in config.get("fields"):
        context[field.get("name")] = field.get("coerce")(request.POST)

    config.get("upgrade_context")(context)

    for method in config.get("process"):
        log.extend(method(context))

    return log
