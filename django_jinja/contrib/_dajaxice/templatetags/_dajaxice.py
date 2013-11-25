# -*- coding: utf-8 -*-

from jinja2 import contextfunction
from django_jinja import library, utils

lib = library.Library()

@lib.global_function
@utils.safe
@contextfunction
def dajaxice_js_import(context, *args, **kwargs):
    from dajaxice.templatetags import dajaxice_templatetags as dajaxice_tags
    return dajaxice_tags.dajaxice_js_import(context, *args, **kwargs)
