# -*- coding: utf-8 -*-

from django_jinja.base import Library
import jinja2

register = Library()

@register.filter
@jinja2.contextfilter
def datetimeformat(ctx, value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)

@register.global_context
def hello(name):
    return "Hello" + name
