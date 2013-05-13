# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

from sr import sr
from django_jinja import library

lib = library.Library()

lib.global_function(sr)
