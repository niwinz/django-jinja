from __future__ import unicode_literals

import traceback
import logging

import django
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.cache import cache
try:
    from django.urls import NoReverseMatch
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import NoReverseMatch
    from django.core.urlresolvers import reverse

from django.utils.formats import localize
from django.utils.translation import pgettext
from django.utils.translation import ugettext
from jinja2 import Markup
from jinja2 import TemplateSyntaxError
from jinja2 import lexer
from jinja2 import nodes
from jinja2.ext import Extension

try:
    from django.utils.encoding import force_text
    from django.utils.encoding import force_bytes
except ImportError:
    from django.utils.encoding import force_unicode as force_text
    from django.utils.encoding import smart_str as force_bytes


JINJA2_MUTE_URLRESOLVE_EXCEPTIONS = getattr(settings, "JINJA2_MUTE_URLRESOLVE_EXCEPTIONS", False)
logger = logging.getLogger(__name__)



# Compatibility with django <= 1.5

if django.VERSION[:2] <= (1, 5):
    import hashlib
    from django.utils.http import urlquote

    def make_template_fragment_key(fragm_name, vary_on):
        args_map = map(urlquote, vary_on)
        args_map = map(lambda x: force_bytes(x), args_map)

        args_string = b':'.join(args_map)
        args_hash = hashlib.md5(args_string).hexdigest()

        return 'template.cache.{0}.{1}'.format(fragm_name, args_hash)
else:
    from django.core.cache.utils import make_template_fragment_key


class CsrfExtension(Extension):
    tags = set(['csrf_token'])

    def __init__(self, environment):
        self.environment = environment

    def parse(self, parser):
        lineno = parser.stream.expect('name:csrf_token').lineno
        call = self.call_method(
            '_render',
            [nodes.Name('csrf_token', 'load', lineno=lineno)],
            lineno=lineno
        )
        return nodes.Output([nodes.MarkSafe(call)])

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

        cache_key = make_template_fragment_key(fragm_name, vary_on)

        value = cache.get(cache_key)
        if value is None:
            value = caller()
            cache.set(cache_key, force_text(value), expire_time)
        else:
            value = force_text(value)

        return value

class StaticFilesExtension(Extension):
    def __init__(self, environment):
        super(StaticFilesExtension, self).__init__(environment)
        environment.globals["static"] = self._static

    def _static(self, path):
        return staticfiles_storage.url(path)


class UrlsExtension(Extension):
    def __init__(self, environment):
        super(UrlsExtension, self).__init__(environment)
        environment.globals["url"] = self._url_reverse

    def _url_reverse(self, name, *args, **kwargs):
        try:
            return reverse(name, args=args, kwargs=kwargs)
        except NoReverseMatch as exc:
            logger.error('Error: %s', exc)
            if not JINJA2_MUTE_URLRESOLVE_EXCEPTIONS:
                raise
            return ''
        return reverse(name, args=args, kwargs=kwargs)


from . import filters

class TimezoneExtension(Extension):
    def __init__(self, environment):
        super(TimezoneExtension, self).__init__(environment)
        environment.globals["utc"] = filters.utc
        environment.globals["timezone"] = filters.timezone
        environment.globals["localtime"] = filters.localtime


class DjangoFiltersExtension(Extension):
    def __init__(self, environment):
        super(DjangoFiltersExtension, self).__init__(environment)
        environment.filters["static"] = filters.static
        environment.filters["reverseurl"] = filters.reverse
        environment.filters["addslashes"] = filters.addslashes
        environment.filters["capfirst"] = filters.capfirst
        environment.filters["escapejs"] = filters.escapejs_filter
        environment.filters["floatformat"] = filters.floatformat
        environment.filters["iriencode"] = filters.iriencode
        environment.filters["linenumbers"] = filters.linenumbers
        environment.filters["make_list"] = filters.make_list
        environment.filters["slugify"] = filters.slugify
        environment.filters["stringformat"] = filters.stringformat
        environment.filters["truncatechars"] = filters.truncatechars
        environment.filters["truncatechars_html"] = filters.truncatechars_html
        environment.filters["truncatewords"] = filters.truncatewords
        environment.filters["truncatewords_html"] = filters.truncatewords_html
        environment.filters["urlizetrunc"] = filters.urlizetrunc
        environment.filters["ljust"] = filters.ljust
        environment.filters["rjust"] = filters.rjust
        environment.filters["cut"] = filters.cut
        environment.filters["linebreaksbr"] = filters.linebreaksbr
        environment.filters["linebreaks"] = filters.linebreaks_filter
        environment.filters["striptags"] = filters.striptags
        environment.filters["add"] = filters.add
        environment.filters["date"] = filters.date
        environment.filters["time"] = filters.time
        environment.filters["timesince"] = filters.timesince_filter
        environment.filters["timeuntil"] = filters.timeuntil_filter
        environment.filters["default_if_none"] = filters.default_if_none
        environment.filters["divisibleby"] = filters.divisibleby
        environment.filters["yesno"] = filters.yesno
        environment.filters["pluralize"] = filters.pluralize
        environment.filters["localtime"] = filters.localtime
        environment.filters["utc"] = filters.utc
        environment.filters["timezone"] = filters.timezone


class DjangoExtraFiltersExtension(Extension):
    def __init__(self, environment):
        super(DjangoExtraFiltersExtension, self).__init__(environment)
        environment.filters["title"] = filters.title
        environment.filters["upper"] = filters.upper
        environment.filters["lower"] = filters.lower
        environment.filters["urlencode"] = filters.urlencode
        environment.filters["urlize"] = filters.urlize
        environment.filters["wordcount"] = filters.wordcount
        environment.filters["wordwrap"] = filters.wordwrap
        environment.filters["center"] = filters.center
        environment.filters["join"] = filters.join
        environment.filters["length"] = filters.length
        environment.filters["random"] = filters.random
        environment.filters["default"] = filters.default
        environment.filters["filesizeformat"] = filters.filesizeformat
        environment.filters["pprint"] = filters.pprint
