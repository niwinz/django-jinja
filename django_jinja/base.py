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

import copy

JINJA2_ENVIRONMENT_OPTIONS = getattr(settings, 'JINJA2_ENVIRONMENT_OPTIONS', {})
JINJA2_EXTENSIONS = getattr(settings, 'JINJA2_EXTENSIONS', [])
JINJA2_FILTERS = getattr(settings, 'JINJA2_FILTERS', {})
JINJA2_TESTS = getattr(settings, 'JINJA2_TESTS', {})


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

        return super(Template, self).render(new_context)

from django.utils.importlib import import_module
import os

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
        
        # Add filters defined on settings
        for name, value in JINJA2_FILTERS.iteritems():
            self.filters[name] = value
        
        # Add tests defined on settings
        for name, value in JINJA2_TESTS.iteritems():
            self.tests[name] = value

        mod_list = []
        for app_path in settings.INSTALLED_APPS:
            try:
                mod = import_module(app_path + '.templatetags')
                mod_list.append((app_path,os.path.dirname(mod.__file__)))
            except ImportError:
                pass
        
        file_mod_list = []
        for app_path, mod_path in mod_list:
            for filename in filter(lambda x: x.endswith(".py"), os.listdir(mod_path)):
                if filename == '__init__.py':
                    continue

                file_mod_path = "%s.templatetags.%s" % (app_path, filename.rsplit(".", 1)[0])
                try:
                    filemod = import_module(file_mod_path)
                    file_mod_list.append(filemod)
                except ImportError:
                    pass

        for mod in file_mod_list:
            try:
                reg_attr = mod.register
            except AttributeError:
                continue

            if not isinstance(reg_attr, Library):
                continue

            if reg_attr.extensions:
                self.extensions.extend(reg_attr.extensions)

            if reg_attr.filters:
                self.filters.update(reg_attr.filters)

            if reg_attr.tests:
                self.tests.update(reg_attr.tests)
                

class Library(object):
    def __init__(self):
        self.filters = {}
        self.extensions = []
        self.globals = {}
        self.tests = {}
    def tag(self, func,name=None):
        if name==None:
            name = getattr(func, "_decorated_function", func).__name__
        self.globals[name] = func

    def filter(self, func,name=None):
        if name==None:
            name = getattr(func, "_decorated_function", func).__name__
        self.filters[name] = func

    def extension(self, ext):
        self.extensions.append(ext)
    
    def set(self,*args,**kwargs):
        for k in kwargs.keys(): #is a object with a name
            self[k] = kwargs[k]
        for a in args:
            self.tag(a) #is a function

    def inclusion_tag(self,template,func,takes_context=False):
        if takes_context:
            import jinja2
            @jinja2.contextfunction
            def tag(context,*args,**kwargs):
                from django.template.loader import render_to_string
                return render_to_string(template, func(dict_from_context(context),*args,**kwargs))

        else:
            def tag(*args,**kwargs):
                from django.template.loader import render_to_string
                return render_to_string(template, func(*args,**kwargs))

        #raise Exception(getattr(func, "_decorated_function", func))
        self.tag(tag,name=getattr(func, "_decorated_function", func).__name__)

    def __setitem__(self, item, value):
        self.globals[item] = value

    def __getitem__(self, item, value): #for reciprocity with __setitem__
        return globals[item]


initial_params = {
    'autoescape': False,
    'loader': FileSystemLoader(app_directories.app_template_dirs + settings.TEMPLATE_DIRS),
    'extensions':['jinja2.ext.i18n'] + JINJA2_EXTENSIONS,
}

initial_params.update(JINJA2_ENVIRONMENT_OPTIONS)
env = Environment(**initial_params)
