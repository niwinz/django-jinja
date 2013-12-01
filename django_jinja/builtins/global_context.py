# -*- coding: utf-8 -*-

import logging

from django.conf import settings
from django.core.urlresolvers import reverse as django_reverse, NoReverseMatch
from django.contrib.staticfiles.storage import staticfiles_storage

JINJA2_MUTE_URLRESOLVE_EXCEPTIONS = getattr(settings, "JINJA2_MUTE_URLRESOLVE_EXCEPTIONS", False)
logger = logging.getLogger(__name__)


def url(name, *args, **kwargs):
    """
    Shortcut filter for reverse url on templates. Is a alternative to
    django {% url %} tag, but more simple.

    Usage example:
        {{ url('web:timeline', userid=2) }}

    This is a equivalent to django:
        {% url 'web:timeline' userid=2 %}

    """
    try:
        return django_reverse(name, args=args, kwargs=kwargs)
    except NoReverseMatch as exc:
        logger.error('Error: %s', exc)
        if not JINJA2_MUTE_URLRESOLVE_EXCEPTIONS:
            raise
        return ''


def static(path):
    return staticfiles_storage.url(path)
