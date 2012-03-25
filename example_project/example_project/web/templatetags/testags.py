# -*- coding: utf-8 -*-

from django_jinja.base import Library

register = Library()

@register.filter
def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)

@register.global_context
def hello(name):    
    return "Hello" + name
