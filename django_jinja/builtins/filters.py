# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse as django_reverse
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode, iri_to_uri
from django.utils.text import Truncator, wrap, phone2numeric
from django.utils.formats import date_format, time_format, number_format
from django.utils.timesince import timesince, timeuntil
from django.utils.html import escapejs, strip_tags, conditional_escape, fix_ampersands, \
    escape, urlize as urlize_impl, linebreaks, strip_tags

from django.utils.text import normalize_newlines
from decimal import InvalidOperation, Decimal, ROUND_HALF_UP, Context
from pprint import pformat
from jinja2 import Markup

import re
import unicodedata

def safe(value):
    return Markup(force_unicode(value))

def reverse(value, *args, **kwargs):
    """
    Shortcut filter for reverse url on templates. Is a alternative to
    django {% url %} tag, but more simple.

    Usage example:
        {{ 'web:timeline'|reverse(userid=2) }}

    This is a equivalent to django: 
        {% url 'web:timeline' userid=2 %}

    """
    return django_reverse(value, args=args, kwargs=kwargs)


def addslashes(value):
    """
    Adds slashes before quotes. Useful for escaping strings in CSV, for
    example. Less useful for escaping JavaScript; use the ``escapejs``
    filter instead.
    """
    return value.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")


def escapejs_filter(value):
    """
    Hex encodes characters for use in JavaScript strings.
    """
    return escapejs(value)


def capfirst(value):
    """
    Capitalizes the first character of the value.
    """
    return value and value[0].upper() + value[1:]


def floatformat(text, arg=-1):
    """
    Displays a float to a specified number of decimal places.
    
    If called without an argument, it displays the floating point number with
    one decimal place -- but only if there's a decimal place to be displayed:
    
    * num1 = 34.23234
    * num2 = 34.00000
    * num3 = 34.26000
    * {{ num1|floatformat }} displays "34.2"
    * {{ num2|floatformat }} displays "34"
    * {{ num3|floatformat }} displays "34.3"
    
    If arg is positive, it will always display exactly arg number of decimal
    places:
    
    * {{ num1|floatformat:3 }} displays "34.232"
    * {{ num2|floatformat:3 }} displays "34.000"
    * {{ num3|floatformat:3 }} displays "34.260"
    
    If arg is negative, it will display arg number of decimal places -- but
    only if there are places to be displayed:
    
    * {{ num1|floatformat:"-3" }} displays "34.232"
    * {{ num2|floatformat:"-3" }} displays "34"
    * {{ num3|floatformat:"-3" }} displays "34.260"
    
    If the input float is infinity or NaN, the (platform-dependent) string
    representation of that value will be displayed.
    """
    
    try:
        input_val = force_unicode(text)
        d = Decimal(input_val)
    except UnicodeEncodeError:
        return u''
    except InvalidOperation:
        if input_val in special_floats:
            return input_val
        try:
            d = Decimal(force_unicode(float(text)))
        except (ValueError, InvalidOperation, TypeError, UnicodeEncodeError):
            return u''
    try:
        p = int(arg)
    except ValueError:
        return input_val
    
    try:
        m = int(d) - d
    except (ValueError, OverflowError, InvalidOperation):
        return input_val
    
    if not m and p < 0:
        return number_format(u'%d' % (int(d)), 0)
    
    if p == 0:
        exp = Decimal(1)
    else:
        exp = Decimal(u'1.0') / (Decimal(10) ** abs(p))
    try:
        # Set the precision high enough to avoid an exception, see #15789.
        tupl = d.as_tuple()
        units = len(tupl[1]) - tupl[2]
        prec = abs(p) + units + 1
    
        # Avoid conversion to scientific notation by accessing `sign`, `digits`
        # and `exponent` from `Decimal.as_tuple()` directly.
        sign, digits, exponent = d.quantize(exp, ROUND_HALF_UP,
            Context(prec=prec)).as_tuple()
        digits = [unicode(digit) for digit in reversed(digits)]
        while len(digits) <= abs(exponent):
            digits.append(u'0')
        digits.insert(-exponent, u'.')
        if sign:
            digits.append(u'-')
        number = u''.join(reversed(digits))
        return number_format(number, abs(p))
    except InvalidOperation:
        return input_val


