# -*- coding: utf-8 -*-
from django.conf import settings
from django.template import TemplateDoesNotExist
from django.template.loaders import app_directories
from django.template.loaders import filesystem

from django_jinja.base import env
import jinja2

DEFAULT_JINJA2_TEMPLATE_EXTENSION = getattr(settings, 
    'DEFAULT_JINJA2_TEMPLATE_EXTENSION', '.jinja')

class LoaderMixin(object):
    is_usable = True

    def load_template(self, template_name, template_dirs=None):
        if not template_name.endswith(DEFAULT_JINJA2_TEMPLATE_EXTENSION):
            return super(LoaderMixin, self).load_template(template_name, template_dirs)
        
        try:
            template = env.get_template(template_name)
            return template, template.filename
        except jinja2.TemplateNotFound:
            raise TemplateDoesNotExist(template_name)


class FileSystemLoader(LoaderMixin, filesystem.Loader):
    pass


class AppLoader(LoaderMixin, app_directories.Loader):
    pass
