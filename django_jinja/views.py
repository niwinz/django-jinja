# -*- coding: utf-8 -*-

from django.conf import settings
from django.views.generic import View
from django.template import loader, RequestContext
from django import http


class GenericView(View):
    response_cls = http.HttpResponse
    content_type = "text/html"
    tmpl_name = None

    def get_context_data(self):
        return {"view": self}

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        output = loader.render_to_string(self.tmpl_name, context,
                                         context_instance=RequestContext(request))

        return self.response_cls(output, content_type=self.content_type)


class PageNotFound(GenericView):
    tmpl_name = "404" + getattr(settings, 'DEFAULT_JINJA2_TEMPLATE_EXTENSION', '.jinja')
    response_cls = http.HttpResponseNotFound


class PermissionDenied(GenericView):
    tmpl_name = "403" + getattr(settings, 'DEFAULT_JINJA2_TEMPLATE_EXTENSION', '.jinja')
    response_cls = http.HttpResponseForbidden


class ServerError(GenericView):
    tmpl_name = "500" + getattr(settings, 'DEFAULT_JINJA2_TEMPLATE_EXTENSION', '.jinja')
    response_cls = http.HttpResponseServerError
