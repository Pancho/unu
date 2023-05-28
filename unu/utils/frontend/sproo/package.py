import io
import logging
import os
import zipfile

import requests
from django.conf import settings

import unu


logger = logging.getLogger(__name__)


def get_sproo_files(app):
    response = requests.get(settings.UNU_SPROO_LOCATION, stream=True, timeout=5)
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
        for zip_info in zip_file.filelist:
            if (
                "/sproo/js/" in zip_info.filename
                and zip_info.filename.endswith(".js")
                or "/sproo/css/" in zip_info.filename
                and zip_info.filename.endswith(".css")
            ):
                js_folder = f"""{settings.UNU_PROJECT_ROOT}/{app}/static/{app}/js"""
                target_file_name = f"{js_folder}/sproo/{zip_info.filename.split('sproo/')[1]}"
                target_folder_name = "/".join(target_file_name.split("/")[:-1])
                if not os.path.exists(target_folder_name):
                    os.makedirs(target_folder_name)

                with open(target_file_name, "w", encoding="utf-8") as target_file:
                    target_file.write(zip_file.read(zip_info.filename).decode())


def create_sproo_app(app, app_name, router_root_url, http_endpoint_stub, enable_logging):
    log = []

    js_folder = f"""{settings.UNU_PROJECT_ROOT}/{app}/static/{app}/js"""
    if app_name in os.listdir(js_folder):
        log.append("A folder with the app's name already exists")
        return log

    (
        index_page_class,
        _,  # index_page_path,
        index_page_log,
    ) = unu.utils.frontend.sproo.helper.create_sproo_page(
        params=[],
        enable_logging=enable_logging,
        component_name="index",
        app_name=app_name,
        app=app,
        use_store=False,
        include_stylesheet=True,
    )
    log.extend(index_page_log)

    (
        not_found_page_class,
        _,  # not_found_page_path,
        not_found_page_log,
    ) = unu.utils.frontend.sproo.helper.create_sproo_page(
        params=[],
        enable_logging=enable_logging,
        component_name="not found",
        app_name=app_name,
        app=app,
        use_store=False,
        include_stylesheet=True,
    )
    log.extend(not_found_page_log)

    create_kwargs = {
        "app": app,
        "app_name": app_name,
        "router_root_url": router_root_url,
        "static_path": settings.STATIC_URL,
        "index_page": index_page_class,
        "not_found_page": not_found_page_class,
        "routes": [],
        "root_stylesheets": [
            f"{settings.STATIC_URL}{app}/sproo/css/meta",
            f"{settings.STATIC_URL}{app}/sproo/css/normalize",
        ],
        "authentication_url": None,
        "authentication_class": None,
        "http_endpoint_stub": http_endpoint_stub,
        "on_app_ready": None,
        "providers": [],
        "logger_config": "level: 'trace'," if enable_logging else "",
    }

    index_log = unu.utils.frontend.sproo.helper.create_sproo_index(**create_kwargs)
    log.extend(index_log)

    return log


def create_sproo_component(app, app_folder, component_name, use_store, include_stylesheet):
    log = []

    app_data = unu.utils.frontend.sproo.analyze.get_sproo_app_data(app_folder)
    index = app_data.get("index")
    app_name = index.get("app_name")
    enable_logging = index.get("logger_config") is not None

    (
        _,  # component_class,
        _,  # component_path,
        component_log,
    ) = unu.utils.frontend.sproo.helper.create_sproo_component(
        params=[],
        enable_logging=enable_logging,
        component_name=component_name,
        app_name=app_name,
        app=app,
        use_store=use_store,
        include_stylesheet=include_stylesheet,
    )
    log.extend(component_log)

    return log


def create_sproo_page(app, app_folder, component_name, url_pattern, use_store):
    log = []

    app_data = unu.utils.frontend.sproo.analyze.get_sproo_app_data(app_folder)
    index = app_data.get("index")
    app_name = index.get("app_name")
    enable_logging = index.get("logger_config") is not None
    params = [param.replace(":", "") for param in url_pattern.split("/") if param.startswith(":")]

    (
        page_class,
        page_path,
        page_log,
    ) = unu.utils.frontend.sproo.helper.create_sproo_page(
        params=[],
        enable_logging=enable_logging,
        component_name=component_name,
        app_name=app_name,
        app=app,
        use_store=use_store,
        include_stylesheet=True,
    )
    log.extend(page_log)

    index["routes"].append(
        {
            "class_name": page_class,
            "path": url_pattern,
        }
    )
    log_entry = {
        "class_name": page_class,
        "path": url_pattern,
    }
    log.append(f"Added route {log_entry}")
    if use_store:
        index["providers"].append(f"{page_class}.STORE_PROVIDER")
        log.append(f"Adding provider {page_class}.STORE_PROVIDER")
    index["imports"].update(
        {
            page_class: page_path,
        }
    )
    log.append(f"Adding import {page_class}:{page_path}")

    index_log = unu.utils.frontend.sproo.helper.create_sproo_index(**index)
    log.extend(index_log)

    return log
