# -*- coding: utf-8 -*-

from easy_thumbnails.templatetags import thumbnail as _thumbnail
from django_jinja import library
lib = library.Library()


@lib.filter
def thumbnail_url(source, alias):
    return _thumbnail.thumbnail_url(source, alias)


@lib.global_function
def thumbnailer_passive(obj):
    return _thumbnail.thumbnailer_passive(obj)


@lib.global_function
def thumbnailer(obj):
    return _thumbnail.thumbnailer(obj)


@lib.global_function
def thumbnail(source, **kwargs):
    thumb = _thumbnail.get_thumbnailer(source).get_thumbnail(kwargs)
    return thumb.url
