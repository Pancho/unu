import logging
import os
import re

from django.conf import settings

import unu.utils.django.helper.context

logger = logging.getLogger(__name__)
SPROO_APP_IMPORT = re.compile(r"(import {)(.*?)(} from \'.)(.*?)(\';)")
SPROO_APP_ROUTER_ROOT_URL = re.compile(r"(routeRoot: \')(.*?)(\',)")
SPROO_APP_STATIC_ROOT_URL = re.compile(r"(staticRoot: \')(.*?)(\',)")
SPROO_APP_INDEX_PAGE = re.compile(r"(homePage: {\s)(.*?\s)(\s},)")
SPROO_APP_NOT_FOUND_PAGE = re.compile(r"(notFound: {\s)(.*?\s)(\s},)")
SPROO_APP_ROUTES = re.compile(r"(routes: \[)((.*?\s)*?)(\],)")
SPROO_APP_ROUTES_INNER = re.compile(r"(\n\s*?)({.+?\1})", re.M | re.S)
SPROO_APP_COMPONENT_ENTRY = re.compile(r"(component: )('\"*)(.*)('\"*)(,*)")
SPROO_APP_PATH_ENTRY = re.compile(r"(path: \')(.*)(\',*)")
SPROO_APP_GUARD_ENTRY = re.compile(r"(guard: )('\"*)(.*)('\"*)(,*)")
SPROO_APP_HOOKS_ENTRY = re.compile(r"(hooks: )((.*?\s)*?})")
SPROO_APP_ROOT_STYLESHEETS = re.compile(r"(rootStylesheets: \[\s)((.*?\s)*?)(\])")
SPROO_APP_AUTHENTICATION_MODULE = re.compile(r"(authenticationModule: )('\"*)(.*)('\"*)(,)")
SPROO_APP_AUTHENTICATION_URL = re.compile(r"(authenticationUrl: \')(.*)(\',*)")
SPROO_APP_HTTP_ENDPOINT_STUB = re.compile(r"(httpEndpointStub: \')(.*?)(\',)")
SPROO_APP_ON_APP_READY = re.compile(r"(onAppReady: \[\n+?\s+)(.*?)(\n\s\],)", re.M | re.S)
SPROO_APP_PROVIDERS = re.compile(r"(providers: \[)(.*?)(])", re.M | re.S)
SPROO_APP_LOGGER_CONFIG = re.compile(r"(loggerConfig: {\n+?\s+)(.*?)(\n\s},)", re.M | re.S)


def has_sproo():
    return os.path.isdir(f"{settings.UNU_FRONTEND_MEDIA_PATH}sproo")


def apps_with_sproo():
    sproo_apps = []

    for app in unu.utils.django.helper.context.get_apps():
        sproo_folder_path = f"{settings.UNU_PROJECT_ROOT}/{app}/static/{app}/js/sproo"
        if os.path.exists(sproo_folder_path):
            sproo_apps.append(app)

    return sproo_apps


def has_sproo_app():
    for folder in os.listdir(settings.UNU_FRONTEND_MEDIA_PATH):
        index_file_path = f"{settings.UNU_FRONTEND_MEDIA_PATH}{folder}/index.js"
        if os.path.exists(index_file_path):
            return True
    return False


def get_sproo_apps():
    sproo_apps = []

    for app in unu.utils.django.helper.context.get_apps():
        js_folder_path = f"{settings.UNU_PROJECT_ROOT}/{app}/static/{app}/js"
        if not os.path.exists(js_folder_path):
            continue
        for folder in os.listdir(js_folder_path):
            index_file_path = f"{js_folder_path}/{folder}/index.js"
            if os.path.exists(index_file_path):
                with open(index_file_path, "r", encoding="utf-8") as file:
                    contents = file.read()
                if "new App({" in contents:
                    sproo_apps.append({
                        'app': app,
                        'sproo_app': folder
                    })

    return sproo_apps


def get_sproo_app_data(app, app_folder):
    if app is None or app_folder is None:
        return {}

    app_file = ""
    index_file_contents = ""
    index_file_path = f"{settings.UNU_PROJECT_ROOT}/{app}/static/{app}/js/{app_folder}/index.js"

    if os.path.exists(index_file_path):
        with open(index_file_path, "r", encoding="utf-8") as index_file:
            index_file_contents = index_file.read()
            app_file = index_file_path

    pages = []
    pages_folder = f"{settings.UNU_PROJECT_ROOT}/{app}/static/{app}/js/{app_folder}/pages"
    components = []
    components_folder = f"{settings.UNU_PROJECT_ROOT}/{app}/static/{app}/js/{app_folder}/components"

    if os.path.exists(pages_folder):
        for folder in os.listdir(pages_folder):
            pages.append(folder)

    if os.path.exists(components_folder):
        for folder in os.listdir(components_folder):
            components.append(folder)

    index = parse_index(index_file_contents)
    return {
        "index": index,
        "app": app,
        "app_folder": app_folder,
        "app_file": app_file,
        "page_folders": pages,
        "component_folders": components,
    }


