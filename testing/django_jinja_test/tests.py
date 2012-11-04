# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

from django.test import TestCase
from django.test.client import RequestFactory
from django.template.loader import render_to_string
from django.template import RequestContext

from django_jinja.base import env, dict_from_context
import datetime

class TemplateFunctionsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def tearDown(self):
        pass

    def test_template_filters(self):
        filters_data = [
            ("{{ 'test-1'|reverseurl }}", {}, '/test1/'),
            ("{{ 'test-1'|reverseurl(data=2) }}", {}, '/test1/2/'),
            ("{{ num|floatformat }}", {'num': 34.23234}, '34.2'),
            ("{{ num|floatformat(3) }}", {'num': 34.23234}, '34.232'),
            ("{{ 'hola'|capfirst }}", {}, "Hola"),
            ("{{ 'hola mundo'|truncatechars(5) }}", {}, "ho..."),
            ("{{ 'hola mundo'|truncatewords(1) }}", {}, "hola ..."),
            ("{{ 'hola mundo'|truncatewords_html(1) }}", {}, "hola ..."),
            ("{{ 'hola mundo'|wordwrap(1) }}", {}, "hola\nmundo"),
            ("{{ 'hola mundo'|title }}", {}, "Hola Mundo"),
            ("{{ 'hola mundo'|slugify }}", {}, "hola-mundo"),
            ("{{ 'hello'|ljust(10) }}", {}, "hello     "),
            ("{{ 'hello'|rjust(10) }}", {}, "     hello"),
            ("{{ 'hello\nworld'|linebreaksbr }}", {}, "hello<br />world"),
            ("{{ '<div>hello</div>'|removetags('div') }}", {}, "hello"),
            ("{{ '<div>hello</div>'|striptags }}", {}, "hello"),
            ("{{ list|join(',') }}", {'list':['a','b']}, 'a,b'),
            ("{{ 3|add(2) }}", {}, "5"),
            ("{{ now|date('n Y') }}", {"now": datetime.datetime(2012, 12, 20)}, "12 2012"),
        ]

        print()
        for template_str, kwargs, result in filters_data:
            print("- Testing: ", template_str, "with:", kwargs)

            template = env.from_string(template_str)
            _result = template.render(kwargs)
            self.assertEqual(_result, result)

    def test_custom_addons_01(self):
        template = env.from_string("{{ 'Hello'|replace('H','M') }}")
        result = template.render({})

        self.assertEqual(result, "Mello")

    def test_custom_addons_02(self):
        template = env.from_string("{% if m is one %}Foo{% endif %}")
        result = template.render({'m': 1})

        self.assertEqual(result, "Foo")

    def test_custom_addons_03(self):
        template = env.from_string("{{ myecho('foo') }}")
        result = template.render({})

        self.assertEqual(result, "foo")

    def test_autoescape_01(self):
        old_autoescape_value = env.autoescape
        env.autoescape = True

        template = env.from_string("{{ foo|safe }}")
        result = template.render({'foo': '<h1>Hellp</h1>'})
        self.assertEqual(result, "<h1>Hellp</h1>")

        env.autoescape = old_autoescape_value

    def test_autoescape_02(self):
        old_autoescape_value = env.autoescape
        env.autoescape = True

        template = env.from_string("{{ foo }}")
        result = template.render({'foo': '<h1>Hellp</h1>'})
        self.assertEqual(result, "&lt;h1&gt;Hellp&lt;/h1&gt;")

        env.autoescape = old_autoescape_value

    def test_csrf_01(self):
        template_content = "{% csrf_token %}"

        request = self.factory.get('/customer/details')
        request.META["CSRF_COOKIE"] = '1234123123'

        context = dict_from_context(RequestContext(request))

        template = env.from_string(template_content)
        result = template.render(context)
        self.assertEqual(result, "<input type='hidden' name='csrfmiddlewaretoken' value='1234123123' />")

    def test_cache_01(self):
        template_content = "{% cache 200 'fooo' %}foo bar{% endcache %}"

        request = self.factory.get('/customer/details')
        context = dict_from_context(RequestContext(request))

        template = env.from_string(template_content)
        result = template.render(context)

        self.assertEqual(result, "foo bar")
