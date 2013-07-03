# -*- coding: utf-8 -*-

from django.contrib.humanize.templatetags import humanize
from django_jinja import library

lib = library.Library()

@lib.filter
def ordinal(source):
    return humanize.ordinal(source)


@lib.filter
def intcomma(source, use_l10n=True):
    return humanize.intcomma(source, use_l10n)


@lib.filter
def intword(source):
    return humanize.intword(source)


@lib.filter
def apnumber(source):
    return humanize.apnumber(source)


@lib.filter
def naturalday(source, arg=None):
    return humanize.naturalday(source, arg)


@lib.filter
def naturaltime(source):
    return humanize.naturaltime(source)
