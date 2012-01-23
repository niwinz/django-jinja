# -*- coding: utf-8 -*-
from django.conf import settings
from django.template import TemplateDoesNotExist
from django.template.loaders import app_directories
from django.template.loaders import filesystem

from django_jinja import env

DEFAULT_JINJA2_TEMPLATE_EXTENSION = getattr(settings, 
    'DEFAULT_JINJA2_TEMPLATE_EXTENSION', '.jinja')

class LoaderMixin(object):
    def load_template(self, template_name, template_dirs=None):
        if not template_name.endswith(DEFAULT_JINJA2_TEMPLATE_EXTENSION):
            return super(FileSystemLoader, self).load_template(template_name, template_dirs)

        try:
            template = self.env.get_template(template_name)
            return template, template.filename
        except jinja2.TemplateNotFound:
            raise TemplateDoesNotExist(template_name)


class FileSystemLoader(LoaderMixin, filesystem.Loader):
    is_usable = True


class AppLoader(LoaderMixin, app_directories.Loader):
    is_usable = True
