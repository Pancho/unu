import logging
import os


from django.conf import settings
from django.template import loader


logger = logging.getLogger(__name__)


def create_sproo_index(
    **kwargs,
):
    log = []

    root_stylesheets = kwargs.get("root_stylesheets")
    if root_stylesheets is None:
        log.append("Using default root stylesheets")
        root_stylesheets = [
            f"""/{settings.STATIC_URL}{kwargs.get("app")}/js/sproo/css/meta""",
            f"""/{settings.STATIC_URL}{kwargs.get("app")}/js/sproo/css/normalize""",
        ]
    else:
        log.append("Using supplied root stylesheets")

    log.append("Extracted app name and path")

    context = {
        **kwargs,
        "router_root_url": kwargs.get("router_root_url"),
        "http_endpoint_stub": kwargs.get("http_endpoint_stub"),
        "index_page": kwargs.get("index_page"),
        "not_found_page": kwargs.get("not_found_page"),
        "app_name": kwargs.get("app_name"),
        "authentication_url": kwargs.get("authentication_url"),
        "authentication_class": kwargs.get("authentication_class"),
        "root_stylesheets": root_stylesheets,
        "routes": kwargs.get("routes"),
        "on_app_ready": kwargs.get("on_app_ready"),
        "providers": kwargs.get("providers"),
        "logger_config": kwargs.get("logger_config"),
        "imports": kwargs.get("imports"),
    }

    target_file_name = f"""{settings.UNU_PROJECT_ROOT}/{kwargs.get("app")}/static/{kwargs.get("app")}/js/{kwargs.get("app_name")}/index.js"""
    target_folder_name = "/".join(target_file_name.split("/")[:-1])
    if not os.path.exists(target_folder_name):
        os.makedirs(target_folder_name)

    with open(target_file_name, "w", encoding="utf-8") as file:
        file.write(loader.render_to_string("unu/code/sproo/index.js", context))

    log.append(f"""Index file for the app "{kwargs.get("app_name")}" is now updated""")
    return log


def create_sproo_component(**kwargs):
    return assemble_sproo_component(
        **{"component_type": "components", "params": [], **kwargs},
    )


def create_sproo_page(**kwargs):
    return assemble_sproo_component(
        **{"component_type": "pages", **kwargs},
    )


def assemble_sproo_component(
    **kwargs,
):
    log = []

    component_name_suffix = "Page" if kwargs.get("component_type") == "pages" else ""
    log_entity = "page component" if kwargs.get("component_type") == "pages" else "component"

    log.append(f"Creating new {log_entity}")

    component_name = kwargs.get("component_name").lower().replace("page", "").replace("component", "").strip()
    class_name = f"{''.join([part.capitalize() for part in component_name.split(' ')])}{component_name_suffix}Component"
    log.append(f"New {log_entity} class name: {class_name}")

    path_stub = "-".join([part.lower() for part in component_name.split(" ")])
    component_path = f"{path_stub}/{path_stub}"
    app_path = "-".join([part.lower() for part in kwargs.get("app_name").split(" ")])
    log.append(f"{log_entity.capitalize()} paths assembled")

    tag_name = f"{app_path}-{path_stub}"
    log.append(f"{log_entity.capitalize()} tag name: {tag_name}")

    component_folder = (
        f"""{settings.UNU_PROJECT_ROOT}/{kwargs.get("app")}/static/{kwargs.get("app")}/js/{kwargs.get("app_name")}"""
        f"""/{kwargs.get("component_type")}/{path_stub}"""
    )
    log.append(f"{log_entity.capitalize()} file paths created")

    context = {
        **kwargs,
        "static_path": settings.STATIC_URL,
        "class_name": class_name,
        "tag_name": tag_name,
        "app_path": app_path,
        "path_stub": path_stub,
        "component_path": component_path,
        "params": ", ".join(kwargs.get("params")),
    }

    if not os.path.exists(component_folder):
        os.makedirs(component_folder)

    for extension in ["js", "html", "css"]:
        with open(f"{component_folder}/{path_stub}.{extension}", "w", encoding="utf-8") as file:
            file.write(loader.render_to_string(f"unu/code/sproo/component.{extension}", context))
            log.append(f"{log_entity.capitalize()} {extension} file created")

    return (
        f"""{settings.STATIC_URL}{kwargs.get("app")}/js/{kwargs.get("app_name")}/{kwargs.get("component_type")}/{path_stub}/{path_stub}.js""",
        f"/{kwargs.get('component_type')}/{component_path}.js",
        log,
    )
