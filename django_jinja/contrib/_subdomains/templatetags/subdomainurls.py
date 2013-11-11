# -*- coding: utf-8 -*-

from jinja2 import contextfunction
from django_jinja import library
from subdomains.templatetags.subdomainurls import url as subdomain_url


lib = library.Library()

@lib.global_function
@contextfunction
def url(context, *args, **kwargs):
    return subdomain_url(context, *args, **kwargs)
