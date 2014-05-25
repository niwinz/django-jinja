# -*- coding: utf-8 -*-

import os

from jinja2 import Environment
from jinja2 import Template
from jinja2 import FileSystemLoader

from django.conf import settings
from django.template import Origin
from django.template.context import BaseContext
from django.utils.importlib import import_module
from django.utils import six

from . import builtins, utils


JINJA2_ENVIRONMENT_OPTIONS = getattr(settings, "JINJA2_ENVIRONMENT_OPTIONS", {})
JINJA2_EXTENSIONS = getattr(settings, "JINJA2_EXTENSIONS", [])
JINJA2_FILTERS = getattr(settings, "JINJA2_FILTERS", {})
JINJA2_FILTERS_REPLACE_FROM_DJANGO = getattr(settings, "JINJA2_FILTERS_REPLACE_FROM_DJANGO", True)
JINJA2_TESTS = getattr(settings, "JINJA2_TESTS", {})
JINJA2_GLOBALS = getattr(settings, "JINJA2_GLOBALS", {})
JINJA2_AUTOESCAPE = getattr(settings, "JINJA2_AUTOESCAPE", True)
JINJA2_NEWSTYLE_GETTEXT = getattr(settings, "JINJA2_NEWSTYLE_GETTEXT", True)
JINJA2_CONSTANTS = getattr(settings, "JINJA2_CONSTANTS", {})

JINJA2_BYTECODE_CACHE_ENABLE = getattr(settings, "JINJA2_BYTECODE_CACHE_ENABLE", False)
JINJA2_BYTECODE_CACHE_NAME = getattr(settings, "JINJA2_BYTECODE_CACHE_NAME", "default")
JINJA2_BYTECODE_CACHE_BACKEND = getattr(settings, "JINJA2_BYTECODE_CACHE_BACKEND",
                                        "django_jinja.cache.BytecodeCache")


# Default jinja extension list
DEFAULT_EXTENSIONS = [
    "jinja2.ext.do",
    "jinja2.ext.loopcontrols",
    "jinja2.ext.with_",
    "jinja2.ext.i18n",
    "jinja2.ext.autoescape",
]


JINJA2_FILTERS.update({
    "static": "django_jinja.builtins.filters.static",
    "reverseurl": "django_jinja.builtins.filters.reverse",
    "addslashes": "django_jinja.builtins.filters.addslashes",
    "capfirst": "django_jinja.builtins.filters.capfirst",
    "escapejs": "django_jinja.builtins.filters.escapejs_filter",
    "fix_ampersands": "django_jinja.builtins.filters.fix_ampersands_filter",
    "floatformat": "django_jinja.builtins.filters.floatformat",
    "iriencode": "django_jinja.builtins.filters.iriencode",
    "linenumbers": "django_jinja.builtins.filters.linenumbers",
    "make_list": "django_jinja.builtins.filters.make_list",
    "slugify": "django_jinja.builtins.filters.slugify",
    "stringformat": "django_jinja.builtins.filters.stringformat",
    "truncatechars": "django_jinja.builtins.filters.truncatechars",
    "truncatewords": "django_jinja.builtins.filters.truncatewords",
    "truncatewords_html": "django_jinja.builtins.filters.truncatewords_html",
    "urlizetrunc": "django_jinja.builtins.filters.urlizetrunc",
    "ljust": "django_jinja.builtins.filters.ljust",
    "rjust": "django_jinja.builtins.filters.rjust",
    "cut": "django_jinja.builtins.filters.cut",
    "linebreaksbr": "django_jinja.builtins.filters.linebreaksbr",
    "linebreaks": "django_jinja.builtins.filters.linebreaks_filter",
    "removetags": "django_jinja.builtins.filters.removetags",
    "striptags": "django_jinja.builtins.filters.striptags",
    "add": "django_jinja.builtins.filters.add",
    "date": "django_jinja.builtins.filters.date",
    "time": "django_jinja.builtins.filters.time",
    "timesince": "django_jinja.builtins.filters.timesince_filter",
    "timeuntil": "django_jinja.builtins.filters.timeuntil_filter",
    "default_if_none": "django_jinja.builtins.filters.default_if_none",
    "divisibleby": "django_jinja.builtins.filters.divisibleby",
    "yesno": "django_jinja.builtins.filters.yesno",
    "pluralize": "django_jinja.builtins.filters.pluralize",
})

if JINJA2_FILTERS_REPLACE_FROM_DJANGO:
    JINJA2_FILTERS.update({
        "title": "django_jinja.builtins.filters.title",
        "upper": "django_jinja.builtins.filters.upper",
        "lower": "django_jinja.builtins.filters.lower",
        "urlencode": "django_jinja.builtins.filters.urlencode",
        "urlize": "django_jinja.builtins.filters.urlize",
        "wordcount": "django_jinja.builtins.filters.wordcount",
        "wordwrap": "django_jinja.builtins.filters.wordwrap",
        "center": "django_jinja.builtins.filters.center",
        "join": "django_jinja.builtins.filters.join",
        "length": "django_jinja.builtins.filters.length",
        "random": "django_jinja.builtins.filters.random",
        "default": "django_jinja.builtins.filters.default",
        "filesizeformat": "django_jinja.builtins.filters.filesizeformat",
        "pprint": "django_jinja.builtins.filters.pprint",
    })

