# -*- coding: utf-8 -*-
import os
import re
from importlib import import_module

import django
import jinja2
from django.conf import settings
from django.template.context import BaseContext
from django.test import utils as django_utils
from django.test.signals import setting_changed, template_rendered
from django.utils import six
from jinja2 import Template as Jinja2Template
from jinja2.loaders import BaseLoader

from . import builtins
from . import library
from . import utils

JINJA2_ENVIRONMENT_OPTIONS = getattr(settings, "JINJA2_ENVIRONMENT_OPTIONS", {})
JINJA2_EXTENSIONS = getattr(settings, "JINJA2_EXTENSIONS", builtins.DEFAULT_EXTENSIONS)
JINJA2_AUTOESCAPE = getattr(settings, "JINJA2_AUTOESCAPE", True)
JINJA2_UNDEFINED = getattr(settings, "JINJA2_UNDEFINED", None)
JINJA2_NEWSTYLE_GETTEXT = getattr(settings, "JINJA2_NEWSTYLE_GETTEXT", True)

JINJA2_BYTECODE_CACHE_ENABLE = getattr(settings, "JINJA2_BYTECODE_CACHE_ENABLE", False)
JINJA2_BYTECODE_CACHE_NAME = getattr(settings, "JINJA2_BYTECODE_CACHE_NAME", "default")
JINJA2_BYTECODE_CACHE_BACKEND = getattr(settings, "JINJA2_BYTECODE_CACHE_BACKEND",
                                        "django_jinja.cache.BytecodeCache")
JINJA2_TRANSLATION_ENGINE = getattr(settings, "JINJA2_TRANSLATION_ENGINE", "django.utils.translation")
JINJA2_CONSTANTS = getattr(settings, "JINJA2_CONSTANTS", {})
JINJA2_TESTS = getattr(settings, "JINJA2_TESTS", {})
JINJA2_FILTERS = getattr(settings, "JINJA2_FILTERS", {})
JINJA2_GLOBALS = getattr(settings, "JINJA2_GLOBALS", {})


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


class Template(jinja2.Template):
    """
    Customized jinja2 Template subclass.
    Add correct handling django context objects.
    """

    def render(self, context={}):
        new_context = dict_from_context(context)
        if settings.TEMPLATE_DEBUG:
            from django.test import signals

            # Define a "django" like context for emitatet the multi
            # layered context object. This is mainly for apps like
            # django-debug-toolbar that are very coupled to django's
            # internal implementation of context.

            if not isinstance(context, BaseContext):
                class CompatibilityContext(dict):
                    @property
                    def dicts(self):
                        return [self]

                context = CompatibilityContext(context)

            signals.template_rendered.send(sender=self, template=self,
                                           context=context)

        return super(Template, self).render(new_context)

    def stream(self, context={}):
        new_context = dict_from_context(context)
        if settings.TEMPLATE_DEBUG:
            from django.test import signals
            # self.origin = Origin(self.filename)
            signals.template_rendered.send(sender=self, template=self, context=context)

        return super(Template, self).stream(new_context)


def _iter_templatetags_modules_list():
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

    for app_path in all_modules:
        try:
            mod = import_module(app_path + ".templatetags")
            # Empty folders can lead to unexpected behavior with Python 3.
            # We make sure to have the `__file__` attribute.
            if hasattr(mod, '__file__'):
                yield (app_path, os.path.dirname(mod.__file__))
        except ImportError:
            pass


def patch_django_for_autoescape():
    """
    Patch django modules for make them compatible with
    jinja autoescape implementation.
    """
    from django.utils import safestring
    from django.forms.forms import BoundField

    try:
        from django.forms.utils import ErrorList
        from django.forms.utils import ErrorDict

    # Just for django < 1.7 compatibility
    except ImportError:
        from django.forms.util import ErrorList
        from django.forms.util import ErrorDict

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

    if not hasattr(BoundField, "__html__"):
        BoundField.__html__ = lambda self: six.text_type(self)

    if not hasattr(ErrorList, "__html__"):
        ErrorList.__html__ = lambda self: six.text_type(self)

    if not hasattr(ErrorDict, "__html__"):
        ErrorDict.__html__ = lambda self: six.text_type(self)


def setup_test_environment():
    if not hasattr(Jinja2Template, '_original_render'):
        Jinja2Template._original_render = Jinja2Template.render
        def instrumented_render(template_object, *args, **kwargs):
            context = dict(*args, **kwargs)
            template_rendered.send(sender=template_object,
                                   template=template_object,
                                   context=context)
            return Jinja2Template._original_render(template_object, *args, **kwargs)
        Jinja2Template.render = instrumented_render
    django_utils._original_setup_test_environment()