def parse_index(index_file_contents):
    router_root_url = parse_router_root_url(index_file_contents)
    static_root_url = parse_static_root_url(index_file_contents)
    index_page = parse_index_page(index_file_contents)
    not_found_page = parse_not_found_page(index_file_contents)
    routes = parse_routes(index_file_contents)
    # routes, routes_imports = parse_routes(index_file_contents)
    root_stylesheets = parse_root_stylesheets(index_file_contents)
    authentication_url = parse_authentication_url(index_file_contents)
    authentication_module = parse_authentication_module(index_file_contents)
    http_endpoint_stub = parse_http_endpoint_stub(index_file_contents)
    on_app_ready = parse_on_app_ready(index_file_contents)
    providers = parse_providers(index_file_contents)
    logger_config = parse_logger_config(index_file_contents)

    return {
        "router_root_url": router_root_url,
        "static_root_url": static_root_url,
        "index_page": index_page,
        "not_found_page": not_found_page,
        "routes": routes,
        "root_stylesheets": root_stylesheets,
        "authentication_url": authentication_url,
        "authentication_module": authentication_module,
        "http_endpoint_stub": http_endpoint_stub,
        "on_app_ready": on_app_ready,
        "providers": providers,
        "logger_config": logger_config,
    }


def parse_router_root_url(index_file_contents):
    match = SPROO_APP_ROUTER_ROOT_URL.search(index_file_contents)
    if match is not None:
        return match.group(2).strip()
    return None


def parse_static_root_url(index_file_contents):
    match = SPROO_APP_STATIC_ROOT_URL.search(index_file_contents)
    if match is not None:
        return match.group(2).strip()
    return None


def parse_index_page(index_file_contents):
    match = SPROO_APP_INDEX_PAGE.search(index_file_contents)

    if match is not None:
        for line in match.group(2).split(","):
            if line.strip() == "":
                continue
            component_match = SPROO_APP_COMPONENT_ENTRY.search(line)
            class_name = component_match.group(3).strip()
            return class_name
    return None


def parse_not_found_page(index_file_contents):
    match = SPROO_APP_NOT_FOUND_PAGE.search(index_file_contents)

    if match is not None:
        for line in match.group(2).split(","):
            if line.strip() == "":
                continue
            component_match = SPROO_APP_COMPONENT_ENTRY.search(line)
            class_name = component_match.group(3).strip()
            return class_name
    return None


def parse_routes(index_file_contents):
    result = []

    match = SPROO_APP_ROUTES.search(index_file_contents)

    if match is not None:
        for blob in SPROO_APP_ROUTES_INNER.split(match.group(2)):
            if blob.strip() == "," or blob.strip() == "":
                continue
            component_match = SPROO_APP_COMPONENT_ENTRY.search(blob)
            path_match = SPROO_APP_PATH_ENTRY.search(blob)
            guard_match = SPROO_APP_GUARD_ENTRY.search(blob)
            hooks_match = SPROO_APP_HOOKS_ENTRY.search(blob)
            class_name = component_match.group(3).replace(",", "").strip()
            path = path_match.group(2).replace(",", "").strip()
            guard = ""
            if guard_match is not None:
                guard = guard_match.group(2).replace(",", "").strip()
            hooks = ""
            if hooks_match is not None:
                hooks = hooks_match.group(2)  # This one we leave as-is
            route = {
                "component": class_name,
                "path": path,
                "guard": guard,
                "hooks": hooks,
            }
            if route not in result:
                result.append(route)

    return result


def parse_root_stylesheets(index_file_contents):
    result = []

    match = SPROO_APP_ROOT_STYLESHEETS.search(index_file_contents)

    if match is not None:
        for stylesheet_import in match.group(2).split(","):
            if stylesheet_import.strip() == "":
                continue
            result.append(stylesheet_import.strip().replace("'", ""))

    return result


def parse_authentication_url(index_file_contents):
    match = SPROO_APP_AUTHENTICATION_URL.search(index_file_contents)
    if match is not None:
        class_name = match.group(2).strip()
        return class_name
    return None


def parse_authentication_module(index_file_contents):
    match = SPROO_APP_AUTHENTICATION_MODULE.search(index_file_contents)
    if match is not None:
        class_name = match.group(2).strip()
        return class_name
    return None


def parse_http_endpoint_stub(index_file_contents):
    match = SPROO_APP_HTTP_ENDPOINT_STUB.search(index_file_contents)
    if match is not None:
        return match.group(2).strip()
    return None


def parse_on_app_ready(index_file_contents):
    match = SPROO_APP_ON_APP_READY.search(index_file_contents)
    if match is not None:
        return match.group(2).strip()
    return None


def parse_providers(index_file_contents):
    result = []

    match = SPROO_APP_PROVIDERS.search(index_file_contents)

    if match is not None:
        for stylesheet_import in match.group(2).split(","):
            if stylesheet_import.strip() == "":
                continue
            result.append(stylesheet_import.strip())

    return result


def parse_logger_config(index_file_contents):
    match = SPROO_APP_LOGGER_CONFIG.search(index_file_contents)
    if match is not None:
        return match.group(2).strip()
    return None
