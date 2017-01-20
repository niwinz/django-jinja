# -*- coding: utf-8 -*-

import django
from django import http
from django.template import RequestContext, loader
from django.views.generic import View

from ..base import get_match_extension


class GenericView(View):
    response_cls = http.HttpResponse
    content_type = "text/html"
    tmpl_name = None

    def get_context_data(self):
        return {"view": self}

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        if django.VERSION[:2] < (1, 8):
            output = loader.render_to_string(self.tmpl_name, context,
                                             context_instance=RequestContext(request))
        else:
            output = loader.render_to_string(self.tmpl_name, context, request=request)

        return self.response_cls(output, content_type=self.content_type)


class ErrorView(GenericView):

    def head(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def options(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    match_extension = get_match_extension() or ".jinja"


class PageNotFound(ErrorView):
    tmpl_name = "404" + ErrorView.match_extension
    response_cls = http.HttpResponseNotFound


class PermissionDenied(ErrorView):
    tmpl_name = "403" + ErrorView.match_extension
    response_cls = http.HttpResponseForbidden


class BadRequest(ErrorView):
    tmpl_name = "400" + ErrorView.match_extension
    response_cls = http.HttpResponseBadRequest


class ServerError(ErrorView):
    tmpl_name = "500" + ErrorView.match_extension
    response_cls = http.HttpResponseServerError