def _initialize_thirdparty(env):
    """
    Iterate over all available apps in searching and preloading
    available template filters or functions for jinja2.
    """
    for app_path, mod_path in _iter_templatetags_modules_list():
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

    library._update_env(env)


def _initialize_builtins(env):
    """
    Inject into environment instances builtin
    filters, tests, globals, and constants.
    """
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


def _initialize_i18n(env):
    # install translations
    if settings.USE_I18N:
        translation = import_module(JINJA2_TRANSLATION_ENGINE)
        env.install_gettext_translations(translation, newstyle=JINJA2_NEWSTYLE_GETTEXT)
    else:
        env.install_null_translations(newstyle=JINJA2_NEWSTYLE_GETTEXT)


def _initialize_template_loader(env):
    loader = getattr(settings, "JINJA2_LOADER", None)

    if isinstance(loader, six.string_types):
        cls = utils.load_class(loader)
        env.loader = cls()
    elif isinstance(loader, BaseLoader):
        env.loader = loader
    elif loader is None:
        # Create a default loader using django template dirs
        # and django app template dirs.
        from django.template.loaders import app_directories
        default_loader_dirs = (tuple(settings.TEMPLATE_DIRS) +
                               app_directories.app_template_dirs)
        env.loader = jinja2.FileSystemLoader(default_loader_dirs)
    else:
        raise RuntimeError("Wrong parameters to 'JINJA2_LOADER'")


def _initialize_bytecode_cache(env):
    if JINJA2_BYTECODE_CACHE_ENABLE:
        cls = utils.load_class(JINJA2_BYTECODE_CACHE_BACKEND)
        env.bytecode_cache = cls(JINJA2_BYTECODE_CACHE_NAME)


def match_template(template_name, regex=None, extension=None):
    if extension:
        matches_extension = template_name.endswith(extension)
        if regex:
            return matches_extension and re.match(regex, template_name)
        else:
            return template_name.endswith(extension)
    elif regex:
        return re.match(regex, template_name)
    else:
        return True


def make_environment(defaults=None, clspath=None):
    """
    Create a new instance of jinja2 environment.
    """

    initial_params = {"autoescape": JINJA2_AUTOESCAPE}
    initial_params.update(JINJA2_ENVIRONMENT_OPTIONS)

    initial_params.setdefault("extensions", [])
    initial_params["extensions"].extend(JINJA2_EXTENSIONS)

    if JINJA2_UNDEFINED:
        if isinstance(JINJA2_UNDEFINED, six.string_types):
            initial_params["undefined"] = utils.load_class(JINJA2_UNDEFINED)
        else:
            initial_params["undefined"] = JINJA2_UNDEFINED

    if settings.DEBUG:
        initial_params.setdefault("undefined", jinja2.DebugUndefined)
    else:
        initial_params.setdefault("undefined", jinja2.Undefined)

    if defaults is not None:
        initial_params.update(defaults)

    if clspath is None:
        clspath = "jinja2.Environment"

    cls = utils.load_class(clspath)
    env = cls(**initial_params)
    env.template_class = Template

    return env


if django.VERSION[:2] < (1, 8):
    def get_match_extension(using=None):
        """
        Gets the extension that the template loader will match for
        django-jinja. This returns the DEFAULT_JINJA2_TEMPLATE_EXTENSION
        setting.

        The "using" parameter is ignored for Django versions before 1.8.
        """
        return getattr(settings, 'DEFAULT_JINJA2_TEMPLATE_EXTENSION', '.jinja')
else:
    def get_match_extension(using=None):
        """
        Gets the extension that the template loader will match for
        django-jinja. This returns Jinja2.match_extension.

        The "using" parameter selects with Jinja2 backend to use if
        you have multiple ones configured in settings.TEMPLATES.
        If it is None and only one Jinja2 backend is defined then it
        will use that, otherwise an ImproperlyConfigured exception
        is thrown.
        """
        from .backend import Jinja2
        from django.template import engines

        if using is None:
            engine = Jinja2.get_default()
        else:
            engine = engines[using]

        return engine.match_extension


def initialize(environment):
    """
    Initialize given environment populating it with
    builtins and with django i18n data.
    """
    _initialize_builtins(environment)
    _initialize_thirdparty(environment)
    _initialize_i18n(environment)
    _initialize_bytecode_cache(environment)
    _initialize_template_loader(environment)


def testing_reinitialize_signal(setting, **kwargs):
    if "JINJA" in setting or "TEMPLATE" in setting:
        global env
        env = make_environment()
        initialize(env)


# Global variable for store the environment for django <= 1.7
env = None

def setup():
    global env
    env = make_environment()

    initialize(env)
    setting_changed.connect(testing_reinitialize_signal)

# Fallback for prevous django versions.
if django.VERSION[:2] < (1, 7):
    patch_django_for_autoescape()
    setup()
