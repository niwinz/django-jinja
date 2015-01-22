"""
Since django 1.8.x, django comes with native multiple template engine support.
It also comes with jinja2 backend, but it is slightly unflexible, and it does
not support by default all django filters and related stuff.

This is an implementation of django backend inteface for use
django_jinja easy with django 1.8.
"""

from __future__ import absolute_import

import sys
import jinja2

from django.conf import settings
from django.template import TemplateDoesNotExist, TemplateSyntaxError
from django.utils import six
from django.utils.module_loading import import_string

from django.template.backends.base import BaseEngine
from django.template.backends.utils import csrf_input_lazy, csrf_token_lazy

from . import base


class Jinja2(BaseEngine):
    app_dirname = "templates"

    def __init__(self, params):
        params = params.copy()
        options = params.pop("OPTIONS", {}).copy()
        super(Jinja2, self).__init__(params)

        environment_clspath = options.pop("environment", None)

        options.setdefault("loader", jinja2.FileSystemLoader(self.template_dirs))
        options.setdefault("auto_reload", settings.DEBUG)

        self.env = base.make_environemnt(defaults=options,
                                         clspath=environment_clspath)

        base._initialize_builtins(self.env)
        base._initialize_thirdparty(self.env)
        base._initialize_i18n(self.env)
        base._initialize_bytecode_cache(self.env)


    def from_string(self, template_code):
        return Template(self.env.from_string(template_code))

    def get_template(self, template_name):
        try:
            return Template(self.env.get_template(template_name))
        except jinja2.TemplateNotFound as exc:
            six.reraise(TemplateDoesNotExist, TemplateDoesNotExist(exc.args),
                        sys.exc_info()[2])
        except jinja2.TemplateSyntaxError as exc:
            six.reraise(TemplateSyntaxError, TemplateSyntaxError(exc.args),
                        sys.exc_info()[2])

from django.template import RequestContext

class Template(object):
    def __init__(self, template):
        self.template = template

    def render(self, context=None, request=None):
        if context is None:
            context = {}
        if request is not None:
            context["request"] = request
            context["csrf_input"] = csrf_input_lazy(request)
            context["csrf_token"] = csrf_token_lazy(request)
        return self.template.render(context)