JINJA2_GLOBALS.update({
    "url": "django_jinja.builtins.global_context.url",
    "static": "django_jinja.builtins.global_context.static",
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

    def stream(self, context={}):
        new_context = dict_from_context(context)

        if settings.TEMPLATE_DEBUG:
            from django.test import signals
            self.origin = Origin(self.filename)
            signals.template_rendered.send(sender=self, template=self, context=context)

        return super(Template, self).stream(new_context)


class Environment(Environment):
    def initialize(self):
        self.initialize_i18n()
        self.initialize_bytecode_cache()
        self.initialize_template_loader()
        self.initialize_autoescape()

    def initialize_i18n(self):
        # install translations
        if settings.USE_I18N:
            from django.utils import translation
            self.install_gettext_translations(translation, newstyle=JINJA2_NEWSTYLE_GETTEXT)
        else:
            self.install_null_translations(newstyle=JINJA2_NEWSTYLE_GETTEXT)

    def initialize_bytecode_cache(self):
        # Install bytecode cache if is enabled
        if JINJA2_BYTECODE_CACHE_ENABLE:
            cls = utils.load_class(JINJA2_BYTECODE_CACHE_BACKEND)
            self.bytecode_cache = cls(JINJA2_BYTECODE_CACHE_NAME)

    def initialize_template_loader(self):
        self.template_class = Template

        loader = getattr(settings, "JINJA2_LOADER", None)
        if loader is None:
            from django.template.loaders import app_directories
            default_loader_dirs = (app_directories.app_template_dirs +
                                   tuple(settings.TEMPLATE_DIRS))

            self.loader = FileSystemLoader(default_loader_dirs)
        elif isinstance(loader, six.string_types):
            loader_params = getattr(settings, "JINJA2_LOADER_SETTINGS", {})
            cls = utils.load_class(loader)
            self.loader = cls(**loader_params)
        else:
            self.loader = loader

    def initialize_autoescape(self):
        if not self.autoescape:
            return

        from django.utils import safestring

        if hasattr(safestring, "SafeText"):
            if not hasattr(safestring.SafeText, "__html__"):
                safestring.SafeText.__html__ = lambda self: six.text_type(self)

        if hasattr(safestring, "SafeString"):
            if not hasattr(safestring.SafeString, "__html__"):
                safestring.SafeString.__html__ = lambda self: six.text_type(self)

        if hasattr(safestring, "SafeUnicode"):
            if not hasattr(safestring.SafeUnicode, "__html__"):
                safestring.SafeUnicode.__html__ = lambda self: six.text_type(self)

        if hasattr(safestring, "SafeBytes"):
            if not hasattr(safestring.SafeBytes, "__html__"):
                safestring.SafeBytes.__html__ = lambda self: six.text_type(self)


def get_templatetags_modules_list():
    """
    Get list of modules that contains templatetags
    submodule.
    """
    # Django 1.7 compatibility imports
    try:
        from django.apps import apps
        all_modules = [x.name for x in apps.get_app_configs()]
    except ImportError:
        all_modules = settings.INSTALLED_APPS

    mod_list = []
    for app_path in all_modules:
        try:
            mod = import_module(app_path + ".templatetags")
            mod_list.append((app_path, os.path.dirname(mod.__file__)))
        except ImportError:
            pass

    return mod_list


def load_builtins(env):
    for name, value in JINJA2_FILTERS.items():
        if isinstance(value, six.string_types):
            env.filters[name] = utils.load_class(value)
        else:
            env.filters[name] = value

    for name, value in JINJA2_TESTS.items():
        if isinstance(value, six.string_types):
            env.tests[name] = utils.load_class(value)
        else:
            env.tests[name] = value

    for name, value in JINJA2_GLOBALS.items():
        if isinstance(value, six.string_types):
            env.globals[name] = utils.load_class(value)
        else:
            env.globals[name] = value

    for name, value in JINJA2_CONSTANTS.items():
        env.globals[name] = value

    env.add_extension(builtins.extensions.CsrfExtension)
    env.add_extension(builtins.extensions.CacheExtension)


def load_django_templatetags():
    """
    Given a ready modules list, try import all modules
    related to templatetags for populate a library.
    """

    for app_path, mod_path in get_templatetags_modules_list():
        if not os.path.isdir(mod_path):
            continue

        for filename in filter(lambda x: x.endswith(".py") or x.endswith(".pyc"), os.listdir(mod_path)):
            # Exclude __init__.py files
            if filename == "__init__.py" or filename == "__init__.pyc":
                continue

            file_mod_path = "%s.templatetags.%s" % (app_path, filename.rsplit(".", 1)[0])
            try:
                import_module(file_mod_path)
            except ImportError:
                pass


initial_params = {
    "autoescape": JINJA2_AUTOESCAPE,
    "extensions": list(set(list(JINJA2_EXTENSIONS) + DEFAULT_EXTENSIONS)),
}

initial_params.update(JINJA2_ENVIRONMENT_OPTIONS)
env = Environment(**initial_params)


def initialize_environment():
    env.initialize()

    load_django_templatetags()
    load_builtins(env)


__all__ = ["env", "initialize_environment"]
