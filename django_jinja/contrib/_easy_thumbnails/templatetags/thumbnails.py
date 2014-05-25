# -*- coding: utf-8 -*-

from easy_thumbnails.templatetags import thumbnail as _thumbnail
from django_jinja import library


@library.filter
def thumbnail_url(source, alias):
    return _thumbnail.thumbnail_url(source, alias)


@library.global_function
def thumbnailer_passive(obj):
    return _thumbnail.thumbnailer_passive(obj)


@library.global_function
def thumbnailer(obj):
    return _thumbnail.thumbnailer(obj)


@library.global_function
def thumbnail(source, **kwargs):
    thumbnail =  _thumbnail.get_thumbnailer(source).get_thumbnail(kwargs)
    return thumbnail.url
