from __future__ import unicode_literals

from django.conf import settings
from django.core.cache import cache
from django.utils.http import urlquote

from jinja2.ext import Extension
from jinja2 import nodes
from jinja2 import Markup

import hashlib
import traceback


class CsrfExtension(Extension):
    tags = set(['csrf_token'])

    def __init__(self, environment):
        self.environment = environment

    def parse(self, parser):
        try:
            token = next(parser.stream)
            call_res = self.call_method('_render', [nodes.Name('csrf_token','load')])
            return nodes.Output([call_res]).set_lineno(token.lineno)
        except Exception:
            traceback.print_exc()

    def _render(self, csrf_token):
        if csrf_token:
            if csrf_token == 'NOTPROVIDED':
                return Markup("")

            return Markup("<input type='hidden'"
                          " name='csrfmiddlewaretoken' value='%s' />" % (csrf_token))

        if settings.DEBUG:
            import warnings
            warnings.warn("A {% csrf_token %} was used in a template, but the context"
                          "did not provide the value.  This is usually caused by not "
                          "using RequestContext.")
        return ''


class CacheExtension(Extension):
    """
    Exactly like Django's own tag, but supports full Jinja2
    expressiveness for all arguments.

        {% cache gettimeout()*2 "foo"+options.cachename  %}
            ...
        {% endcache %}

    General Syntax:

        {% cache [expire_time] [fragment_name] [var1] [var2] .. %}
            .. some expensive processing ..
        {% endcache %}

    Available by default (does not need to be loaded).

    Partly based on the ``FragmentCacheExtension`` from the Jinja2 docs.
    """

    tags = set(['cache'])

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        expire_time = parser.parse_expression()
        fragment_name = parser.parse_expression()
        vary_on = []

        while not parser.stream.current.test('block_end'):
            vary_on.append(parser.parse_expression())

        body = parser.parse_statements(['name:endcache'], drop_needle=True)

        return nodes.CallBlock(
            self.call_method('_cache_support',
                             [expire_time, fragment_name,
                              nodes.List(vary_on), nodes.Const(lineno)]),
            [], [], body).set_lineno(lineno)

    def _cache_support(self, expire_time, fragm_name, vary_on, lineno, caller):
        try:
            expire_time = int(expire_time)
        except (ValueError, TypeError):
            raise TemplateSyntaxError('"%s" tag got a non-integer timeout '
                'value: %r' % (list(self.tags)[0], expire_time), lineno)

        args_map = map(urlquote, vary_on)
        args_map = map(lambda x: x.encode('utf-8'), args_map)

        args_string = b':'.join(args_map)
        args_hash = hashlib.md5(args_string).hexdigest()

        cache_key = 'template.cache.{0}.{1}'.format(fragm_name, args_hash)

        value = cache.get(cache_key)
        if value is not None:
            return value.decode('utf-8')

        value = caller()
        cache.set(cache_key, value.encode('utf-8'), expire_time)
        return value
