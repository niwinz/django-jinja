# -*- coding: utf-8 -*-

from django_jinja import library
from jinja2 import contextfunction
from subdomains.templatetags.subdomainurls import url as subdomain_url


@library.global_function
@contextfunction
def url(context, *args, **kwargs):
    return subdomain_url(context, *args, **kwargs)
