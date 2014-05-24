# -*- coding: utf-8 -*-

from django_jinja.library import Library
import jinja2

register = Library()

@register.test(name="one")
def is_one(n):
    return n == 1


@register.filter
@jinja2.contextfilter
def replace(context, value, x, y):
    return value.replace(x, y)


@register.global_function
def myecho(data):
    return data
