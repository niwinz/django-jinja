# -*- coding: utf-8 -*-

import functools
from importlib import import_module

import django
from django.utils.safestring import mark_safe
from django.core.exceptions import ImproperlyConfigured


DJANGO_18 = (django.VERSION[:2] == (1, 8))


def load_class(path):
    """
    Load class from path.
    """

    try:
        mod_name, klass_name = path.rsplit('.', 1)
        mod = import_module(mod_name)
    except AttributeError as e:
        raise ImproperlyConfigured('Error importing {0}: "{1}"'.format(mod_name, e))

    try:
        klass = getattr(mod, klass_name)
    except AttributeError:
        raise ImproperlyConfigured('Module "{0}" does not define a "{1}" class'.format(mod_name, klass_name))

    return klass


def safe(function):
    @functools.wraps(function)
    def _decorator(*args, **kwargs):
        return mark_safe(function(*args, **kwargs))
    return _decorator

