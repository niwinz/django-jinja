"""
Since django 1.8.x, django comes with native multiple template engine support.
It also comes with jinja2 backend, but it is slightly unflexible, and it does
not support by default all django filters and related stuff.

This is an implementation of django backend inteface for use
django_jinja easy with django 1.8.
"""

from __future__ import absolute_import

import copy
import sys
from importlib import import_module

import jinja2
from django.conf import settings
from django.template import RequestContext
from django.template import TemplateDoesNotExist
from django.template import TemplateSyntaxError
from django.template.backends.base import BaseEngine
from django.template.backends.utils import csrf_input_lazy
from django.template.backends.utils import csrf_token_lazy
from django.utils import six
from django.utils.functional import cached_property
from django.utils.module_loading import import_string

from . import base
from . import builtins
from . import utils


class Jinja2(BaseEngine):
    app_dirname = "templates"

    def __init__(self, params):
        params = params.copy()
        options = params.pop("OPTIONS", {}).copy()

        super(Jinja2, self).__init__(params)

        newstyle_gettext = options.pop("newstyle_gettext", True)
        context_processors = options.pop("context_processors", [])
        match_extension = options.pop("match_extension", ".jinja")
        match_regex = options.pop("match_regex", None)
        environment_clspath = options.pop("environment", "jinja2.Environment")
        extra_filters = options.pop("filters", {})
        extra_tests = options.pop("tests", {})
        extra_globals = options.pop("globals", {})
        extra_constants = options.pop("constants", {})
        replace_filters_from_django = options.pop("replace_filters_from_django", True)
        translation_engine = options.pop("translation_engine", "django.utils.translation")

        environment_cls = import_string(environment_clspath)

        options.setdefault("loader", jinja2.FileSystemLoader(self.template_dirs))
        options.setdefault("extensions", base.DEFAULT_EXTENSIONS)
        options.setdefault("auto_reload", settings.DEBUG)
        options.setdefault("autoescape", True)

        if settings.DEBUG:
            options.setdefault("undefined", jinja2.DebugUndefined)
        else:
            options.setdefault("undefined", jinja2.Undefined)

        self.env = environment_cls(**options)

        self._context_processors = context_processors
        self._match_regex = match_regex
        self._match_extension = match_extension

        # Initialize i18n support
        if settings.USE_I18N:
            translation = import_module(translation_engine)
            self.env.install_gettext_translations(translation, newstyle=newstyle_gettext)
        else:
            self.env.install_null_translations(newstyle=newstyle_gettext)

        self._initialize_extensions()
        self._initialize_builtins(filters=extra_filters,
                                  tests=extra_tests,
                                  globals=extra_globals,
                                  constants=extra_constants,
                                  replace_filters_from_django=replace_filters_from_django)
        self._initialize_thirdparty()

    def _initialize_thirdparty(self):
        base._initialize_thirdparty(self.env)

    def _initialize_extensions(self):
        base._initialize_extensions()

    def _initialize_builtins(self, filters=None, tests=None, globals=None, constants=None,
                             replace_filters_from_django=True):
        _filters = copy.copy(base.JINJA2_FILTERS)
        if filters is not None:
            _filters.update(filters)

        if replace_filters_from_django:
            _filters.update(base.FILTERS_FROM_DJANGO)

        _globals = copy.copy(base.JINJA2_GLOBALS)
        if globals is not None:
            _globals.update(globals)

        _tests = copy.copy(base.JINJA2_TESTS)
        if tests is not None:
            _tests.update(tests)

        _constants = copy.copy(base.JINJA2_CONSTANTS)
        if constants is not None:
            _constants.update(constants)

        def insert(data, name, value):
            if isinstance(value, six.string_types):
                data[name] = import_string(value)
            else:
                data[name] = value

        for name, value in _filters.items():
            insert(self.env.filters, name, value)

        for name, value in _tests.items():
            insert(self.env.tests, name, value)

        for name, value in _globals.items():
            insert(self.env.globals, name, value)

        for name, value in _constants.items():
            self.env.globals[name] = value

        self.env.add_extension(builtins.extensions.CsrfExtension)
        self.env.add_extension(builtins.extensions.CacheExtension)

    @cached_property
    def context_processors(self):
        return tuple(import_string(path) for path in self._context_processors)

    def from_string(self, template_code):
        return Template(self.env.from_string(template_code), self)

    def match_template(self, template_name):
        return base.match_template(template_name,
                                   regex=self._match_regex,
                                   extension=self._match_extension)

    def get_template(self, template_name):
        if not self.match_template(template_name):
            raise TemplateDoesNotExist("Template {} does not exists".format(template_name))

        try:
            return Template(self.env.get_template(template_name), self)
        except jinja2.TemplateNotFound as exc:
            six.reraise(TemplateDoesNotExist, TemplateDoesNotExist(exc.args), sys.exc_info()[2])
        except jinja2.TemplateSyntaxError as exc:
            six.reraise(TemplateSyntaxError, TemplateSyntaxError(exc.args), sys.exc_info()[2])


class Template(object):
    def __init__(self, template, backend):
        self.template = template
        self.backend = backend


    def render(self, context=None, request=None):
        if context is None:
            context = {}

        if request is not None:
            context["request"] = request
            context["csrf_input"] = csrf_input_lazy(request)
            context["csrf_token"] = csrf_token_lazy(request)

            # Support for django context processors
            for processor in self.backend.context_processors:
                context.update(processor(request))

        return self.template.render(context)