@stringfilter
def truncatechars(value, arg):
    """
    Truncates a string after a certain number of characters.

    Argument: Number of characters to truncate after.
    """
    try:
        length = int(arg)
    except ValueError: # Invalid literal for int().
        return value # Fail silently.
    return Truncator(value).chars(length)


@stringfilter
def truncatewords(value, arg):
    """
    Truncates a string after a certain number of words.

    Argument: Number of words to truncate after.

    Newlines within the string are removed.
    """
    try:
        length = int(arg)
    except ValueError: # Invalid literal for int().
        return value # Fail silently.
    return Truncator(value).words(length, truncate=' ...')

@stringfilter
def truncatewords_html(value, arg):
    """
    Truncates HTML after a certain number of words.

    Argument: Number of words to truncate after.

    Newlines in the HTML are preserved.
    """
    try:
        length = int(arg)
    except ValueError: # invalid literal for int()
        return value # Fail silently.
    return Truncator(value).words(length, html=True, truncate=' ...')


@stringfilter
def wordwrap(value, arg):
    """
    Wraps words at specified line length.

    Argument: number of characters to wrap the text at.
    """
    return wrap(value, int(arg))

@stringfilter
def title(value):
    """Converts a string into titlecase."""
    t = re.sub("([a-z])'([A-Z])", lambda m: m.group(0).lower(), value.title())
    return re.sub("\d([A-Z])", lambda m: m.group(0).lower(), t)

@stringfilter
def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)

@stringfilter
def lower(value):
    """Converts a string into all lowercase."""
    return value.lower()

@stringfilter
def ljust(value, arg):
    """
    Left-aligns the value in a field of a given width.

    Argument: field size.
    """
    return value.ljust(int(arg))


@stringfilter
def rjust(value, arg):
    """
    Right-aligns the value in a field of a given width.

    Argument: field size.
    """
    return value.rjust(int(arg))

@stringfilter
def linebreaksbr(value, autoescape=None):
    """
    Converts all newlines in a piece of plain text to HTML line breaks
    (``<br />``).
    """
    autoescape = autoescape and not isinstance(value, SafeData)
    value = normalize_newlines(value)
    if autoescape:
        value = escape(value)
    return value.replace('\n', '<br />')

@stringfilter
def linebreaks_filter(value):
    """
    Replaces line breaks in plain text with appropriate HTML; a single
    newline becomes an HTML line break (``<br />``) and a new line
    followed by a blank line becomes a paragraph break (``</p>``).
    """
    return linebreaks(value, False)

@stringfilter
def removetags(value, tags):
    """Removes a space separated list of [X]HTML tags from the output."""
    tags = [re.escape(tag) for tag in tags.split()]
    tags_re = u'(%s)' % u'|'.join(tags)
    starttag_re = re.compile(ur'<%s(/?>|(\s+[^>]*>))' % tags_re, re.U)
    endtag_re = re.compile(u'</%s>' % tags_re)
    value = starttag_re.sub(u'', value)
    value = endtag_re.sub(u'', value)
    return value

@stringfilter
def striptags(value):
    """Strips all [X]HTML tags."""
    return strip_tags(value)


def join(value, arg, autoescape=None):
    """
    Joins a list with a string, like Python's ``str.join(list)``.
    """
    value = map(force_unicode, value)
    if autoescape:
        value = [conditional_escape(v) for v in value]
    try:
        data = conditional_escape(arg).join(value)
    except AttributeError: # fail silently but nicely
        return value
    return data

def random(value):
    """Returns a random item from the list."""
    return random_module.choice(value)

def add(value, arg):
    """Adds the arg to the value."""
    try:
        return int(value) + int(arg)
    except (ValueError, TypeError):
        try:
            return value + arg
        except Exception:
            return ''

