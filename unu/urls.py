from django.conf import settings
from django.urls import path

from unu import views


app_name = "unu"
if settings.DEBUG:
    urlpatterns = [
        path("", views.index.Controller.as_view(), name="index"),
        path(
            "optimize-client-code",
            views.optimize_client_code.Controller.as_view(),
            name="optimize_client_code",
        ),
        path("analyze", views.analyze.Controller.as_view(), name="analyze"),
        path("fix-views", views.fix_views.Controller.as_view(), name="fix_views"),
        path(
            "fix-models",
            views.fix_models.Controller.as_view(),
            name="fix_models",
        ),
        path("fix-urls", views.fix_urls.Controller.as_view(), name="fix_urls"),
        path(
            "new-view/<str:view>",
            views.new_view.Controller.as_view(),
            name="new_view",
        ),
        path(
            "new-view/<str:view>/create",
            views.new_view_create.Controller.as_view(),
            name="new_view_create",
        ),
        path("get-apps", views.get_apps.Controller.as_view(), name="get_apps"),
        path("get-urls", views.get_urls.Controller.as_view(), name="get_urls"),
        path(
            "get-models",
            views.get_models.Controller.as_view(),
            name="get_models",
        ),
        path("sproo", views.sproo.Controller.as_view(), name="sproo"),
        path(
            "sproo-get-files/<slug:app>",
            views.sproo_get_files.Controller.as_view(),
            name="sproo_get_files",
        ),
        path(
            "sproo-new-app",
            views.sproo_new_app.Controller.as_view(),
            name="sproo_new_app",
        ),
        path(
            "sproo-new-page",
            views.sproo_new_page.Controller.as_view(),
            name="sproo_new_page",
        ),
        path(
            "sproo-new-component",
            views.sproo_new_component.Controller.as_view(),
            name="sproo_new_component",
        ),
        path(
            "sproo-app/<slug:app>/<slug:app_folder>",
            views.sproo_app.Controller.as_view(),
            name="sproo_app",
        ),
    ]
