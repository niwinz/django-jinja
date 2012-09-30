# -*- coding: utf-8 -*-

from jinja2 import Environment
from jinja2 import Template
from jinja2 import loaders
from jinja2 import TemplateSyntaxError
from jinja2 import FileSystemLoader

from django.conf import settings
from django.template.context import BaseContext
from django.template import TemplateDoesNotExist
from django.template import Origin
from django.template import InvalidTemplateLibrary
from django.template.loaders import app_directories
from django.utils.importlib import import_module

import os
import copy

JINJA2_ENVIRONMENT_OPTIONS = getattr(settings, 'JINJA2_ENVIRONMENT_OPTIONS', {})
JINJA2_EXTENSIONS = getattr(settings, 'JINJA2_EXTENSIONS', [])
JINJA2_FILTERS = getattr(settings, 'JINJA2_FILTERS', {})
JINJA2_TESTS = getattr(settings, 'JINJA2_TESTS', {})
JINJA2_GLOBALS = getattr(settings, 'JINJA2_GLOBALS', {})
JINJA2_AUTOESCAPE = getattr(settings, 'JINJA2_AUTOESCAPE', False)

from django_jinja import builtins

JINJA2_FILTERS.update({
    'reverseurl': builtins.filters.reverse,
    'addslashes': builtins.filters.addslashes,
    'escapejs': builtins.filters.escapejs_filter,
    'capfirst': builtins.filters.capfirst,
    'floatformat': builtins.filters.floatformat,
    'truncatechars': builtins.filters.truncatechars,
    'truncatewords': builtins.filters.truncatewords,
    'truncatewords_html': builtins.filters.truncatewords_html,
    'wordwrap': builtins.filters.wordwrap,
    'title': builtins.filters.title,
    'slugify': builtins.filters.slugify,
    'lower': builtins.filters.lower,
    'ljust': builtins.filters.ljust,
    'rjust': builtins.filters.rjust,
    'linebreaksbr': builtins.filters.linebreaksbr,
    'linebreaks': builtins.filters.linebreaks_filter,
    'removetags': builtins.filters.removetags,
    'striptags': builtins.filters.striptags,
    'join': builtins.filters.join,
    'random': builtins.filters.random,
    'add': builtins.filters.add,
    'date': builtins.filters.date,
    'time': builtins.filters.time,
    'timesince': builtins.filters.timesince_filter,
    'timeuntil': builtins.filters.timeuntil_filter,
    'default': builtins.filters.default,
    'default_if_none': builtins.filters.default_if_none,
    'divisibleby': builtins.filters.divisibleby,
    'yesno': builtins.filters.yesno,
    'filesizeformat': builtins.filters.filesizeformat,
    'pprint': builtins.filters.pprint,
    'safe': builtins.filters.safe,
})

JINJA2_GLOBALS.update({
    'url': builtins.global_context.url,
})


def dict_from_context(context):
    """
    Converts context to native python dict.
    """

    if isinstance(context, BaseContext):
        new_dict = {}
        for i in reversed(list(context)):
            new_dict.update(dict_from_context(i))
        return new_dict

    return dict(context)


class Template(Template):
    """
    Customized template class.
    Add correct handling django context objects.
    """

    def render(self, context={}):
        new_context = dict_from_context(context)

        if settings.TEMPLATE_DEBUG:
            from django.test import signals
            self.origin = Origin(self.filename)
            signals.template_rendered.send(sender=self, template=self, context=context)

        return super(Template, self).render(new_context)


class Environment(Environment):
    def __init__(self, *args, **kwargs):
        super(Environment, self).__init__(*args, **kwargs)

        # install translations
        if settings.USE_I18N:
            from django.utils import translation
            self.install_gettext_translations(translation)
        else:
            self.install_null_translations(newstyle=False)

        self.template_class = Template

        # Add filters defined on settings + builtins
        for name, value in JINJA2_FILTERS.items():
            self.filters[name] = value

        # Add tests defined on settings + builtins
        for name, value in JINJA2_TESTS.items():
            self.tests[name] = value

        # Add globals defined on settings + builtins
        for name, value in JINJA2_GLOBALS.items():
            self.globals[name] = value

        mod_list = []
        for app_path in settings.INSTALLED_APPS:
            try:
                mod = import_module(app_path + '.templatetags')
                mod_list.append((app_path,os.path.dirname(mod.__file__)))
            except ImportError:
                pass

        for app_path, mod_path in mod_list:
            for filename in filter(lambda x: x.endswith(".py"), os.listdir(mod_path)):
                if filename == '__init__.py':
                    continue

                file_mod_path = "%s.templatetags.%s" % (app_path, filename.rsplit(".", 1)[0])
                try:
                    filemod = import_module(file_mod_path)
                except ImportError:
                    pass

        # Update current environment with app filters
        Library()._update_env(self)

        # Add builtin extensions.
        self.add_extension(builtins.extensions.CsrfExtension)


class Library(object):
    instance = None

    _globals = {}
    _tests = {}
    _filters = {}

    def __new__(cls, *args, **kwargs):
        if cls.instance == None:
            cls.instance = super(Library, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    @classmethod
    def get_instance(cls):
        return cls.instance

    def _update_env(self, env):
        env.filters.update(self._filters)
        env.globals.update(self._globals)
        env.tests.update(self._tests)

    def _new_function(self, attr, func, name=None):
        _attr = getattr(self, attr)
        if name is None:
            name = func.__name__

        _attr[name] = func
        return func

    def _function(self, attr, name=None, _function=None):
        if name is None and _function is None:
            def dec(func):
                return self._new_function(attr, func)
            return dec

        elif name is not None and _function is None:
            if callable(name):
                return self._new_function(attr, name)

            else:
                def dec(func):
                    return self._function(attr, name, func)

                return dec

        elif name is not None and _function is not None:
            return self._new_function(attr, _function, name)

        raise RuntimeError("Invalid parameters")

    def global_function(self, *args, **kwargs):
        return self._function("_globals", *args, **kwargs)

    def test(self, *args, **kwargs):
        return self._function("_tests", *args, **kwargs)

    def filter(self, *args, **kwargs):
        return self._function("_filters", *args, **kwargs)

    def __setitem__(self, item, value):
        self.globals[item] = value

    def __getitem__(self, item, value): #for reciprocity with __setitem__
        return self.globals[item]


initial_params = {
    'autoescape': JINJA2_AUTOESCAPE,
    'loader': FileSystemLoader(app_directories.app_template_dirs + settings.TEMPLATE_DIRS),
    'extensions':['jinja2.ext.i18n', 'jinja2.ext.autoescape'],
}

initial_params.update(JINJA2_ENVIRONMENT_OPTIONS)
env = Environment(**initial_params)
