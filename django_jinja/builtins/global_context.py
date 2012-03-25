# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse as django_reverse

def url(name, *args, **kwargs):
    """
    Shortcut filter for reverse url on templates. Is a alternative to
    django {% url %} tag, but more simple.

    Usage example:
        {{ url('web:timeline', userid=2) }}

    This is a equivalent to django: 
        {% url 'web:timeline' userid=2 %}

    """
    return django_reverse(name, args=args, kwargs=kwargs)
