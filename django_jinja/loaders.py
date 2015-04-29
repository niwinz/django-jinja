"""
Api for django <= 1.7.x that uses loader extending
way for get it working.
"""

import re
import jinja2

from django.conf import settings
from django.template import TemplateDoesNotExist
from django.template.loaders import app_directories
from django.template.loaders import filesystem
from . import base

if hasattr(settings, "DEFAULT_JINJA2_TEMPLATE_INTERCEPT_RE"):
    INTERCEPT_RE = getattr(settings, "DEFAULT_JINJA2_TEMPLATE_INTERCEPT_RE")
    REGEX = re.compile(INTERCEPT_RE)
    EXTENSION = None
else:
    REGEX = None
    EXTENSION = getattr(settings, 'DEFAULT_JINJA2_TEMPLATE_EXTENSION', '.jinja')


class LoaderMixin(object):
    is_usable = True

    def match_template(self, template_name):
        return base.match_template(template_name, regex=REGEX, extension=EXTENSION)

    def load_template(self, template_name, template_dirs=None):
        if self.match_template(template_name):
            try:
                template = base.env.get_template(template_name)
                return template, template.filename
            except jinja2.TemplateNotFound:
                raise TemplateDoesNotExist(template_name)
        else:
            return super(LoaderMixin, self).load_template(template_name, template_dirs)


class FileSystemLoader(LoaderMixin, filesystem.Loader):
    pass


class AppLoader(LoaderMixin, app_directories.Loader):
    pass
