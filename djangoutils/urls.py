from django.urls import include, path
from django.contrib import admin
from django.views.generic import base


urlpatterns = [
    # FOR ROBOTS
    path(
        "robots.txt",
        base.TemplateView.as_view(template_name="unu/txt/robots.txt"),
        name="robots.txt",
    ),
    path(
        "ads.txt",
        base.TemplateView.as_view(template_name="unu/txt/ads.txt"),
        name="ads.txt",
    ),
    # ADMIN
    path("admin/", admin.site.urls),
    # Unu views
    path("unu/", include("unu.urls", namespace="unu")),
    path("test-fixers/", include("test_fixers.urls", namespace="test_fixers")),
]
