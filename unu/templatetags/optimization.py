import logging


from django import template
from django.utils import safestring
from django.conf import settings


import unu


register = template.Library()
logger = logging.getLogger(__name__)


@register.simple_tag
def css(file):
    if settings.DEBUG:
        unu.utils.frontend.optimization.css.update_file(file)
    return safestring.mark_safe(
        '<link{} type="text/css" rel="stylesheet" data-original="/media/dist/{}.css" data-source="/media/css/{}.css" href="/media/dist/{}{}.css?v={}" />'.format(
            ' id="locator-css"' if settings.DEBUG else "",
            file.replace("/", "-"),
            file,
            file.replace("/", "-"),
            ".opt" if not settings.DEBUG else "",
            settings.STATIC_FILES_VERSION,
        )
    )


@register.simple_tag
def javascript(file):
    if settings.DEBUG:
        unu.utils.frontend.optimization.javascript.update_file(file)
    return safestring.mark_safe(
        '<script{} type="text/javascript" async="async" data-original="/media/dist/{}.js" data-source="/media/js/{}.js" src="/media/dist/{}{}.js?v={}"></script>'.format(
            ' id="locator-js"' if settings.DEBUG else "",
            file.replace("/", "-"),
            file,
            file.replace("/", "-"),
            ".opt" if not settings.DEBUG else "",
            settings.STATIC_FILES_VERSION,
        )
    )
