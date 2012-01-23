# -*- coding: utf-8 -*-

__version__ = (0, 1, 0, 'final', 0)


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

import copy


def dict_from_context(context):
    """
    Converts context to native python dict.
    """

    if isinstance(context, BaseContext):
        d = {}
        for i in reversed(list(context)):
            d.update(dict_from_context(i))
        return d
    else:
        return dict(context)


class Template(Template):
    """
    Customized template class.
    Add correct handling django context objects.
    """

    def render(self, context):
        new_context = dict_from_context(context)

        if settings.TEMPLATE_DEBUG:
            from django.test import signals
            self.origin = Origin(self.filename)
            signals.template_rendered.send(sender=self, template=self, context=context)

        return super(Template, self).render(context_dict)


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


from django.template.loaders import app_directories

JINJA2_ENVIRONMENT_OPTIONS = getattr(settings, 'JINJA2_ENVIRONMENT_OPTIONS', {})

initial_params = {
    'autoescape': False,
    'loader': FileSystemLoader(app_directories.app_template_dirs + settings.TEMPLATE_DIRS),
    'extensions':['jinja2.ext.i18n'],
}

initial_params.update(JINJA2_ENVIRONMENT_OPTIONS)

env = Environment(**initial_params)
