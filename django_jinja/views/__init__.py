from django.views import defaults

from ..base import get_match_extension


def bad_request(request, exception=None):
    return defaults.bad_request(
        request,
        exception,
        template_name=f"400{get_match_extension() or '.jinja'}"
    )


def permission_denied(request, exception=None):
    return defaults.permission_denied(
        request,
        exception,
        template_name=f"403{get_match_extension() or '.jinja'}"
    )


def page_not_found(request, exception=None):
    return defaults.page_not_found(
        request,
        exception,
        template_name=f"404{get_match_extension() or '.jinja'}"
    )


def server_error(request):
    return defaults.server_error(
        request,
        template_name=f"500{get_match_extension() or '.jinja'}"
    )
