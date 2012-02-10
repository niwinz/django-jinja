# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

def url(value, *args, **kwargs):
    """
    Shortcut filter for reverse url on templates. Is a alternative to
    django {% url %} tag, but more simple.

    Usage example:
        {{ 'web:timeline'|url(userid=2) }}

    This is a equivalent to django: 
        {% url 'web:timeline' userid=2 %}

    """
    return  reverse(value, args=args, kwargs=kwargs)
