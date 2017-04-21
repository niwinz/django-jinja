from copy import copy
from django_jinja import library
from widget_tweaks.templatetags import widget_tweaks


@library.filter
def attr(field, attr):
    return widget_tweaks.set_attr(field, attr)


@library.filter
def add_error_attr(field, attr):
    return widget_tweaks.add_error_attr(field, attr)


@library.filter
def append_attr(field, attr):
    return widget_tweaks.append_attr(field, attr)


@library.filter
def add_class(field, css_class):
    return widget_tweaks.add_class(field, css_class)


@library.filter
def add_error_class(field, css_class):
    return widget_tweaks.add_error_class(field, css_class)


@library.filter
def set_data(field, data):
    return widget_tweaks.set_data(field, data)


@library.filter
def field_type(field):
    return widget_tweaks.field_type(field)


@library.filter
def widget_type(field):
    return widget_tweaks.widget_type(field)


@library.global_function
def render_field(field, **kwargs):
    attrs = copy(field.field.widget.attrs)
    field.field.widget.attrs.update(kwargs)
    try:
        return str(field)
    finally:
        for key in kwargs:
            del field.field.widget.attrs[key]
        field.field.widget.attrs.update(attrs)
