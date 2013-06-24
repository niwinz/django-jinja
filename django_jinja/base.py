# -*- coding: utf-8 -*-

import os
import sys
import copy

from jinja2 import Environment
from jinja2 import Template
from jinja2 import loaders
from jinja2 import TemplateSyntaxError
from jinja2 import FileSystemLoader

from django.conf import settings
from django.template import Origin
from django.template import TemplateDoesNotExist
from django.template import InvalidTemplateLibrary
from django.template.context import BaseContext
from django.template.loaders import app_directories
from django.utils.importlib import import_module
from django.utils import six

from . import builtins, utils
from .library import Library


JINJA2_ENVIRONMENT_OPTIONS = getattr(settings, 'JINJA2_ENVIRONMENT_OPTIONS', {})
JINJA2_EXTENSIONS = getattr(settings, 'JINJA2_EXTENSIONS', [])
JINJA2_FILTERS = getattr(settings, 'JINJA2_FILTERS', {})
JINJA2_TESTS = getattr(settings, 'JINJA2_TESTS', {})
JINJA2_GLOBALS = getattr(settings, 'JINJA2_GLOBALS', {})
JINJA2_AUTOESCAPE = getattr(settings, 'JINJA2_AUTOESCAPE', False)


# Default jinja extension list
DEFAULT_EXTENSIONS = [
    'jinja2.ext.do',
    'jinja2.ext.loopcontrols',
    'jinja2.ext.with_',
    'jinja2.ext.i18n',
    'jinja2.ext.autoescape',
]


JINJA2_FILTERS.update({
    'reverseurl': "django_jinja.builtins.filters.reverse",
    'addslashes': "django_jinja.builtins.filters.addslashes",
    'capfirst': "django_jinja.builtins.filters.capfirst",
    'escapejs': "django_jinja.builtins.filters.escapejs_filter",
    'fix_ampersands': "django_jinja.builtins.filters.fix_ampersands_filter",
    'floatformat': "django_jinja.builtins.filters.floatformat",
    'iriencode': "django_jinja.builtins.filters.iriencode",
    'linenumbers': "django_jinja.builtins.filters.linenumbers",
    'make_list': "django_jinja.builtins.filters.make_list",
    'slugify': "django_jinja.builtins.filters.slugify",
    'stringformat': "django_jinja.builtins.filters.stringformat",
    'title': "django_jinja.builtins.filters.title",
    'truncatechars': "django_jinja.builtins.filters.truncatechars",
    'truncatewords': "django_jinja.builtins.filters.truncatewords",
    'truncatewords_html': "django_jinja.builtins.filters.truncatewords_html",
    'upper': "django_jinja.builtins.filters.upper",
    'lower': "django_jinja.builtins.filters.lower",
    'urlencode': "django_jinja.builtins.filters.urlencode",
    'urlize': "django_jinja.builtins.filters.urlize",
    'urlizetrunc': "django_jinja.builtins.filters.urlizetrunc",
    'wordcount': "django_jinja.builtins.filters.wordcount",
    'wordwrap': "django_jinja.builtins.filters.wordwrap",
    'ljust': "django_jinja.builtins.filters.ljust",
    'rjust': "django_jinja.builtins.filters.rjust",
    'center': "django_jinja.builtins.filters.center",
    'cut': "django_jinja.builtins.filters.cut",
    'linebreaksbr': "django_jinja.builtins.filters.linebreaksbr",
    'linebreaks': "django_jinja.builtins.filters.linebreaks_filter",
    'removetags': "django_jinja.builtins.filters.removetags",
    'striptags': "django_jinja.builtins.filters.striptags",
    'join': "django_jinja.builtins.filters.join",
    'length': "django_jinja.builtins.filters.length",
    'random': "django_jinja.builtins.filters.random",
    'add': "django_jinja.builtins.filters.add",
    'date': "django_jinja.builtins.filters.date",
    'time': "django_jinja.builtins.filters.time",
    'timesince': "django_jinja.builtins.filters.timesince_filter",
    'timeuntil': "django_jinja.builtins.filters.timeuntil_filter",
    'default': "django_jinja.builtins.filters.default",
    'default_if_none': "django_jinja.builtins.filters.default_if_none",
    'divisibleby': "django_jinja.builtins.filters.divisibleby",
    'yesno': "django_jinja.builtins.filters.yesno",
    'filesizeformat': "django_jinja.builtins.filters.filesizeformat",
    'pprint': "django_jinja.builtins.filters.pprint",
    'pluralize': "django_jinja.builtins.filters.pluralize",
})

JINJA2_GLOBALS.update({
    'url': "django_jinja.builtins.global_context.url",
    'static': "django_jinja.builtins.global_context.static",
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
            if isinstance(value, six.string_types):
                self.filters[name] = utils.load_class(value)
            else:
                self.filters[name] = value

        # Add tests defined on settings + builtins
        for name, value in JINJA2_TESTS.items():
            if isinstance(value, six.string_types):
                self.tests[name] = utils.load_class(value)
            else:
                self.tests[name] = value

        # Add globals defined on settings + builtins
        for name, value in JINJA2_GLOBALS.items():
            if isinstance(value, six.string_types):
                self.globals[name] = utils.load_class(value)
            else:
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
        self.add_extension(builtins.extensions.CacheExtension)

        if self.autoescape:
            from django.utils import safestring
            if hasattr(safestring, "SafeText"):
                if not hasattr(safestring.SafeText, '__html__'):
                    if sys.version_info.major < 3:
                        safestring.SafeText.__html__ = lambda self: unicode(self)
                    else:
                        safestring.SafeText.__html__ = lambda self: str(self)

            if hasattr(safestring, "SafeString"):
                if not hasattr(safestring.SafeString, '__html__'):
                    if sys.version_info.major < 3:
                        safestring.SafeString.__html__ = lambda self: unicode(self)
                    else:
                        safestring.SafeString.__html__ = lambda self: str(self)

            if hasattr(safestring, "SafeUnicode"):
                if not hasattr(safestring.SafeUnicode, '__html__'):
                    if sys.version_info.major < 3:
                        safestring.SafeUnicode.__html__ = lambda self: unicode(self)
                    else:
                        safestring.SafeUnicode.__html__ = lambda self: str(self)

            if hasattr(safestring, "SafeBytes"):
                if not hasattr(safestring.SafeBytes, '__html__'):
                    if sys.version_info.major < 3:
                        safestring.SafeBytes.__html__ = lambda self: unicode(self)
                    else:
                        safestring.SafeBytes.__html__ = lambda self: str(self)


initial_params = {
    'autoescape': JINJA2_AUTOESCAPE,
    'loader': FileSystemLoader(app_directories.app_template_dirs + tuple(settings.TEMPLATE_DIRS)),
    'extensions': list(set(list(JINJA2_EXTENSIONS) + DEFAULT_EXTENSIONS)),
}

initial_params.update(JINJA2_ENVIRONMENT_OPTIONS)
env = Environment(**initial_params)