from django.utils import formats
from django.utils.dateformat import format, time_format


def date(value, arg=None):
    """Formats a date according to the given format."""
    if not value:
        return u''
    if arg is None:
        arg = settings.DATE_FORMAT
    try:
        return formats.date_format(value, arg)
    except AttributeError:
        try:
            return format(value, arg)
        except AttributeError:
            return ''

def time(value, arg=None):
    """Formats a time according to the given format."""
    if value in (None, u''):
        return u''
    if arg is None:
        arg = settings.TIME_FORMAT
    try:
        return formats.time_format(value, arg)
    except AttributeError:
        try:
            return time_format(value, arg)
        except AttributeError:
            return ''

def timesince_filter(value, arg=None):
    """Formats a date as the time since that date (i.e. "4 days, 6 hours")."""
    if not value:
        return u''
    try:
        if arg:
            return timesince(value, arg)
        return timesince(value)
    except (ValueError, TypeError):
        return u''

def timeuntil_filter(value, arg=None):
    """Formats a date as the time until that date (i.e. "4 days, 6 hours")."""
    if not value:
        return u''
    try:
        return timeuntil(value, arg)
    except (ValueError, TypeError):
        return u''

def default(value, arg):
    """If value is unavailable, use given default."""
    return value or arg

def default_if_none(value, arg):
    """If value is None, use given default."""
    if value is None:
        return arg
    return value

def divisibleby(value, arg):
    """Returns True if the value is devisible by the argument."""
    return int(value) % int(arg) == 0

def yesno(value, arg=None):
    """
    Given a string mapping values for true, false and (optionally) None,
    returns one of those strings according to the value:

    ==========  ======================  ==================================
    Value       Argument                Outputs
    ==========  ======================  ==================================
    ``True``    ``"yeah,no,maybe"``     ``yeah``
    ``False``   ``"yeah,no,maybe"``     ``no``
    ``None``    ``"yeah,no,maybe"``     ``maybe``
    ``None``    ``"yeah,no"``           ``"no"`` (converts None to False
                                        if no mapping for None is given.
    ==========  ======================  ==================================
    """
    if arg is None:
        arg = ugettext('yes,no,maybe')
    bits = arg.split(u',')
    if len(bits) < 2:
        return value # Invalid arg.
    try:
        yes, no, maybe = bits
    except ValueError:
        # Unpack list of wrong size (no "maybe" value provided).
        yes, no, maybe = bits[0], bits[1], bits[1]
    if value is None:
        return maybe
    if value:
        return yes
    return no

def filesizeformat(bytes):
    """
    Formats the value like a 'human-readable' file size (i.e. 13 KB, 4.1 MB,
    102 bytes, etc).
    """
    try:
        bytes = float(bytes)
    except (TypeError,ValueError,UnicodeDecodeError):
        return ungettext("%(size)d byte", "%(size)d bytes", 0) % {'size': 0}

    filesize_number_format = lambda value: number_format(round(value, 1), 1)

    if bytes < 1024:
        return ungettext("%(size)d byte", "%(size)d bytes", bytes) % {'size': bytes}
    if bytes < 1024 * 1024:
        return ugettext("%s KB") % filesize_number_format(bytes / 1024)
    if bytes < 1024 * 1024 * 1024:
        return ugettext("%s MB") % filesize_number_format(bytes / (1024 * 1024))
    if bytes < 1024 * 1024 * 1024 * 1024:
        return ugettext("%s GB") % filesize_number_format(bytes / (1024 * 1024 * 1024))
    if bytes < 1024 * 1024 * 1024 * 1024 * 1024:
        return ugettext("%s TB") % filesize_number_format(bytes / (1024 * 1024 * 1024 * 1024))
    return ugettext("%s PB") % filesize_number_format(bytes / (1024 * 1024 * 1024 * 1024 * 1024))

def pprint(value):
    """A wrapper around pprint.pprint -- for debugging, really."""
    try:
        return pformat(value)
    except Exception, e:
        return u"Error in formatting: %s" % force_unicode(e, errors="replace")

